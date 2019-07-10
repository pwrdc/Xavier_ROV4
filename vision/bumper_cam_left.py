import cv2
from vision.base_camera_itf import IBaseCamera

class BumperCamLeft(IBaseCamera):
    '''
    Camera positioned at the left bumper
    '''
    def __init__(self, mode="HARDWARE", simulation_ref=None):
        """
        :param: hardware - decide if camera get video from simulation or real camera
            two option: "HARDWARE" or "SIMULATION"
        """
        pass

    def get_image(self):
        '''
        :return: the latest image captured from camera, standard openCV type
        '''
        pass

