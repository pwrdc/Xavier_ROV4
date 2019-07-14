from neural_networks.yolo_model_proxy import YoloModelProxy
import time
from tests.utils.prepare_test_yolo import prepare_test_yolo


if __name__ == "__main__":
    prepare_test_yolo()

    model = YoloModelProxy("tests/resources/yolo/yolo_test_model")

    model.load()
    start = time.time()
    model.release()
    model.load()
    end = time.time()

    print(f"Switching models takes {end - start} seconds")