"""
File contains interface for navigation class in path
"""
import  abc

class INavigation(metaclass=abc.ABCMeta):
    """
    Interfce for algorithm for tasks
    """
    @abc.abstractmethod
    def get_rotation_angle(self):
        """
        Return an angle of rotation to turn around to be compatible of vector indicated by path
        Vector of ROV indicates straight ahead
        :return: one int value in range of (-180,180], which is an angle of rotation
            where 0 : in front of, -90 : left, 90 : right etc.
        """
        pass
