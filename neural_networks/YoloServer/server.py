from flask import Flask, request, Response
import pickle

server = Flask(__name__)


@server.route("/predict", methods=["POST"])
def predict():
    img_bytes = request.data
    img = pickle.loads(img_bytes)

    print(img)

    return 'wut'


if __name__ == "__main__":
    server.run("localhost", 5000)
