"""
File contains interface for locator class in gate
"""
import  abc

class ILocator(metaclass=abc.ABCMeta):
    """
    Interfce for gate locator
    """
    @abc.abstractmethod
    def get_gate_cordinates(self, image):
        """
        Method for geting cordinates of gate
        @param: image captured from camera, standard openCV type
        :return: boundin box: dictionary with x,y cordinates of centre of bounding box in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.

            and h,w (hight, width of bounding box)
            values are floats in the range [0, 1], where 1 - means - height of whole picture, and 0.5 - half of height
            example: {"x":0.4, "y":0.5, "h":0.5, "w":0.2}
        """
        pass
