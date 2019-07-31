from neural_networks.yolo_model_proxy import YoloModelProxy
from utils.stopwatch import Stopwatch
from tests.utils.prepare_test_yolo import prepare_test_yolo
import argparse
from neural_networks.nn_manager import NNManager

parser = argparse.ArgumentParser(description='Tests of Yolo Neural Network model')
parser.add_argument("model", type=str, help="Model name")
args = parser.parse_args()

MODEL_NAME = args.model

if __name__ == "__main__":
    stopwatch = Stopwatch()
    NNManager.get_yolo_model(MODEL_NAME)

    stopwatch.start()
    NNManager.release()
    model = NNManager.get_yolo_model(MODEL_NAME)
    time = stopwatch.stop()

    print(f"Switching models takes {time} seconds")