"""
File contains interface for locator class in garlic drop
"""
import  abc

class ILocator(metaclass=abc.ABCMeta):
    """
    Interfce for garlic drop locator
    """
    @abc.abstractmethod
    def get_drop_zone_coordinates(self, image):
        """
        Method for getting cordinates of garlic drop zone
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
            example: {"x":0.4, "y":0.5}
        """
        pass   

    @abc.abstractmethod
    def get_wolf_coordinates(self, image):
        """
        Method for getting cordinates of wolf
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_bat_coordinates(self, image):
        """
        Method for getting cordinates of bat
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass