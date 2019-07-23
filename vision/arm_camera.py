import cv2
from vision.base_camera_itf import IBaseCamera
from definitions import CAMERAS


class ArmCamera(IBaseCamera):
    '''
    Camera positioned at the front of AUV
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
            pass
        elif mode == 'ROV4':
            self.cap = cv2.VideoCapture(CAMERAS.ARM_CAMERA_NR)
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
        self.simulation_ref.set_camera_focus(1)
        return self.simulation_ref.get_image()

    def get_hardware_image(self):
        _, frame = self.cap.read()
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def get_xiaomi_image(self):
        raise Exception("Arm camera not implemented in ROV3")
