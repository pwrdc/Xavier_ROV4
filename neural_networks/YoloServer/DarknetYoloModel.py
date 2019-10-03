from tasks.model_itf import IModel
from structures.bounding_box import BoundingBox
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
import tensorflow as tf
from typing import Optional
import cv2
import numpy as np
from neural_networks.darknet import load_net, load_meta, detect

class DarknetYoloModel:
    """
        Class for using a pretrained Yolo neural network
    """
    def __init__(self, model_path, img_width=416, img_height=416, num_classes=1, threshold=0.5):
        self.model_path = model_path
        self.img_width = img_width
        self.img_height = img_height
        self.num_classes = num_classes
        self.threshold = threshold
        
        self.net = None
        self.meta = None 

    def load(self):
        """
        Takes GPU resources and loads model from file into memory
        :return: None
        """
        cfg_path = f"{self.model_path}/yolo.cfg".encode('UTF-8')
        weights_path = f"{self.model_path}/yolo.weights".encode('UTF-8')
        self._create_meta()
        meta_path = f"{self.model_path}/yolo.data".encode('UTF-8')

        self.net = load_net(cfg_path, weights_path, 0)
        self.meta = load_meta(meta_path)

    def _get_num_classes(self):
        names_path = f"{self.model_path}/yolo.names".encode('UTF-8')
        num_lines = 0

        with open(names_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            if not line.isspace():
                num_lines = num_lines + 1

        return num_lines

    def _create_meta(self):
        with open(f"{self.model_path}/yolo.data", "w") as f:
            f.write(f"classes={self._get_num_classes()}\n")
            f.write("train=fake\n")
            f.write("valid=fake\n")
            f.write(f"names={self.model_path}/yolo.names\n")

    def predict(self, image: np.ndarray) -> [BoundingBox]:
        """
        Finds object on an image
        :param image: np.array representing RGB image with values from 0 to 255
        :return: BoudingBox with relative coordinates (from 0 to 1) of found object. If nothing is found, function
                 returns None
        """
        #image = cv2.resize(image, (self.img_width, self.img_height))
        results = detect(self.net, self.meta, image, thresh=self.threshold, hier_thresh=self.threshold)

        detections = []

        if len(results) == 0:
            return detections

        for result in results:
            detection = result[0].decode('utf-8')
            probability = result[1]
            position = result[2]

            x = position[0] / self.img_width
            y = position[1] / self.img_height
            w = position[2] / self.img_width
            h = position[3] / self.img_height        

            detections.append(BoundingBox(x,y,w,h,probability,detection))

        return detections
