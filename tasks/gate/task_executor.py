"""
File contains interface for task executor
"""
import time
from tasks.task_executor_itf import ITaskExecutor
from tasks.gate.locator.ml_solution.locator import Locator as ML_Locator

class TaskExecutor(ITaskExecutor):
    """
    TaskExecutor inherit from this interface
    Every sub-algorithm also implement his interface
    """
    def __init__(self, movement_object, cameras_dict):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
        """
        self.movement_object = movement_object
        self.main_camera = cameras_dict['front_cam1']
        self.locator = ML_Locator()
            

    def run(self):
        """
        This method is started by precedent class.
        Algorithm for task solution should be implemented here
        :return: 0 in case of failure, 1 in case of success
        """
        while True:
            img = self.main_camera.get_image()
            bounding_box = self.locator.get_gate_cordinates(img)
            if bounding_box["x"]> 0.5:
                self.movement_object.set_lin_velocity(front = 0.3)
                time.sleep(1)
