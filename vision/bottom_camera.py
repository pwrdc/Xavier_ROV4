from vision.base_camera_itf import IBaseCamera

class BottomCamera(IBaseCamera):
    '''
    Camera directed to the bottom of AUV
    '''
    def get_image(self):
        '''
        :return: the latest image captured from camera, standard openCV type
        '''
        pass
