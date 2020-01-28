"""
File contains interface for locator class in casket task
"""
import  abc

class ILocator(metaclass=abc.ABCMeta):
    """
    Interfce for casket task locator
    """
    @abc.abstractmethod
    def get_open_coffin_coordinates(self, image):
        """
        Method for getting general cordinates of open coffin
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_closed_coffin_coordinates(self, image):
        """
        Method for getting general cordinates of closed coffin
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_coffin_lock_coordinates(self, image):
        """
        Method for getting general cordinates of coffin lock
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_vampire_coordinates(self, image):
        """
        Method for getting general cordinates of vampire (purple pipe)
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_vampire_angle(self, image):
        """
        Return an angle of rotation to turn so that the angle between the violet tube's axis and the ROV vector is 0
        Vector of ROV indicates straight ahead
        @param: image captured from camera, standard openCV type
        :return: one int value in range of (-180,180], which is an angle of rotation
            where 0 : in front of, -90 : left, 90 : right etc.
        """
        pass
