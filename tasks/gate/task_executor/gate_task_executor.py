from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.gate.locator.ml_solution.yolo_soln import YoloGateLocator
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from configs.config import get_config
from time import sleep
import cv2

from utils.python_rest_subtask import PythonRESTSubtask

class GateTaskExecutor(ITaskExecutor):
    def __init__(self, contorl_dict: Movements, sensors_dict, cameras_dict: Cameras, main_logger):
        self._control = contorl_dict
        self._front_camera = cameras_dict['front_cam1']
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._logger = main_logger
        self.config = get_config("tasks")['gate_task']
        self.img_server = PythonRESTSubtask("utils/img_server.py", 6669)
        self.img_server.start()
        # For which path we are taking angle. For each path, rotation 
        # angle might be set differently in config.json
        self.number = 0

    def run(self):
        self._logger.log("Start gate task executor")
        self._control.pid_turn_on()
        self._control.pid_yaw_turn_on()
        self._logger.log("gate: turn on depth and yaw contorl")

        if not self.find_gate():
            self._logger.log("gate: if not self.find_gate()")
            return 0

        if not self.center_on_gate():
            self._logger.log("gate: if not self.center_on_gate():")
            return 0

        if not self.go_through_gate():
            self._logger.log("gate: not self.go_through_gate()")
            return 0

        return 1

    def post_image(self, img, bounding_box = None):
        if bounding_box is not None:
            self.img_server.post("set_img", img, unpickle_result=False)
            bb = bounding_box.denormalize(img.shape[1], img.shape[0])
            p1 = (int(bb.x1), int(bb.y1))
            p2 = (int(bb.x2), int(bb.y2))
            img = cv2.rectangle(img, p1, p2, (255,0,255))
        self._logger.log("img posted")
        self.img_server.post("set_img", img, unpickle_result=False)

    def find_gate(self):
        self._logger.log("finding the gate")
        config = self.config['search']
        MAX_ANG_SPEED = config['max_ang_speed']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']
        MAX_TIME_SEC = config['max_time_sec']

        self._control.set_ang_velocity(0,0, MAX_ANG_SPEED)

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("searted find gate loop")

        while(True):
            img = self._front_camera.get_image()
            bounding_box = YoloGateLocator().get_gate_bounding_box(img)
            self.post_image(img, bounding_box)

            confidence = 0

            if bounding_box is not None:
                confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT)
                self._bounding_box.mvg_avg(bounding_box, 0.5, True)
                self._logger.log("gate: somoething detected")
            else:
                confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)

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
            img = self._front_camera.get_image()
            bounding_box = YoloGateLocator().get_gate_bounding_box(img)
            self.post_image(img, bounding_box)

            # Try again if yolo did not return a box
            # TODO: Maybe go back?
            if bounding_box is None:
                continue

            self._bounding_box.mvg_avg(bounding_box, MOVING_AVERAGE_DISCOUNT, True)
        
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
            up_speed = ENGINE_POWER * self._bounding_box.yc
            right_speed = ENGINE_POWER * self._bounding_box.xc

            self._control.set_lin_velocity(0, right_speed, up_speed)

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


