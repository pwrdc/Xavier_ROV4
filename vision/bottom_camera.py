import cv2
from vision.base_camera_itf import IBaseCamera
from definitions import CAMERAS


class BottomCamera(IBaseCamera):
    '''
    Camera directed to the bottom of AUV
    '''
    def __init__(self, mode="HARDWARE", simulation_ref=None):
        """
        :param: hardware - decide if camera get video from simulation or real camera
            two option: "HARDWARE" or "SIMULATION"
        """
        self.mode = mode
        self.simulation_ref = simulation_ref
        self.get_img_ref = self.get_hardware_image
        if mode == 'SIMULATION':
            self.get_img_ref = self.get_simulation_image
        elif mode == 'HARDWARE':
            self.cap = cv2.VideoCapture(CAMERAS.BOTTOM_CAMERA_NR)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        elif mode == "ROV3":
            self.get_img_ref = self.get_xiaomi_image

    def get_image(self):
        '''
        :return: the latest image captured from camera, standard openCV frame
        '''
        return self.get_img_ref()

    def get_simulation_image(self):
        self.simulation_ref.set_camera_focus(CAMERAS.SIM_BOTTOM_CAM_ID)
        return self.simulation_ref.get_image()

    def get_hardware_image(self):
        _, frame = self.cap.read()
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def get_xiaomi_image(self):
        raise Exception("Bottom camera not implemented in ROV3")
