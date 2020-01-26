#import path_detector # Zawislak library
from tasks.path.locator.locator_itf import ILocator


class Locator(ILocator):
    def __init__(self):
        self.path = path_detector.Path()
        self.path.setlow_thresh(1, 2, 3)
        self.path.set_high_thresh(2, 4, 6)
        # first number in tange 0-179, second and third 0-255

    def get_path_cordinates(self, image):
        """
        Method for geting cordinates of path
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        return self.path.get_intersection_coordinates(image)


    def get_rotation_angle(self, image):
        """
        Return an angle of rotation to turn around to be compatible of vector indicated by path
        Vector of ROV indicates straight ahead
        @param: image captured from camera, standard openCV type
        :return: one int value in range of (-180,180], which is an angle of rotation
            where 0 : in front of, -90 : left, 90 : right etc.
        """
        return self.path.get_rotation_angle(self, image)
    
