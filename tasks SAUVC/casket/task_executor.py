from tasks.task_executor_itf import ITaskExecutor
from tasks.casket.locator.cv_solution.locator import  Locator as CVLocator

import time

class CasketTaskExecutor(ITaskExecutor):
    def __init__(self, control_dict, sensors_dict, cameras_dict, main_logger):
        """
        @param: movement_object is an object of Movements Class
            keywords: movements; torpedoes; manipulator;
        @param: sensors_dict is a dictionary of references to sensors objects
            keywords: ahrs; depth; hydrophones; distance;
        @param: cameras_dict is a dictionary of references to cameras objects
            keywords: arm_camera; bottom_camera; front_cam1; bumper_cam_right; bumper_cam_left;
            for cameras objects look at /vision/front_cam_1.py
        @param: main_logger is a reference to logger of main thread
        """
        self.control_dict = control_dict
        self.sensors_dict = sensors_dict
        self.movements = control_dict['movements']
        self._logger = main_logger
        self._bottom_cam = cameras_dict['bottom_camera']

    def run(self):
        self.grab_vampire()

    def grab_vampire(self):
        locator = CVLocator()
        while True:
            img = self._bottom_cam.get_image()
            self._logger.log("got image")
            vampire_coordinates = locator.get_vampire_coordinates(img)
            self._logger.log("got coordinates: "+str(vampire_coordinates))
            time.sleep(0.02)
