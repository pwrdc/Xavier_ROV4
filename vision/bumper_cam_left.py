import cv2
from vision.base_camera_itf import IBaseCamera
from definitions import CAMERAS


class BumperCamLeft(IBaseCamera):
    '''
    Camera positioned at the left bumper
    '''
    def __init__(self, mode="ROV4", simulation_ref=None):
        """
        :param: ROV4 - decide if camera get video from simulation or real camera
            two option: "ROV4" or "SIMULATION"
        """
        self.mode = mode
        self.simulation_ref = simulation_ref
        self.get_img_ref = self.get_hardware_image
        if mode == 'SIMULATION':
            self.get_img_ref = self.get_simulation_image
        elif mode == 'ROV4':
            self.cap = cv2.VideoCapture(CAMERAS.BUMBER_CAMERA_LEFT_NR)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        elif mode == "ROV3":
            self.get_img_ref = self.get_xiaomi_image

    def __del__(self):
        if self.mode == 'ROV4':
            self.cap.release()

    def get_image(self):
        '''
        :return: the latest image captured from camera, standard openCV frame
        '''
        return self.get_img_ref()

    def get_simulation_image(self):
        self.simulation_ref.set_camera_focus(0)
        return self.simulation_ref.get_image()

    def get_hardware_image(self):
        _, frame = self.cap.read()
        return frame

    def get_xiaomi_image(self):
        raise Exception("Bumper camera not implemented in ROV3")
