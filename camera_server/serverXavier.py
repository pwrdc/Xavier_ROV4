import socket
import cv2
import struct
import pickle
from logpy.LogPy import Logger


# [BUGFIX] Socket binding error: [Errno 98] Address already in use
# ->  Changing ports between 9999 and 8888 in create_socket() function and client.py may help

class ServerXavier:
    def __init__(self, host="localhost", port=8888, black_and_white=False, retry_no=5):
        """
        Initialize server
        :param host: [String] host address
        :param port: [Int] port
        :param black_and_white: [Bool] Is white and white camera image?
        :param retry_no: [Int] Number of retries
        """
        self.host = host
        self.port = port
        self.bw = black_and_white
        self.retryNo = retry_no
        # set logger file
        self.logger = Logger(filename='serverXavier', title="ServerXavier")
        # start up camera
        self.cameraCapture = cv2.VideoCapture(0)
        if not self.__auto_retry(self.__create_socket()):
            self.logger.log(f"ERROR: Create socket failure")
            return
        if not self.__auto_retry(self.__bind_socket()):
            self.logger.log(f"ERROR: Bind socket failure")
            return
        self.logger.log(f"Init complete")

    def __create_socket(self):
        """
        Create socket for making connection possible
        :return: [Bool] True if successful
        """
        try:
            self.socket = socket.socket()
            return True
        except socket.error as msg:
            self.logger.log(f'WARNING: Socket creation error: {msg}.')
            return False

    def __bind_socket(self):
        """
        Bind selected socket and listen for connections
        :return: [Bool] True if successful
        """
        try:
            self.logger.log(f"Binding the Port {self.port}")

            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            return True

        except socket.error as msg:
            self.logger.log(f"WARNING: Socket binding error: {msg}.")
            return False

    def __auto_retry(self, function):
        """
        Auto-retry function
        :param function: [Function] Function to try. Require False/0 if unsuccessful
        :return: True if finished with retry number of tries
        """
        for i in range(self.retryNo):
            if function:
                return True
            elif i == self.retryNo:
                self.logger.log("ERROR: Initialize error. Check logs for more info.")
                return False
            self.logger.log(f"Retrying. Try: {i} of {self.retryNo}.")

    def socket_accept(self):
        """
        Accept connection from client
        :return:
        """
        conn, address = self.socket.accept()
        self.logger.log(f"Connection has been established! | {str(address[0])}:{str(address[1])}")
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            conn.send(self.__frame)
        conn.close()

    @property
    def __frame(self):
        """
        Get picture frame
        :return: frame
        """
        # Capture frame
        ret, frame = self.cameraCapture.read()

        # Handles the mirroring of the current frame
        frame = cv2.flip(frame, 1)

        if self.bw:
            # Change color to black and white if decided
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Code image
        result, frame = cv2.imencode('.jpg', frame)

        data = pickle.dumps(frame, 0)
        size = len(data)
        return struct.pack(">L", size) + data


if __name__ == "__main__":
    serverXavier = ServerXavier()
    serverXavier.socket_accept()

