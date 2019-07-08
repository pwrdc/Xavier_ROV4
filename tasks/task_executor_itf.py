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
    def __init__(self, movement_object, cameras_dict):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
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
