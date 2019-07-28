from flask import Flask, request, Response
import pickle
import numpy as np
from threading import Thread, Lock
import cv2
import json
from time import sleep
import requests
from definitions import CAMERAS
from configs.config import get_config

# Turn off flask logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Server config
config = get_config("cameras")
IP = config["hostname"]
PORT = config["server_port"]
SLEEP = config["interframe_sleep"]

def get_image(camera_name: str):
    """
    Gets image from specified camera from camera server
    """
    img_bytes = requests.post(f"http://{IP}:{PORT}/get_image", data=pickle.dumps(camera_name)).content
    img = pickle.loads(img_bytes)


images = {}
class ImageAquisition(Thread):
    def __init__(self):
        global images
        super().__init__()
        self.cameras = {}

        self.cameras_config = config["cameras"]

        for camera_name, camera_config in self.cameras_config.items():
            if camera_config["debug"] == False:
                self.cameras[camera_name] = cv2.VideoCapture(int(camera_config["id"])) # Use physical camera
            else:
                self.cameras[camera_name] = cv2.VideoCapture(camera_config["debug_path"]) # Use video as camera input

            _, images[camera_name] = self.cameras[camera_name].read()

    def run(self):
        global images

        while(True):
            for (camera_id, camera) in self.cameras.items():
                ret, img = camera.read()
                if ret:
                    images[camera_id] = img
                elif self.cameras_config[camera_id]["debug"]:
                    camera.set(cv2.CAP_PROP_POS_FRAMES, 0) # restarts video from start
                
            sleep(SLEEP)

if __name__ == "__main__":
    server = Flask(__name__)

    thread = ImageAquisition()
    thread.start()

    @server.route("/get_image", methods=["POST"])
    def predict():
        global images
        camera_id = pickle.loads(request.data)
        return pickle.dumps(images[camera_id])

    server.run("0.0.0.0", port=PORT)