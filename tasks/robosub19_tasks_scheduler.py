from tasks.task_executor_itf import ITaskExecutor
from definitions import TASKS   

from tasks.robosub19.gate.task_executor.gate_task_executor import GateTaskExecutor as GateExecutor
from tasks.robosub19.gate.task_executor.gate_mrn import GateMrn
from tasks.robosub19.path.task_executor.path_task_executor import PathTaskExecutor
from tasks.robosub19.path.task_executor.opencv_task_executor import PathTaskExecutor as CVPathTaskExecutor
from tasks.robosub19.buoys.buoys_task_executor import BuoysTaskExecutor
from tasks.robosub19.buoys.buyos_mrn import BuoysMrn
from tasks.robosub19.auto_movements.prequalification import Prequalification
from tasks.robosub19.casket.task_executor import CasketTaskExecutor
from tasks.robosub19.garlic.task_executor import GarlicTaskExecutor
from tasks.robosub19.garlic_drop.drop_task_executor import DropTaskExecutor

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
        if TASKS.GATE:
            gate_executor = GateExecutor(self.control_dict['movements'], self.sensors_dict,
                                         self.cameras_dict, self.logger)
            gate_executor.run()
        elif TASKS.GATE_MRN:
            path_executor = GateMrn(self.control_dict['movements'], self.sensors_dict,
                                            self.cameras_dict, self.logger)
            path_executor.run()

        if TASKS.PATH:
            path_executor = PathTaskExecutor(self.control_dict['movements'], self.sensors_dict,
                                                self.cameras_dict, self.logger)
            path_executor.run()
        elif TASKS.PATH_MRN:
            pass
            # TODO path mrn executor

        if TASKS.BUOYS:
            buyos_mrn = BuoysTaskExecutor(self.control_dict, self.sensors_dict,
                                 self.cameras_dict, self.logger)
            buyos_mrn.run()

        elif TASKS.BUOYS_MRN:
            buyos_mrn = BuoysMrn(self.control_dict, self.sensors_dict,
                                 self.cameras_dict, self.logger)
            buyos_mrn.run()

        if TASKS.GARLIC_DROP:
            drop_executor = DropTaskExecutor(self.control_dict, self.sensors_dict,
                                             self.cameras_dict, self.logger)
            drop_executor.run()


        #garlic_executor = GarlicTaskExecutor(self.control_dict, self.sensors_dict,
        #                                     self.cameras_dict, self.logger)
        #garlic_executor.run()

        if TASKS.CASKET:
            casket_executor = CasketTaskExecutor(self.control_dict, self.sensors_dict,
                                                 self.cameras_dict, self.logger)
            casket_executor.run()

        self.logger.log("finish all tasks")