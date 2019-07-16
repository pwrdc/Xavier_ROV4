from tasks.gate.locator.locator_itf import ILocator
from neural_networks.yolo_model_proxy import YoloModelProxy
from neural_networks.nn_manager import NNManager

class YoloGateLocator(ILocator):
    def __init__(self, threshold=0.5):
        self.model: YoloModelProxy = None

    def get_gate_cordinates(self, image):
        """
        Method for geting cordinates of gate
        @param: image captured from camera, standard openCV type
        :return: boundin box: dictionary with x,y cordinates of centre of bounding box in relative to centre of camera (0,0)
            values are floats in the range [-1, 1], where -1 is max left of max down cordinate,
            0 is centre, 0.5 is halfway between 0 anf max right or up etc.

            and h,w (hight, width of bounding box)
            values are floats in the range [0, 1], where 1 - means - height of all picture, and 0.5 - half of height
            example: {"x":0.4, "y":0.5, "h":0.5, "w":0.2}
        """
        if self.model is None or not self.model.is_active():
            self.model = NNManager.get_yolo_model("gate")

        self.model.predict(image).to_dict()
        
        