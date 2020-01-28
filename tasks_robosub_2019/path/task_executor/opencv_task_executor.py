from tasks.path.locator.cv_solution.locator import Locator as CVLocator
from tasks.task_executor_itf import ITaskExecutor, Cameras

import time

class PathTaskExecutor(ITaskExecutor):
    def __init__(self, contorl_dict, sensors_dict, cameras_dict: Cameras, main_logger):
        self._logger = main_logger
        self._locator = CVLocator()
        self._bottom_cam = cameras_dict['bottom_cam']

    def run(self):
        self._logger.log("path open cv executor ")
        self.centre()
        self.rotate()

    def centre(self):
        for _ in range(100): # while True:
            img = self._bottom_cam.get_image()
            coordinates = self._locator.get_path_cordinates(img)
            self._logger.log("coordinates of path: "+str(coordinates))
            time.sleep(0.05)

    def rotate(self):
        for _ in range(5):
            img = self._bottom_cam.get_image()
            angle = self._locator.get_rotation_angle(img)
            self._logger.log("rotation angle:"+str(angle))
            time.sleep(0.05)
