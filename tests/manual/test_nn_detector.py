import unittest
from neural_networks.YoloServer.YoloModel import YoloModel
import os
import cv2
import numpy as np
from tests.utils.prepare_test_yolo import prepare_test_yolo, MODEL_PATH, IMG_PATH
from tests.utils.stopwatch import Stopwatch
from neural_networks.nn_manager import NNManager
from utils.project_managment import PROJECT_ROOT
import argparse

VISUALIZE_OUTPUT = False
MODEL_NAME="path"
SELECTED_IMAGE_PATH=IMG_PATH

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tests of Yolo Neural Network model')
    parser.add_argument("-v", "--visualize", action="store_true", help="Show output of neural network on an image")
    parser.add_argument("-n", "--name", default=MODEL_PATH, help="Model name")
    parser.add_argument("-i", "--image", default=IMG_PATH, help="Path to image on which visualization will be made")
    args = parser.parse_args()

    if args.visualize:
        VISUALIZE_OUTPUT = True

    # TODO: Fix problems with relative / absolute paths
    MODEL_NAME = args.name
    SELECTED_IMAGE_PATH=args.image
    VISUALIZE_OUTPUT = args.visualize

    img = cv2.imread(SELECTED_IMAGE_PATH)
    prediction = NNManager.get_yolo_model(args.name).predict(img)

    if prediction is not None:
        prediction.denormalize(img.shape[1], img.shape[0], True)

    if VISUALIZE_OUTPUT:
        if prediction is not None:
            p1 = (int(prediction.x1), int(prediction.y1))
            p2 = (int(prediction.x2), int(prediction.y2))
            print(p1)
            print(p2)
            img = cv2.rectangle(img, p1, p2, (255,0,255))

        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

