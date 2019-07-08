from flask import Flask, request, Response
import pickle
import argparse as ap
from neural_networks.YoloServer.YoloModel import YoloModel
from utils.project_managment import PROJECT_ROOT

if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Train SSD Network")
    parser.add_argument("-p", '--port', default=5000, type=int, help="Port on which server will be run")
    parser.add_argument("-m", '--model', required=True, type=str, help="Path to model folder, relative to project root")
    args = parser.parse_args()

    server = Flask(__name__)

    model = YoloModel(f"{PROJECT_ROOT}/{args.model}", prediction_tensor_name="conv2d_1/Sigmoid:0",
                      input_tensor_name="input_1:0")
    model.load()

    @server.route("/predict", methods=["POST"])
    def predict():
        img_bytes = request.data
        img = pickle.loads(img_bytes)

        result = model.predict(img)

        return pickle.dumps(result)

    @server.route("/is_ready", methods=["GET"])
    def is_ready():
        return "true"

    server.run("localhost", args.port)
