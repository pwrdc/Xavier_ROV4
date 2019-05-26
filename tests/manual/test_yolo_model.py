import unittest
from neural_networks.YoloServer.YoloModel import YoloModel
import os
import cv2
import numpy as np
from tests.utils.prepare_test_yolo import prepare_test_yolo, MODEL_PATH, IMG_PATH


class TestYoloModel(unittest.TestCase):
    def setUp(self) -> None:
        prepare_test_yolo()

    def test_ModelSetup(self):
        img = cv2.imread(IMG_PATH)
        model = YoloModel(MODEL_PATH, prediction_tensor_name="conv2d_1/Sigmoid:0", input_tensor_name="input_1:0")
        model.load()
        result = model.predict(img)

        print (img.shape)
        result.denormalize(img.shape[1], img.shape[0], inplace=True)

        print(result)

        p1 = (int(result.x1), int(result.y1))
        p2 = (int(result.x2), int(result.y2))

        img = cv2.rectangle(img, p1, p2, (255,0,255))
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    unittest.main()