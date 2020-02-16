from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.navigation.locator.ml_solution.yolo_soln import YoloGateLocator
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from configs.config import get_config
from utils.python_rest_subtask import PythonRESTSubtask
from tasks.flares.locator import cv_locator
from time import sleep
import cv2
import math as m
import numpy as np

class GateTaskExecutor(ITaskExecutor):

    ###Initialization###
    def __init__(self, control_dict: Movements, sensors_dict, cameras_dict: Cameras, main_logger):
        self._control = control_dict
        self._front_camera = cameras_dict['front_cam1']
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._logger = main_logger
        self.config = get_config("tasks")['localization_task']
        self.img_server = PythonRESTSubtask("utils/img_server.py", 6669)
        self.img_server.start()
        self.confidence = 0
        self.detector = cv_locator.FlareDetector

    ###Start the gate algorithm###
    def run(self):
        MAX_TIME_SEC = self.config['max_time_sec'] #w configu trzeba zmienic bo na razie jest do samego gate
        self._logger.log("Localization task executor started")
        self._control.pid_turn_on()

        stopwatch = Stopwatch()
        stopwatch.start()

        if stopwatch >= MAX_TIME_SEC:
            self._logger.log("TIME EXPIRED FLARE NOT FOUND")
            # przerwij zadanie

        # zanurz się na odpowiednią do zadania głębokość
        if not self.dive():
            self._logger.log("LocalizationTE: diving in progress")

        self.rotate_to_flare(flare_positions, auv_position)

        # szukaj flary
        self.find_flare()

        while True:
            # obróć się tak, aby flara była na środku obrazu
            if not self.center_on_flare(flare_position):
                self._logger.log("LocalizationTE: centering on flare in progress")

            # płyń prosto przez określony czas / określony dystans (do ustalenia)
            if not self.go_to_flare():
                self._logger.log("LocalizationTE: going towards flare")

            # sprawdź czy flara została przewrócona (nagle jej nie widać)
            if self.is_flare_knocked():
                # zakończ zadanie
                pass

            # sprawdź głośność pingera i porównaj z poprzednią wartością
            #   jeśli nie jest głośniej, przerwij pętlę i płyń do drugiej flary
            # TODO: no właśnie zmiana na płynięcie do drugiej flary xD
            if not self.is_pinger_louder():
                break

# Przycina obraz, zostaje sam bbox
    def post_image(self, img, bounding_box=None):
        if bounding_box is not None:
            self.img_server.post("set_img", img, unpickle_result=False)
            bb = bounding_box.denormalize(img.shape[1], img.shape[0])
            p1 = (int(bb.x1), int(bb.y1))
            p2 = (int(bb.x2), int(bb.y2))
            img = cv2.rectangle(img, p1, p2, (255,0,255))
        self._logger.log("img posted")
        self.img_server.post("set_img", img, unpickle_result=False)

    ###Find flare###
    # TODO: obsługa wykrycia dwóch flar, obsługa nie wykrycia flary po pełnym obrocie
    def find_flare(self):
        self._logger.log("finding the flare")
        config = self.config['search']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("started find gate loop")

        while True:
            img = self._front_camera.get_image()
            if self.is_this_flare(img):
                return self.detector.findMiddlePoint(img) # no coś tu nie tak
            # obróć się o prawo o ustalony kąt i zatrzymaj

    ###Dive###
    def dive(self):
        depth = get_config('max_depth')
        self._logger.log("Dive: setting depth")
        self._control.pid_set_depth(depth)
        self._logger.log("Dive: holding depth")
        self._control.pid_hold_depth()

    # obróć się w stronę bliższej żółtej flary
    #   kąt obrotu obliczany na podstawie wcześniej określonego przybliżonego położenia flar
    #   i przybliżonego położenia łodzi z poprzedniego zadania
    def rotate_to_flare(self, flare_positions, auv_position):
        pass

    def is_this_flare(self, img):

        MOVING_AVERAGE_DISCOUNT = get_config('moving_avg_discount')
        CONFIDENCE_THRESHOLD = get_config('confidence_threshold')

        bounding_box = YoloGateLocator().get_flare_bounding_box(img)
        self.post_image(img, bounding_box)

        if bounding_box is not None:
            self.confidence = mvg_avg(1, self.confidence, MOVING_AVERAGE_DISCOUNT)
            self._bounding_box.mvg_avg(bounding_box, 0.5, True)
            self._logger.log("is_this_flare: something detected")
        else:
            self.confidence = mvg_avg(0, self.confidence, MOVING_AVERAGE_DISCOUNT)

        # Stop and report success if we are sure we found a path!
        if self.confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this_flare: flare found")
            self._control.set_ang_velocity(0, 0, 0)
            return True

    def center_on_flare(self, flare_position):
        pass

    def go_to_flare(self):
        pass

    def is_pinger_louder(self):
        pass

    def is_flare_knocked(self):
        pass
