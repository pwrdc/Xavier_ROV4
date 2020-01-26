from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.gate.locator.ml_solution.yolo_soln import YoloGateLocator
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from neural_networks.utils import extract_prediction
from configs.config import get_config
from time import sleep
from vision.camera_server import get_image
import cv2

from utils.python_rest_subtask import PythonRESTSubtask

class GateTaskExecutor(ITaskExecutor):
    def __init__(self, contorl_dict: Movements, sensors_dict, cameras_dict: Cameras, main_logger):
        self._control = contorl_dict
        self._sensors = sensors_dict
        self._front_camera = cameras_dict['front_cam1']
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._logger = main_logger
        self.config = get_config("robosub19_tasks")['gate_task']
        self._target_depth = 0
        # For which path we are taking angle. For each path, rotation 
        # angle might be set differently in config.json
        self.number = 0

    def run(self):
        self._logger.log("Start gate task executor")
        self._control.pid_turn_on()
        self._control.pid_yaw_turn_on()
        self._logger.log("gate: turn on depth and yaw contorl")

        #if not self.find_gate():
        #    self._logger.log("gate: if not self.find_gate()")
        #    return 0

        if not self.center_on_gate():
            self._logger.log("gate: if not self.center_on_gate():")
            return 0

        if not self.go_through_gate():
            self._logger.log("gate: not self.go_through_gate()")
            return 0

        return 1

    def go_down(self, x):
        depth = self._sensors['depth'].get_depth()
        self._control.pid_set_depth(depth - x)
        self._logger.log("to pid " + str(depth - x))

    def find_gate(self):
        self._logger.log("finding the gate")
        config = self.config['search']
        MAX_ANG_SPEED = config['max_ang_speed']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']
        MAX_TIME_SEC = config['max_time_sec']
        ANGLE_DELTA = config['angle_delta']

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("searted find gate loop")

        confidence = 0
        self._target_depth = self._sensors['depth'].get_depth()
        while(True):
            img = get_image("front") # self._front_camera.get_image()
            img = cv2.resize(img, (416, 416))
            bounding_box = extract_prediction(YoloGateLocator().get_gate_bounding_box(img), "gate")

            if bounding_box is not None:
                confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT)
                self._bounding_box = bounding_box # mvg avg?
                self._logger.log(f"gate: somoething detected. Confidence: {confidence}")
            else:
                confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)
                self._logger.log(f"gate: Nothing detected. Confidence: {confidence}")
                # self._control.rotate_angle(0,0,ANGLE_DELTA)

            # Stop and report sucess if we are sure we found a path!
            if confidence > CONFIDENCE_THRESHOLD:
                self._logger.log("gate found")
                self._control.set_ang_velocity(0,0,0)
                return True 

            # Abort if we are running far away...
            if stopwatch.time() > MAX_TIME_SEC:
                self._logger.log("gate not found - aboart")
                self._control.set_ang_velocity(0,0,0)
                return False 

    def center_on_gate(self):
        self._logger.log("starting centering")
        config = self.config['centering']
        ENGINE_POWER = config['max_engine_power']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        MAXIMAL_DISTANCE_CENTER = config['max_center_distance']
        MAX_TIME_SEC = config['max_time_sec']

        while(True):
            img = get_image("front") # self._front_camera.get_image()
            img = cv2.resize(img, (416, 416))
            bounding_box = extract_prediction(YoloGateLocator().get_gate_bounding_box(img), "gate")

            # Try again if yolo did not return a box
            # TODO: Maybe go back?
            if bounding_box is None:
                continue

            self._bounding_box = bounding_box # .mvg_avg(bounding_box, MOVING_AVERAGE_DISCOUNT, True)
        
            stopwatch = Stopwatch()
            stopwatch.start() 

            xc = (self._bounding_box.x1 + self._bounding_box.x2) / 2 - 0.5
            yc = (self._bounding_box.y1 + self._bounding_box.y2) / 2 - 0.5

            self._logger.log(f"Current detection x: {xc}")
            self._logger.log(f"Current detection y: {yc}")

            # Stop if centered...
            # TODO: Because of moving avg probably we are too far. Might be problem
            if abs(xc) < MAXIMAL_DISTANCE_CENTER and abs(yc) < MAXIMAL_DISTANCE_CENTER:
                self._control.set_lin_velocity(0,0,0)
                self._logger.log("Centered!")
                return True

            # Stop if centering too long...
            if stopwatch.time() > MAX_TIME_SEC:
                self._control.set_lin_velocity(0,0,0)
                return False

            # New speed is based on path distance from center
            up_speed = -ENGINE_POWER * yc
            right_speed = ENGINE_POWER * xc

            self._control.set_lin_velocity(0, right_speed, up_speed)
            #self.go_down(-up_speed * 0.2)

    def go_through_gate(self):
        self._logger.log("go thtough the gate")
        config = self.config['go']
        MAX_ENGINE_POWER = config['max_engine_power']
        GO_TIME = config['go_time_seconds']

        self._control.set_lin_velocity(MAX_ENGINE_POWER)
        sleep(GO_TIME)
        self._control.set_lin_velocity(0)
        self._logger.log("passed through the gate")
        return True


