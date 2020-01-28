from tasks.navigation.locator.locator_itf import ILocator
from neural_networks.yolo_model_proxy import YoloModelProxy
from neural_networks.nn_manager import NNManager
from structures.bounding_box import BoundingBox
from typing import Optional

class YoloGateLocator(ILocator):
    def get_gate_bounding_box(self, image) -> Optional[BoundingBox]:
        """
        Method for bounding box of gate
        @param: image captured from camera, standard openCV type
        :return: Bounding box containing detected object or None if nothing is detected
        """ 
        return NNManager.get_yolo_model("gate").predict(image)

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
        prediction = self.get_gate_bounding_box(image)

        if prediction is not None:
            return prediction.to_dict()
        else:
            return None
        
        