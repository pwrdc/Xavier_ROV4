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
