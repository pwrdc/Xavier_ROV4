from utils.python_subtask import PythonSubtask
import requests
from utils.networking import post_request
import time
from typing import Any
import  pickle


class PythonRESTSubtask(PythonSubtask):
    """
    Class for interacting with python subtask REST services
    """

    def __init__(self, path, port=5000, post_request_fn=post_request):
        """
        :param path: Path to python script that is run, relative to project root
        :param port port on which server will be found
        :param post_request_fn: f(url, data) that will be used for posts requests to subtasks
        """
        super().__init__(path)
        self.port = port
        self.post_request = post_request_fn

    def wait_ready(self, url="is_ready", expected_response="true", poll_time=1, timeout=None) -> bool:
        """
        Waits until server is ready
        :param url: url to service that tells it sever is ready
        :param expected_response: response from server that indicates the server is ready
        :param poll_time: time between consecutive polls
        :param timeout: Maximum time after witch retries are aborted and False is returned
        :return: True if server is ready, false if couldn't get positive response
        """
        start_time = time.time()

        while True:
            try:
                req = requests.get(f"http://localhost:{self.port}/{url}")
                if req.text == expected_response:
                    return True
            except Exception:
                pass

            time.sleep(poll_time)

            if timeout is not None and time.time() - start_time > timeout:
                return False

    def post(self, url, data, pickle_data=True, unpickle_result=True) -> Any:
        """
        Sends a post request to REST server
        :param url: Url to rest service, without server adress. Eg: yolo/predict
        :param data: data that will be supplied with post request.
        :param pickle_data: serialize input data with pickle library if set to True
        :param unpickle_result: deserialize response with pickle library if set to True
        :return: Response from REST server
        """
        if pickle_data:
            data = pickle.dumps(data)

        req = requests.post(url=f"http://localhost:{self.port}/{url}", data=data)
        result = req.content

        if unpickle_result:
            result = pickle.loads(result)

        return result

    def get(self, url, data, pickle_data=True, unpickle_result=True) -> Any:
        """
        Sends a post request to REST server
        :param url: Url to rest service, without server adress. Eg: yolo/predict
        :param data: data that will be supplied with get request.
        :param pickle_data: serialize input data with pickle library if set to True
        :param unpickle_result: deserialize response with pickle library if set to True
        :return: Response from REST server
        """
        if pickle_data:
            data = pickle.dumps(data)

        req = requests.get(url=f"http://localhost:{self.port}/{url}", data=data)
        result = req.content

        if unpickle_result:
            result = pickle.loads(result)

        return result

    @staticmethod
    def run(path, arguments, port=5000, wait_ready=True):  # -> PythonRESTSubtask
        """
        Factory method for creating and starting a python subtask
        :param path: Path to python script that is run, relative to project root
        :param arguments: arguments provided to python script
        :param port port on which server will be found
        :param wait_ready will wait until server is ready before returning task
        :return: PythonRESTSubtask class with task already started
        """
        task = PythonRESTSubtask(path, port)
        task.start(arguments)

        if wait_ready:
            task.wait_ready()

        return task
