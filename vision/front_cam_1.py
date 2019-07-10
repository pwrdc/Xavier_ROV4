import cv2
from vision.base_camera_itf import IBaseCamera
from definitions import CAMERAS

class FrontCamera1(IBaseCamera):
    '''
    Camera positioned at the front of AUV
    '''
    def __init__(self, mode="HARDWARE", simulation_ref=None):
        """
        :param: hardware - decide if camera get video from simulation or real camera
            two option: "HARDWARE" or "SIMULATION" or "ROV3"
        """
        self.mode = mode
        self.simulation_ref = simulation_ref
        self.get_img_ref = self.get_hardware_image
        if mode == 'SIMULATION':
            self.get_img_ref = self.get_simulation_image
        elif mode == 'HARDWARE':
            self.cap = cv2.VideoCapture(CAMERAS.FRONT_CAM_1_NR)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1);
        elif mode == "ROV3":
            self.cap = cv2.VideoCapture(CAMERAS.XIAOMI_CAMERA_SOURCE)
            self.frame_width = int(self.cap.get(3))
            self.frame_height = int(self.cap.get(4))


    def update_xiaomi_camera(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.cap.isOpened():
                (self.status, self.frame) = self.cap.read()

    def get_image(self):
        '''
        :return: the latest image capd from camera, standard openCV type
        '''
        _, frame = self.cap.read()
        return frame 

    def get_simulation_image(self):
        self.simulation_ref.set_camera_focus(0)
        return self.simulation_ref.get_image()

    def get_hardware_image(self):
        _, frame = self.cap.read()
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
if __name__ == '__main__':
    cam = FrontCamera1(mode = "ROV3")

    while True:
        frame = cam.get_image()
        cv2.imshow('frame', frame)
