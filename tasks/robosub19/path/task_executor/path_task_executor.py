from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.path.locator.ml_solution.yolo_soln import YoloPathLocator
from tasks.path.locator.cv_solution.barbarian_locator import BarbarianLocator
from neural_networks.utils import extract_prediction
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from configs.config import get_config
import cv2
from utils.python_rest_subtask import PythonRESTSubtask
from vision.camera_server import set_bb, get_image
from neural_networks.nn_manager import NNManager

class PathTaskExecutor(ITaskExecutor):
    def __init__(self, contorl_dict: Movements, sensors_dict, cameras_dict: Cameras, main_logger):
        self._control = contorl_dict
        self._bottom_camera = cameras_dict['bottom_camera']
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._logger = main_logger
        self.config = get_config("tasks")['path_task']
        # For which path we are taking angle. For each path, rotation 
        # angle might be set differently in cnfig.json
        self.number = 0

    def run(self):
        self._logger.log("start path task executor _ ml")
        self._control.pid_turn_on()
        #self._control.pid_set_depth(1.5)
        self._control.pid_yaw_turn_on()
        self._logger.log("tuning on depth and yaw control")

        #if not self.find_path():
        #    return 0

        if not self.center_on_path():
            return 0

        #if not self.rotate():
        #    return 0

        return 1

    def find_path(self):
        config = self.config['search']
        ENGINE_POWER = config['max_engine_power']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']
        MAX_TIME_SEC = config['max_time_sec']

        self._logger.log("STARTING SEARCH FOR PATH!")

        self._control.set_lin_velocity(ENGINE_POWER, 0, 0)
        mvg_average = 0

        stopwatch = Stopwatch()
        stopwatch.start() 

        while(True):
            img = self._bottom_camera.get_image()
            bounding_box = extract_prediction(NNManager.get_yolo_model("path").predict(img), "bat")            
            # s\set_bb(bounding_box)

            if bounding_box is not None:
                mvg_average = (1 - MOVING_AVERAGE_DISCOUNT) + MOVING_AVERAGE_DISCOUNT * mvg_average
                self._bounding_box.mvg_avg(bounding_box, 0.5, True)
                self._logger.log(f"Detected possible path. Current confidence is {mvg_average}")
            else:
                mvg_average = 0 + MOVING_AVERAGE_DISCOUNT * mvg_average

            # Stop and report sucess if we are sure we found a path!
            if mvg_average > CONFIDENCE_THRESHOLD:
                self._control.set_lin_velocity(0,0,0)
                self._logger.log("Path is found!")
                
                return True 

            # Abort if we are running far away...
            if stopwatch.time() > MAX_TIME_SEC:
                self._control.set_lin_velocity(0,0,0)
                self._logger.log(f"Path not found in {MAX_TIME_SEC} seconds. Aborting...")
                return False 

    def center_on_path(self):
        config = self.config['centering']
        ENGINE_POWER = config['max_engine_power']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        MAXIMAL_DISTANCE_CENTER = config['max_center_distance']
        MAX_TIME_SEC = config['max_time_sec']

        self._logger.log("STARTING CENTERING ON PATH!")

        while(True):
            # img = self._bottom_camera.get_image()
            img = get_image("bottom")
            img = cv2.resize(img, (416, 416))
            bounding_box = NNManager.get_yolo_model("path").predict(img)
            print(bounding_box)
            bounding_box = extract_prediction(bounding_box, "bat")
            
            # Try again if yolo did not return a box
            # TODO: Maybe go back?
            if bounding_box is None:
                self._logger.log("Warning: Path not detected")
                continue

            self._bounding_box = bounding_box #.mvg_avg(bounding_box, 0.9, True)
        
            stopwatch = Stopwatch()
            stopwatch.start() 

            self._logger.log(f"Current detection x: {self._bounding_box.xc}")
            self._logger.log(f"Current detection y: {self._bounding_box.yc}")

            # Stop if centered...
            # TODO: Because of moving avg probably we are too far. Might be problem
            if abs(self._bounding_box.xc) < MAXIMAL_DISTANCE_CENTER and abs(self._bounding_box.yc) < MAXIMAL_DISTANCE_CENTER:
                self._control.set_lin_velocity(0,0,0)
                self._logger.log("Centered!")
                return True

            # Stop if centering too long...
            if stopwatch.time() > MAX_TIME_SEC:
                self._control.set_lin_velocity(0,0,0)
                return False

            # New speed is based on path distance from center
            front_speed = 0.5 * ENGINE_POWER * self._bounding_box.yc
            right_speed = -1 * ENGINE_POWER * self._bounding_box.xc

            self._control.set_lin_velocity(front_speed, right_speed, 0)

            # alternative movement option
            #front_move = 0.01 * self._bounding_box.yc
            #right_move = 0.01 * self._bounding_box.xc

            # self._control.move_distance(front=front_move, right=right_move)

    def rotate(self):
        config = self.config['turn']
        ALGORITHM_TYPE = config['type']
        
        if ALGORITHM_TYPE == "hardcoded":
            return self.rotate_hardcoded()
        
        return False

    def rotate_hardcoded(self):
        config = self.config['turn']['hardcoded']
        ANGLES = config['angles']

        # Check if rotation is defined for n-th path
        if len(ANGLES) <= self.number:
            return False

        self._control.rotate_angle(0,0,ANGLES[self.number])

        return True
