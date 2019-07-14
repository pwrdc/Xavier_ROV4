import unittest
from neural_networks.YoloServer.YoloModel import YoloModel
import os
import cv2
import numpy as np
from tests.utils.prepare_test_yolo import prepare_test_yolo, MODEL_PATH, IMG_PATH
from tests.utils.stopwatch import Stopwatch
import argparse

VISUALIZE_OUTPUT = False

def test_ModelSetup(img):
    model = YoloModel(MODEL_PATH, prediction_tensor_name="conv2d_1/Sigmoid:0", input_tensor_name="input_1:0")
    model.load()
    result = model.predict(img)

    result.denormalize(img.shape[1], img.shape[0], inplace=True)

    print("Neural network output")
    print("=========================")
    print(result)

    p1 = (int(result.x1), int(result.y1))
    p2 = (int(result.x2), int(result.y2))

    if VISUALIZE_OUTPUT:
        img = cv2.rectangle(img, p1, p2, (255,0,255))
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return model

def test_ModelFPS(model, num_predictions=100):
    stopwatch = Stopwatch()

    stopwatch.start()
    for i in range(num_predictions):
        result = model.predict(img)
    time = stopwatch.stop()
    FPS = num_predictions / time

    print("Neural network speed")
    print("========================")
    print(f"Making {num_predictions} predictions took {time} seconds")
    print(f"Avg fps was: {FPS}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tests of Yolo Neural Network model')
    parser.add_argument("-v", "--visualize", action="store_true", help="Show output of neural network on an image")
    args = parser.parse_args()

    if args.visualize:
        VISUALIZE_OUTPUT = True

    prepare_test_yolo()
    img = cv2.imread(IMG_PATH)

    model = test_ModelSetup(img)
    test_ModelFPS(model, 100)

