from tasks.task_executor_itf import ITaskExecutor

from tasks.gate.task_executor.gate_task_executor import GateTaskExecutor as GateExecutor
from tasks.path.task_executor.path_task_executor import PathTaskExecutor
from tasks.path.task_executor.opencv_task_executor import PathTaskExecutor as CVPathTaskExecutor
from tasks.auto_movements.prequalification import Prequalification
from tasks.casket.task_executor import CasketTaskExecutor
from tasks.garlic.task_executor import GarlicTaskExecutor

class TaskSchedululer(ITaskExecutor):

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
        self.cameras_dict = cameras_dict
        self.logger = main_logger

    def run(self):
        """
        This method is started by main object.
        """
        self.logger.log("Task scheduler is running")
        #prequalification = Prequalification(self.control_dict, self.sensors_dict,
        #                                    self.cameras_dict, self.logger)
        #prequalification.run()

        #gate_executor = GateExecutor(self.control_dict['movements'], self.sensors_dict,
        #                             self.cameras_dict, self.logger)
        #gate_executor.run()

        #path_executor = PathTaskExecutor(self.control_dict['movements'], self.sensors_dict,
        #                                 self.cameras_dict, self.logger)
        #path_executor.run()

        garlic_executor = GarlicTaskExecutor(self.control_dict, self.sensors_dict,
                                             self.cameras_dict, self.logger)
        garlic_executor.run()

        #casket_executor = CasketTaskExecutor(self.control_dict, self.sensors_dict,
        #                                     self.cameras_dict, self.logger)
        #casket_executor.run()
