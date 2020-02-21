from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.localization.locator.ml_solution.yolo_soln import YoloFlareLocator
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
        self.hydrophones = self._sensors['hydrophones']

        self.flare_position = None

    ###Start the gate algorithm###
    def run(self):
        self._logger.log("Localization task executor started")
        self._control.pid_turn_on()

        self.dive()

        self.center_on_pinger()

        if not self.find_flare():
            self._logger.log("couldn't find flare - task failed, aborting")
            return False

        while True:
            if not self.center_on_flare():
                self._logger.log("couldn't center on flare - task failed, aborting")
                return False

            # if traveled whole distance to flare, checked if flare knocked
            # else repeat loop
            if self.go_to_flare():
                if self.is_flare_knocked():
                    self._logger.log("knocked flare - task finished successfully")
                    return True

    def find_flare(self):
        # TODO: obsługa wykrycia dwóch flar

        self._logger.log("finding the flare")
        config = self.config['search']

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("started find flare loop")

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

        bounding_box = YoloFlareLocator().get_flare_bounding_box(img)
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

    def dive(self):
        depth = self.config['max_depth']
        self._logger.log("Dive: setting depth")
        self._control.pid_set_depth(depth)
        self._logger.log("Dive: holding depth")
        self._control.pid_hold_depth()

    def center_on_flare(self):
        """
        rotates in vertical axis so flare is in the middle of an image
        TODO: obsługa dwóch flar
        """
        config = self.config['centering']
        flare_size = get_config("objects_size")["localization"]["flare"]["height"]

        MAX_CENTER_ANGLE_DEG = config['max_center_angle_deg']
        MAX_TIME_SEC = config['max_time_sec']

        stopwatch = Stopwatch()
        stopwatch.start()

        while stopwatch <= MAX_TIME_SEC:
            img = self._front_camera.get_image()
            b_box, color = FlareDetector().findMiddlePoint(img)
            self.flare_position = location_calculator(b_box, flare_size, "height")
            angle = -m.degrees(m.atan2(self.flare_position['x'], self.flare_position['distance']))
            if abs(angle) <= MAX_CENTER_ANGLE_DEG:
                self._logger.log("centered on flare successfully")
                return True
            self.movements.rotate_angle(0, 0, angle)
        self._logger.log("couldn't center on flare")
        return False

    def go_to_flare(self):
        """
        moves distance to flare + a little more to knock it
        :return: True - if managed to move distance in time
                 False - if didn't manage to move distance in time
        """
        config = self.config['go']
        MAX_TIME_SEC = config['max_time_sec']

        stopwatch = Stopwatch()
        stopwatch.start()

        self.movements.move_distance(self.flare_position['distance'] + self.config['go']['distance_to_add_m'], 0, 0)

        if stopwatch <= MAX_TIME_SEC:
            self._logger.log("go_to_flare - traveled whole distance")
            return True
        else:
            self._logger.log("go_to_flare - didn't travel whole distance")
            return False

    def center_on_pinger(self):
        """
        rotates in vertical axis so pinger signal is in front
        """
        config = self.config['centering']
        MAX_TIME_SEC = config['max_time_sec']
        MAX_CENTER_ANGLE_DEG = config['max_center_angle_deg']

        self._logger.log("centering on pinger")
        stopwatch = Stopwatch()
        stopwatch.start()

        while stopwatch < MAX_TIME_SEC:
            angle = self.hydrophones.get_angle()
            if angle is None:
                self._logger.log("no signal from hydrophones - locating pinger failed")
                return False
            if abs(angle) < MAX_CENTER_ANGLE_DEG:
                self._logger.log("centered on pinger successfully")
                return True
            self.movements.rotate_angle(0, 0, angle)
        self._logger.log("couldn't ceneter on pinger")
        return False

    def is_flare_knocked(self):
        """
        if doesn't see the flare, then it's knocked
        """
        img = self._front_camera.get_image()
        if YoloFlareLocator().get_flare_bounding_box(img) is None:
            self._logger.log("can't see flare - flare knocked")
            return True
        self._logger.log("flare still visible - flare not knocked")
        return False

    def post_image(self, img, bounding_box=None):
        """
        wrzuca obraz wykrytej flary, nic ważnego
        """
        if bounding_box is not None:
            self.img_server.post("set_img", img, unpickle_result=False)
            bb = bounding_box.denormalize(img.shape[1], img.shape[0])
            p1 = (int(bb.x1), int(bb.y1))
            p2 = (int(bb.x2), int(bb.y2))
            img = cv2.rectangle(img, p1, p2, (255,0,255))
        self._logger.log("img posted")
        self.img_server.post("set_img", img, unpickle_result=False)