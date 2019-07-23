from utils.project_managment import PROJECT_ROOT
import cv2
from utils.python_rest_subtask import PythonRESTSubtask
import requests
import pickle
from time import sleep
IP = "192.168.0.108"
PORT = 6669

while(True):
    try:
        img_bytes = requests.get(f"http://{IP}:{PORT}/get_img").content
        img = pickle.loads(img_bytes)

        cv2.imshow('image', img)
        cv2.waitKey(1)
    except Exception as e:
        print(e)
        sleep(1)
        pass

cv2.destroyAllWindows()
