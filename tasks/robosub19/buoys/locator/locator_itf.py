"""
File contains interface for locator class in buoys
"""
import  abc

class ILocator(metaclass=abc.ABCMeta):
    """
    Interfce for buoys locator
    """
    @abc.abstractmethod
    def get_jiangshi_coordinates(self, image):
        """
        Method for getting cordinates of jiangshi buoy
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_rectangle_coordinates(self, image):
        """
        Method for getting cordinates of whole rectangle buoy
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass
    
    @abc.abstractmethod
    def get_draugr_wall_coordinates(self, image):
        """
        Method for getting cordinates of Draugr wall-buoy
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_aswang_wall_coordinates(self, image):
        """
        Method for getting cordinates of aswang wall-buoy
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass

    @abc.abstractmethod
    def get_vetalas_wall_coordinates(self, image):
        """
        Method for getting cordinates of vetalas wall-buoy
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass