from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.gate.locator.ml_solution.yolo_soln import YoloGateLocator
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from configs.config import get_config
from time import sleep
import cv2

class GateTaskExecutor(ITaskExecutor):

    ###Initialization###
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


    ###Start the gate algorithm###
    def run(self):
        MAX_TIME_SEC = self.config['max_time_sec'] #w configu trzeba zmienic bo na razie jest do samego gate
        self._logger.log("Gate task executor started")
        self._control.pid_turn_on()

        stopwatch = Stopwatch()
        stopwatch.start()

        if stopwatch >= MAX_TIME_SEC:
            self._logger.log("TIME EXPIRED GATE NOT FOUND")
            self._control.set_ang_velocity(0, 0, 0)

        if not self.dive():
            self._logger.log("GateTE: diving in progress")

        if not self.find_gate():
            self._logger.log("GateTE: finding the gate in progress")

        if not self.center_on_gate:
            self._logger.log("GateTE: centering on the gate in progress")

        if not self.go_trough_gate():
            self._logger.log("GateTE: going through the gate")

#Przycina obraz, zostaje sam bbox
    def post_image(self, img, bounding_box = None):
        if bounding_box is not None:
            self.img_server.post("set_img", img, unpickle_result=False)
            bb = bounding_box.denormalize(img.shape[1], img.shape[0])
            p1 = (int(bb.x1), int(bb.y1))
            p2 = (int(bb.x2), int(bb.y2))
            img = cv2.rectangle(img, p1, p2, (255,0,255))
        self._logger.log("img posted")
        self.img_server.post("set_img", img, unpickle_result=False)

    ###Find gate###
    def find_gate(self):
        self._logger.log("finding the gate")
        config = self.config['search']
        MAX_ANG_SPEED = config['max_ang_speed']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']


        self._control.set_ang_velocity(0, 0, MAX_ANG_SPEED)

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("started find gate loop")

        while (True):
            img = self._front_camera.get_image()

            if self.is_this_gate(img):
                self.create_path()    #W trajektorii musi byc uwzgledniona przeszkoda funkcja wyszukujaca przeszkode is_this_obstacle(bounding_box, img):
                self.go_trough_gate()



    ###Dive###
    def dive (self):
        #self._logger.log("Dive: setting depth")
        #self._control.pid_set_depth(depth)
        #Czy trzeba najpierw ustawic glebokosc, czy mozna od razu w hold depth to robic?
        DEPTH = get_config('max_depth')
        self._logger.log("Dive: holding depth")
        self._control.pid_hold_depth(DEPTH)

    def is_this_gate(self, bounding_box, img):

        confidence = 0
        MOVING_AVERAGE_DISCOUNT = get_config('moving_avg_discount')
        CONFIDENCE_THRESHOLD = get_config('confidence_threshold')

        bounding_box = YoloGateLocator().get_gate_bounding_box(img)
        self.post_image(img, bounding_box)

        if bounding_box is not None:
            confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT) #co robi funkcja mvg_avg
            self._bounding_box.mvg_avg(bounding_box, 0.5, True)
            self._logger.log("is_this_gate: somoething detected")
        else:
            confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)

        # Stop and report sucess if we are sure we found a path!
        if confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this_gate: gate found")
            self._control.set_ang_velocity(0, 0, 0)
            return True

    def is_this_obstacle(self, bounding_box, img):

        confidence = 0
        MOVING_AVERAGE_DISCOUNT = get_config('moving_avg_discount')
        CONFIDENCE_THRESHOLD = get_config('confidence_threshold')

        bounding_box = YoloGateLocator().get_obstacle_bounding_box(img)  # Funkcja rozpoznawania przeszkody do dodania
        self.post_image(img, bounding_box)

        if bounding_box is not None:
            confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT)
            self._bounding_box.mvg_avg(bounding_box, 0.5, True)
            self._logger.log("is_this-obstacle: somoething detected")
        else:
            confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)

        # Stop and report sucess if we are sure we found a path!
        if confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this-obstacle: obstacle found")
            self._control.set_ang_velocity(0, 0, 0)
            return True

    def create_path(self):

    ###Swim through the gate###
    def go_trough_gate(self):
        self._logger.log("go thtough the gate")
        config = self.config['go']
        MAX_ENGINE_POWER = config['max_engine_power']
        GO_TIME = config['go_time_seconds']

        self._control.set_lin_velocity(MAX_ENGINE_POWER)
        sleep(GO_TIME)
        self._control.set_lin_velocity(0)
        self._logger.log("passed through the gate")
        return True