import abc


class IBaseCamera:
    """
    interface for all camera classes
    """

    @abc.abstractmethod
    def get_image(self):
        '''
        :return: the latest image captured from camera, standard openCV type
        '''
        pass
