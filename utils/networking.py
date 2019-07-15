<<<<<<< HEAD
import socket
from typing import Optional
import requests

def get_free_port() -> int:
    """
    Determines a free port using sockets.
    src: https://stackoverflow.com/questions/44875422/how-to-pick-a-free-port-for-a-subprocess
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()

    return port


def post_request(url: str, data: any = None) -> Optional[str]:
    """
    Sends http post request to specified url with optional data

    :param url: Target url for request, eg. http://google.com:80
    :param data: Data that will be attached to request
    :return: Response string if everyting is ok, None otherwise
    """

    response = requests.post(url=url, data=data)

    if response.status_code != 200:
        return None

    return response.content
=======
import socket


def get_free_port() -> int:
    """
    Determines a free port using sockets.
    src: https://stackoverflow.com/questions/44875422/how-to-pick-a-free-port-for-a-subprocess
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()

    return port
>>>>>>> Removing PyCharm related files from tracking on git
