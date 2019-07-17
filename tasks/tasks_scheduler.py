from tasks.task_executor_itf import ITaskExecutor

from tasks.gate.task_executor import TaskExecutor as GateExecutor
from tasks.auto_movements.prequalification import Prequalification


class TaskSchedululer(ITaskExecutor):

    def __init__(self, control_dict, sensors_dict, cameras_dict, main_logger):
        """
        @param: movement_object is an object of Movements Class
            keywords: movements; torpedoes;
        @param: sensors_dict is a dictionary of references to sensors objects
            keywords: ahrs; depth; hydrophones; distance;
        @param: cameras_dict is a dictionary of references to cameras objects
            keywords: arm_camera; bottom_camera; front_cam1; bumper_cam_right; bumper_cam_left;
            for cameras objects look at /vision/front_cam_1.py
        @param: main_logger is a reference to logger of main thread
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
