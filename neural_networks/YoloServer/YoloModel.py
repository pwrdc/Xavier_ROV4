from tasks.model_itf import IModel
from structures.bounding_box import BoundingBox
import tensorflow as tf
from typing import Optional
import cv2
import numpy as np


class YoloModel:
    """
        Class for using a pretrained Yolo neural network
    """
    def __init__(self, model_path, img_width=416, img_height=416, num_classes=1, input_tensor_name="input:0",
                 prediction_tensor_name="prediction:0", threshold=0.5):
        self.model_path = model_path
        self.img_width = img_width
        self.img_height = img_height
        self.num_classes = num_classes
        self.threshold = threshold

        self.input_tensor_name = input_tensor_name
        self.prediction_tensor_name = prediction_tensor_name

        self.session: Optional[tf.Session] = None
        self.saver = None
        self.inputs = None
        self.predictions = None

    def load(self):
        """
        Takes GPU resources and loads model from file into memory
        :return: None
        """
        self.session = tf.Session()
                
        self.saver = tf.train.import_meta_graph(f"{self.model_path}/model.chkpt.meta")
        
        self.session.run(tf.global_variables_initializer())
        self.session.run(tf.local_variables_initializer())


        self.saver.restore(self.session, f"{self.model_path}/model.chkpt")

        self.inputs = self.session.graph.get_tensor_by_name(self.input_tensor_name)
        self.predictions = self.session.graph.get_tensor_by_name(self.prediction_tensor_name)

    def predict(self, image: np.ndarray) -> BoundingBox:
        """
        Finds object on an image
        :param image: np.array representing RGB image with values from 0 to 255
        :return: BoudingBox with relative coordinates (from 0 to 1) of found object. If nothing is found, function
                 returns None
        """
        image = cv2.resize(image, (int(self.img_width), int(self.img_height)))
        image = np.reshape(image, (1, *np.shape(image))) / 255
        prediction = self.session.run(self.predictions, {self.inputs: image})

        return self.__interpret_prediction(prediction)

    def __interpret_prediction(self, predictions: np.ndarray) -> Optional[BoundingBox]:
        """
        Helper function for transfering raw neural network output into Bounding Box
        :param predictions: raw Yolo output
        :return: BoundingBox with relative (0.0 - 1.0) coorinates of found element or None if nothing is fount
        """
        predictions = np.array(predictions)
        probs = predictions[0, :, :, 4]
        pred_mat_shape = np.shape(probs)

        best_prediction = np.unravel_index(np.argmax(probs), pred_mat_shape)

        if probs[best_prediction] < self.threshold:
            return None

        coordinates_pred = predictions[0, best_prediction[0], best_prediction[1], 0:4]

        x = (best_prediction[0] + coordinates_pred[0]) / pred_mat_shape[0]
        y = (best_prediction[1] + coordinates_pred[1]) / pred_mat_shape[1]
        w = coordinates_pred[2]
        h = coordinates_pred[3]

        return BoundingBox(x, y, w, h)
