from tasks.model_itf import IModel
from structures.bounding_box import BoundingBox
import tensorflow as tf

class YoloModel:
    def __init__(self, model_path, img_width=416, img_height=416, num_classes=1, input_tensor_name="input",
                 prediction_tensor_name="prediction"):
        self.model_path = model_path
        self.img_width = img_width
        self.img_height = img_height
        self.num_classes = num_classes

        self.input_tensor_name = input_tensor_name
        self.prediction_tensor_name = prediction_tensor_name

        self.session = tf.
        self.inputs = None
        self.predictions = None

    def load(self):
        tf.train.import_meta_graph()

        pass

    def predict(self, image) -> BoundingBox:
        """ method for runing prediction
        """
        pass
