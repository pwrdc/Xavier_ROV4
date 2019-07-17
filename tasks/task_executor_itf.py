"""
File contains interface for task executor
"""
import  abc

class ITaskExecutor(metaclass=abc.ABCMeta):
    """
    Interfce for trainer class
    All tasks executon algorithm are implemented in TaskExecutor class in task location
    e.g. TaskExecutor in tasks/path/task_executor.py

    TaskExecutor inherit from this interface
    Every sub-algorithm also implement his interface
    """
    @abc.abstractmethod
    def __init__(self, contorl_dict, sensors_dict, cameras_dict, main_logger):
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
        pass

    @abc.abstractmethod
    def run(self):
        """
        This method is started by precedent class.
        Algorithm for task solution should be implemented here
        :return: 0 in case of failure, 1 in case of success
        """
        pass
