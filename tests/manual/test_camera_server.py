from utils.project_managment import PROJECT_ROOT
import cv2
import requests
import pickle
from time import sleep
from definitions import CAMERAS
from configs.config import get_config
import argparse

config = get_config("cameras")

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--camera", type=str, default="front", help="Camera name")
parser.add_argument("-i", "--ip", type=str, default=config["hostname"], help="Camera server host ip")
parser.add_argument("-p", "--port", type=str, default=config['server_port'], help="Camera server port")
parser.add_argument("-wi", "--width", type=int, default=1280, help="Display width")
parser.add_argument("-hg", "--height", type=int, default=720, help="Display height")
args = parser.parse_args()

IP = args.ip
PORT = args.port
CAMERA = args.camera
WIDTH = args.width
HEIGHT = args.height

while(True):
    try:
        img_bytes = requests.post(f"http://{IP}:{PORT}/get_image", data=pickle.dumps(CAMERA), timeout=1).content
        img = pickle.loads(img_bytes)

        img = cv2.resize(img, (WIDTH, HEIGHT))
        
        cv2.imshow('image', img)
        cv2.waitKey(1)
    except Exception as e:
        print(e)

cv2.destroyAllWindows()
