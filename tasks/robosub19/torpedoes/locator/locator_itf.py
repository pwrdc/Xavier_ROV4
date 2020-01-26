"""
File contains interface for locator class in torpedoes task
"""
import  abc

class ILocator(metaclass=abc.ABCMeta):
    """
    Interfce for torpedoes locator
    """
    @abc.abstractmethod
    def get_general_coordinates(self, image):
        """
        Method for getting general cordinates of torpedo buoy
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_heart_coordinates(self, image):
        """
        Method for getting general cordinates of heart
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_ellipse_coordinates(self, image):
        """
        Method for getting cordinates of ellipse
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_lever_coordinates(self, image):
        """
        Method for getting cordinates of lever
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.

            and h,w (hight, width of bounding box)
            values are floats in the range [0, 1], where 1 - means - height of whole picture, and 0.5 - half of height
            example: {"x":0.4, "y":0.5, "h":0.5, "w":0.2}
        """
        pass