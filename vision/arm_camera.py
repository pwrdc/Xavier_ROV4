from vision.base_camera_itf import IBaseCamera

class GrasperCamera(IBaseCamera):
    '''
    Camera positioned at the front of AUV
    '''
    def get_image(self):
        '''
        :return: image captured from camera, standard openCV type
        '''
        pass
