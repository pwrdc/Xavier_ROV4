from tasks.task_executor_itf import ITaskExecutor

from tasks.gate.task_executor import TaskExecutor as GateExecutor
from tasks.auto_movements.prequalification import Prequalification


class TaskSchedululer(ITaskExecutor):

    def __init__(self, control_dict, sensors_dict, cameras_dict, main_logger):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
        """
        self.control_dict = control_dict
        self.sensors_dict = sensors_dict
        self.cameras_dict = cameras_dict
        self.logger = main_logger

    def run(self):
        """
        This method is started by main object.
        """
        self.logger.log("Task scheduler is running")
        prequalification = Prequalification(self.control_dict, self.sensors_dict,
                                            self.cameras_dict, self.logger)
        prequalification.run()
