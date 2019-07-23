import cv2
import numpy as np
import math
from tasks.task_executor_itf import ITaskExecutor
from tasks.garlic.grabber.grab_garlic import GrabGarlic


class GarlicTaskExecutor(ITaskExecutor):
    def __init__(self, control_dict, sensors_dict, cameras_dict, main_logger):
        self.control_dict = control_dict
        self.sensors_dict = sensors_dict
        self.cameras_dict = cameras_dict
        self.main_logger = main_logger

    def run(self):
        self.main_logger.log("run GarlicGrabber")
        grab = GrabGarlic(self.control_dict, self.sensors_dict, self.cameras_dict, self.main_logger)
