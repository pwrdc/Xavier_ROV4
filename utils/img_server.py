from flask import Flask, request, Response
import pickle
import numpy as np

PORT=6669

if __name__ == "__main__":
    server = Flask(__name__)
    img = np.random.randn(416, 416, 3)
    
    @server.route("/set_img", methods=["POST"])
    def set_img():
        global img
        img_bytes = request.data
        img = pickle.loads(img_bytes)

        return "ok"

    @server.route("/get_img", methods=["GET"])
    def get_img():
        return pickle.dumps(img)

    server.run("0.0.0.0", PORT)
