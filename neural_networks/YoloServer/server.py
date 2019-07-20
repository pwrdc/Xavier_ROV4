from flask import Flask, request, Response
import pickle
import argparse as ap
from neural_networks.YoloServer.YoloModel import YoloModel
from utils.project_managment import PROJECT_ROOT
import logging
logging.basicConfig(level=logging.ERROR)


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Train SSD Network")
    parser.add_argument("-p", '--port', default=5000, type=int, help="Port on which server will be run")
    parser.add_argument("-m", '--model', required=True, type=str, help="Path to model folder, relative to project root")
    parser.add_argument("-t", '--threshold', default=0.5, type=float, help="Detection threshold (from 0 to 1)")
    parser.add_argument('--input_tensor', default="input:0", type=str, help="Name of the input placeholder tensor")
    parser.add_argument('--output_tensor', default="output:0", type=str, help="Name of the output tensor")


    args = parser.parse_args()

    server = Flask(__name__)

    model = YoloModel(f"{PROJECT_ROOT}/{args.model}", prediction_tensor_name=args.output_tensor,
                      input_tensor_name=args.input_tensor, threshold=args.threshold)
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
