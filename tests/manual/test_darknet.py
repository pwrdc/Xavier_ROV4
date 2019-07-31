import unittest
from neural_networks.YoloServer.YoloModel import YoloModel
import os
import cv2
import numpy as np
from tests.utils.prepare_test_yolo import prepare_test_yolo, MODEL_PATH, IMG_PATH
from tests.utils.stopwatch import Stopwatch
from utils.project_managment import PROJECT_ROOT
from neural_networks.nn_manager import NNManager
import argparse
from configs.config import get_config

config = get_config("models")

parser = argparse.ArgumentParser(description='Tests of Yolo Neural Network model')
parser.add_argument("-v", "--visualize", action="store_true", help="Show output of neural network on an image")
parser.add_argument("-m", "--model", required=True, help="Model name")
parser.add_argument("-i", "--image", default=IMG_PATH, help="Path to image on which visualization will be made")
parser.add_argument("--video", required=False, help="Path to video file. Overwrites with --image option")
parser.add_argument("--fps", action="store_true", help="Test avarage network performance measured in fps")
args = parser.parse_args()

VISUALIZE = args.visualize
SELECTED_MODEL = args.model
INPUT_TENSOR = config[SELECTED_MODEL]["input_tensor"]
OUTPUT_TENSOR = config[SELECTED_MODEL]["output_tensor"]
IMG_PATH = args.image
VIDEO = args.video
FPS = args.fps

print(PROJECT_ROOT)

MODEL = NNManager.get_yolo_model(SELECTED_MODEL)

def predict(img):
    result = MODEL.predict(img)
    print(result)

    if result is not None:
        result.denormalize(img.shape[1], img.shape[0], inplace=True)

    return result

def prediction_text(img):
    result = predict(img)
    print("Neural network output")
    print("=========================")
    print(result)

def prediction_img(img, wait_time=0):
    prediction = predict(img)

    if prediction is not None:
        p1 = (int(prediction.x1), int(prediction.y1))
        p2 = (int(prediction.x2), int(prediction.y2))

        img = cv2.rectangle(img, p1, p2, (255,0,255))
    cv2.imshow('image', img)
    cv2.waitKey(wait_time)

    if wait_time == 0:
        cv2.destroyAllWindows()

def prediction_video(video):
    ret, img = video.read()

    while ret:
        ret, img = video.read()
        prediction_img(img, 1)

    cv2.destroyAllWindows()


def measure_fps(img, num_predictions=100):
    stopwatch = Stopwatch()

    stopwatch.start()
    for i in range(num_predictions):
        result = MODEL.predict(img)
    time = stopwatch.stop()
    FPS = num_predictions / time

    print("Neural network speed")
    print("========================")
    print(f"Making {num_predictions} predictions took {time} seconds")
    print(f"Avg fps was: {FPS}")

if VISUALIZE:
    if VIDEO is not None:
        video = cv2.VideoCapture(VIDEO)
        prediction_video(video)
    else:
        prediction_img(image)
else: 
    image = cv2.imread(IMG_PATH)
    prediction_text(image)
    
if FPS:
    measure_fps(image)
