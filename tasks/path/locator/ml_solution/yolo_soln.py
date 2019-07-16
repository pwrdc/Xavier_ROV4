from tasks.path.locator.locator_itf import ILocator
from neural_networks.yolo_model_proxy import YoloModelProxy
from neural_networks.nn_manager import NNManager

class YoloPathLocator(ILocator):
    def __init__(self, threshold=0.5):
        self.model = None

    def get_path_cordinates(self, image):
        """
        Method for geting cordinates of path
        @param: image captured from camera, standard openCV type
        :return: dictionary with x,y cordinates of path in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.
            example: {"x":0.4, "y":0.5}
        """
        if self.model is None or not self.model.is_active():
            self.model = NNManager.get_yolo_model("path")

        self.model.predict(image).to_dict()

        prediction = self.model.predict(image)

        return {
            "x": prediction.xc,
            "y": prediction.yc
        }


    def get_rotation_angle(self, image):
        """
        Return an angle of rotation to turn around to be compatible of vector indicated by path
        Vector of ROV indicates straight ahead
        @param: image captured from camera, standard openCV type
        :return: one int value in range of (-180,180], which is an angle of rotation
            where 0 : in front of, -90 : left, 90 : right etc.
        """
        
        # TODO: Make real functionality
        return 0
        