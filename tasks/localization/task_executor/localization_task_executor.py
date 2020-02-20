from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.localization.locator.ml_solution.yolo_soln import YoloGateLocator
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from utils.location_calculator import location_calculator
from configs.config import get_config
from utils.python_rest_subtask import PythonRESTSubtask
from tasks.localization.locator.cv_locator import FlareDetector
from time import sleep
import cv2
import math as m
import numpy as np


class GateTaskExecutor(ITaskExecutor):

    ###Initialization###
    def __init__(self, control_dict, sensors_dict, cameras_dict: Cameras, main_logger):
        self._control = control_dict
        self._sensors = sensors_dict
        self._front_camera = cameras_dict['front_cam1']
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._logger = main_logger
        self.movements = control_dict['movements']
        self.config = get_config('tasks')['localization']
        self.img_server = PythonRESTSubtask("utils/img_server.py", 6669)
        self.img_server.start()
        self.confidence = 0
        self.ahrs = self._sensors['ahrs']

        self.flare_position = None

    ###Start the gate algorithm###
    def run(self):
        MAX_TIME_SEC = self.config['search']['max_time_sec']
        objects_position = get_config('objects_position')
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

        # przybliżone położenie flar
        flare_positions = [objects_position['flare1'], objects_position['flare2']]

        # przybliżone położenie łodzi z poprzedniego zadania
        # TODO: poprzednie zadanie pobierać przez argument wejściowy
        auv_position = objects_position['acquisition']

        self.rotate_to_flare(flare_positions, auv_position)

        if not self.find_flare():
            self._logger.log("LocalizationTE: finding flare in progress")

        # TODO: kontynuować tylko jeśli find_flare() zwróci True
        while True:
            # obróć się tak, aby flara była na środku obrazu
            if not self.center_on_flare():
                self._logger.log("LocalizationTE: centering on flare in progress")

            # płyń prosto przez określony czas / określony dystans (do ustalenia)
            if not self.go_to_flare():
                self._logger.log("LocalizationTE: going towards flare")

            if self.is_flare_knocked():
                return True

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

    def find_flare(self):
        # TODO: obsługa wykrycia dwóch flar
        #   obsługa nie wykrycia flary po pełnym obrocie

        self._logger.log("finding the flare")
        config = self.config['search']

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("started find gate loop")

        while stopwatch < config['max_time_sec']:
            # sprawdza kilka razy, dla pewności
            #   (no i żeby confidence się zgadzało, bo bez tego to nawet jak raz wykryje, to nie przejdzie -
            #       - przy moving_avg_discount=0.9 musi wykryć 10 razy z rzędu
            for i in range(config['number_of_samples']):
                img = self._front_camera.get_image()
                if self.is_this_flare(img):
                    return True
            self.movements.rotate_angle(0, 0, config['rotation_angle'])

        self._logger.log("flare not found")
        return False

    def is_this_flare(self, img):
        config = self.config['search']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']

        bounding_box = YoloGateLocator().get_flare_bounding_box(img)
        #self.post_image(img, bounding_box)

        if bounding_box is not None:
            self.confidence = mvg_avg(1, self.confidence, MOVING_AVERAGE_DISCOUNT)
            self._bounding_box.mvg_avg(bounding_box, 0.5, True)
            self._logger.log("is_this_flare: something detected")
        else:
            self.confidence = mvg_avg(0, self.confidence, MOVING_AVERAGE_DISCOUNT)

        if self.confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this_flare: flare found")
            return True

    ###Dive###
    def dive(self):
        depth = self.config['max_depth']
        self._logger.log("Dive: setting depth")
        self._control.pid_set_depth(depth)
        self._logger.log("Dive: holding depth")
        self._control.pid_hold_depth()

    # obróć się w stronę bliższej żółtej flary
    #   kąt obrotu obliczany na podstawie wcześniej określonego przybliżonego położenia flar
    #   i przybliżonego położenia łodzi z poprzedniego zadania
    def rotate_to_flare(self, flare_positions, auv_position):
        distances = []
        for flare_position in flare_positions:
            distances.append(
                m.sqrt((flare_position["x"] - auv_position["x"]) ** 2 + (flare_position["y"] - auv_position["y"]) ** 2))
        # pozycja najbliższej flary
        flare_position = flare_positions[distances.index(min(distances))]
        angle = m.atan2(flare_position['y'] - auv_position['y'],
                        flare_position['x'] - auv_position['x']) - self.ahrs.get_yaw()
        self.movements.rotate_angle(0, 0, angle)

    def center_on_flare(self):
        # TODO: ograniczenie czasowe
        config = self.config['centering']
        flare_size = get_config("objects_size")["localization"]["flare"]["height"]
        MAX_CENTER_ANGLE = config['max_center_angle']
        while True:
            img = self._front_camera.get_image()
            b_box, color = FlareDetector().findMiddlePoint(img)
            self.flare_position = location_calculator(b_box, flare_size, "height")
            angle = -m.degrees(m.atan2(self.flare_position['x'], self.flare_position['distance']))
            if abs(angle) <= MAX_CENTER_ANGLE:
                return True
            self.movements.rotate_angle(0, 0, angle)

    def go_to_flare(self):
        """
        travels distance to flare + a little more to knock it
        """
        self.movements.move_distance(self.flare_position['distance'] + self.config['go']['distance_to_add_m'], 0, 0)
        return True

    def is_pinger_louder(self):
        pass

    def is_flare_knocked(self):
        """
        if doesn't see the flare, then it's knocked
        """
        img = self._front_camera.get_image()
        if YoloGateLocator().get_flare_bounding_box(img) is None:
            return True
