from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.gate.locator.ml_solution.yolo_soln import YoloGateLocator
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from utils.config import get_config
from time import sleep

class GateTaskExecutor(ITaskExecutor):
    def __init__(self, contorl_dict: Movements, sensors_dict, cameras_dict: Cameras, main_logger):
        self._control = contorl_dict
        self._front_camera = cameras_dict['front_cam1']
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._config = get_config()['gate_task']
        # For which path we are taking angle. For each path, rotation 
        # angle might be set differently in config.json
        self.number = 0

    def run(self):
        if not self.find_gate():
            return 0

        if not self.center_on_gate():
            return 0

        if not self.rotate():
            return 0

        return 1

    def find_gate(self):
        config = self.config['search']
        MAX_ANG_SPEED = config['max_ang_speed']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']
        MAX_TIME_SEC = config['max_time_sec']

        self._control.set_ang_velocity(0,0, MAX_ANG_SPEED)

        stopwatch = Stopwatch()
        stopwatch.start() 

        while(True):
            img = self._bottom_camera.get_image()
            bounding_box = YoloGateLocator().get_gate_bounding_box(img)

            confidence = 0

            if bounding_box is not None:
                confidence = mvg_avg(1, MOVING_AVERAGE_DISCOUNT)
                self._bounding_box.mvg_avg(bounding_box, 0.5, True)
            else:
                confidence = mvg_avg(0, MOVING_AVERAGE_DISCOUNT)

            # Stop and report sucess if we are sure we found a path!
            if confidence > CONFIDENCE_THRESHOLD:
                self._control.set_ang_velocity(0,0,0)
                return True 

            # Abort if we are running far away...
            if stopwatch.time() > MAX_TIME_SEC:
                self._control.set_ang_velocity(0,0,0)
                return False 

    def center_on_gate(self):
        config = self.config['centering']
        ENGINE_POWER = config['max_engine_power']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        MAXIMAL_DISTANCE_CENTER = config['max_center_distance']
        MAX_TIME_SEC = config['max_time_sec']

        while(True):
            img = _front_camera.get_image()
            bounding_box = YoloGateLocator().get_path_bounding_box(img)

            # Try again if yolo did not return a box
            # TODO: Maybe go back?
            if bounding_box is None:
                continue

            self._bounding_box.mvg_avg(bounding_box, MOVING_AVERAGE_DISCOUNT, True)
        
            stopwatch = Stopwatch()
            stopwatch.start() 

            # Stop if centered...
            # TODO: Because of moving avg probably we are too far. Might be problem
            if abs(self.bounding_box.xc) < MAXIMAL_DISTANCE_CENTER and abs(self.bounding_box.yc) < MAXIMAL_DISTANCE_CENTER:
                self._control.set_lin_velocity(0,0,0)
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
        config = self.config['go']
        MAX_ENGINE_POWER = config['max_engine_power']
        GO_TIME = config['go_time_seconds']

        self._control.set_lin_velocity(MAX_ENGINE_POWER)
        sleep(GO_TIME)
        self._control.set_lin_velocity(0)

        return True


