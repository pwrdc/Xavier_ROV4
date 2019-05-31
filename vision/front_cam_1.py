from vision.base_camera_itf import IBaseCamera

class FrontCamera(IBaseCamera):
    '''
    Camera positioned at the front of AUV
    '''
    def get_image(self):
        '''
        :return: the latest image captured from camera, standard openCV type
        '''
        pass
