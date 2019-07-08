from tasks.task_executor_itf import ITaskExecutor

from tasks.gate.task_executor import TaskExecutor as GateExecutor
from tasks.path.task_executor import TaskExecutor as PathExecutor


class TaskSchedululer(ITaskExecutor):

    def __init__(self, movement_object, cameras_dict):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
        """
        self.movement_object = movement_object
        self.cameras_dict = cameras_dict

    def run(self):
        """
        This method is started by main object.
        """
        pass