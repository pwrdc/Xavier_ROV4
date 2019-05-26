from tasks.model_itf import IModel
from structures.bounding_box import BoundingBox
import tensorflow as tf
from typing import Optional
import cv2
import numpy as np

class YoloModel:
    def __init__(self, model_path, img_width=416, img_height=416, num_classes=1, input_tensor_name="input",
                 prediction_tensor_name="prediction"):
        self.model_path = model_path
        self.img_width = img_width
        self.img_height = img_height
        self.num_classes = num_classes

        self.input_tensor_name = input_tensor_name
        self.prediction_tensor_name = prediction_tensor_name

        self.session: Optional[tf.Session] = None
        self.saver = None
        self.inputs = None
        self.predictions = None

    def load(self):
        self.session = tf.Session()
        self.saver = tf.train.import_meta_graph(f"{self.model_path}/model.meta")
        self.saver.restore(self.session, f"{self.model_path}")

        self.inputs = self.session.graph.get_tensor_by_name(self.input_tensor_name)
        self.predictions = self.session.graph.get_tensor_by_name(self.prediction_tensor_name)

    def predict(self, image) -> BoundingBox:
        image = cv2.resize(image, (int(self.img_width), int(self.img_height)))
        np.reshape(image, (1, *np.shape(image)))
        prediction = self.session.run(self.predictions, {self.inputs: image})

        return BoundingBox(0, 0, 1, 1)


if __name__ == "__main__":
    model = YoloModel()
    model.load()
    model.predict()
