from flask import Flask, request, Response
import pickle
import numpy as np
from threading import Thread, Lock
import cv2
import json
from time import sleep
import requests
from definitions import CAMERAS

with open("config.json", "r") as f:
        config = json.load(f)

IP = "localhost"
PORT = config["camera_server"]["port"]
SLEEP = 0.033

def get_image(camera_id):
    img_bytes = requests.post(f"http://{IP}:{PORT}/get_image", data=pickle.dumps(camera_id)).content
    img = pickle.loads(img_bytes)


lock = Lock()
images = {}
class ImageAquisition(Thread):
    def __init__(self, camera_ids):
        global images
        super().__init__()
        self.cameras = {}

        lock.acquire()
        for camera_id in camera_ids:
            self.cameras[camera_id] = cv2.VideoCapture(camera_id)
            _, images[camera_id] = self.cameras[camera_id].read()
        lock.release()

    def run(self):
        global images

        while(True):
            for (camera_id, camera) in self.cameras.items():
                _, images[camera_id] = camera.read()
            sleep(SLEEP)


if __name__ == "__main__":
    server = Flask(__name__)

    thread = ImageAquisition([0])
    thread.start()

    @server.route("/get_image", methods=["POST"])
    def predict():
        global images
        camera_id = pickle.loads(request.data)
        return pickle.dumps(images[camera_id])

    server.run("0.0.0.0", port=PORT)
