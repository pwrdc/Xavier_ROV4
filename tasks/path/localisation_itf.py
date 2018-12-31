"""
File contains interface for localization class in path
"""
import  abc

class ILocalisation(metaclass=abc.ABCMeta):
    """
    Interfce for path localisation
    """
    @abc.abstractmethod
    def get_path_cordinates(self):
        """
        Method for geting cordinates of path
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        pass
    @abc.abstractmethod
    def get_path_box(self):
        """
        Method for geting width and height of box contains path
        Box shoud be as small as possible
        :return: dictionary with width, height of path in relative to centre of camera (0,0)
            values are floats in the range (0, 1], which are ratio of box's size to image size,
            example:
            {"width":0.4, "hight":0.25} - when image is 256, 256 then box dimensions are: 102, 64
        """
        pass
