import numpy as np
from utils.python_rest_subtask import PythonRESTSubtask
from structures.bounding_box import BoundingBox
from typing import Optional
from utils.networking import get_free_port

class YoloModelProxy:
    """
    Class for finding objects in image with Yolo architecture
    """
    def __init__(self, model_path: str, threshold = 0.5, is_secondary = False, input_tensor_name = "input:0", output_tensor_name = "output:0"):
        """
        :param model_path: Path to model, relative to project root
        """
        self.server_task: Optional[PythonRESTSubtask] = None
        self.model_path = model_path
        self.threshold = threshold
        self.port = get_free_port()
        self.input_tensor_name = input_tensor_name
        self.output_tensor_name = output_tensor_name

    def load(self) -> None:
        """
        Prepare model to be run
        """
        if self.server_task is not None:
            return

        # TODO: Add timeout
        self.server_task = PythonRESTSubtask.run("neural_networks/YoloServer/server.py",
                                                 (f"-p {self.port} -m {self.model_path} -t {self.threshold} "
                                                 f"--input_tensor {self.input_tensor_name} --output_tensor {self.output_tensor_name}")
                                                 , port=self.port, wait_ready=True)

    def predict(self, image: np.ndarray) -> Optional[BoundingBox]:
        """
        Finds object on an image
        :param image: np.array representing RGB image with values from 0 to 255
        :return: BoudingBox with relative coordinates (from 0 to 1) of found object. If nothing is found, function
                 returns None
        """
        if self.server_task is None:
            return None

        return self.server_task.post("predict", image)

    def is_active(self) -> bool:
        if self.server_task is None:
            return False
        else:
            return True

    def release(self) -> None:
        """
        Releases resources taken by neural network
        :return:
        """
        self.server_task.kill()
        self.server_task = None
