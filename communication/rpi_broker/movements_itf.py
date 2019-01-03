"""
Module includes IMovements
"""
import  abc

class IMovements(metaclass=abc.ABCMeta):
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    @abc.abstractmethod
    def set_lin_velocity(self, front, right, up):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """
        pass

    @abc.abstractmethod
    def set_ang_velocity(self, roll, pitch, yaw):
        """
        Set angular velocity as 100% of engines power
        @param: roll int in range [-100, 100], case negative - reverse direction
        @param: pitch int in range [-100, 100], case negative - reverse direction
        @param: yaw int in range [-100,100], case negative - reverse direction
        """
        pass

    @abc.abstractmethod
    def move_distance(self, front, right, up):
        """
        Make precise linear movement, valeues in meters
        @param: front float in range [-10, 10], case negative value move back
        @param: right float in range [-10, 10], case negative value move down
        @param: up float in range [-10,10], case negative value move down

        Not shure if it is going to work correctly
        """
        pass

    @abc.abstractmethod
    def rotate_angle(self, roll, pitch, yaw):
        """
        Make precise angular movement
        @param: roll float in range [-360, 360], case negative - reverse direction
        @param: pitch float in range [-360, 360], case negative - reverse direction
        @param: yaw flaot in range [-360, 360], case negative - reverse direction
        """
        pass
