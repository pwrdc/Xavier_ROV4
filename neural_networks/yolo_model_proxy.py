import numpy as np
from utils.python_rest_subtask import PythonRESTSubtask
from typing import Optional
from utils.networking import get_free_port


class YoloModelProxy:
    """
    Class for finding objects in image with Yolo architecture
    """
    def __init__(self, model_path: str):
        """
        :param model_path: Path to model, relative to project root
        """
        self.server_task: Optional[PythonRESTSubtask] = None
        self.model_path = model_path
        self.port = get_free_port()

    def load(self) -> None:
        """
        Prepare model to be run
        """
        if self.server_task is not None:
            return

        # TODO: Add timeout
        self.server_task = PythonRESTSubtask.run("neural_networks/YoloServer/server.py",
                                                 f"-p {self.port} -m {self.model_path}", port=self.port,
                                                 wait_ready=True)

    def predict(self, image: np.ndarray) -> Optional[PythonRESTSubtask]:
        """
        Finds object on an image
        :param image: np.array representing RGB image with values from 0 to 255
        :return: BoudingBox with relative coordinates (from 0 to 1) of found object. If nothing is found, function
                 returns None
        """
        if self.server_task is None:
            return None

        return self.server_task.post("predict", image)

    def release(self) -> None:
        """
        Releases resources taken by neural network
        :return:
        """
        self.server_task.kill()
        self.server_task = None
