import cv2
import numpy as np
import math
from tasks.task_executor_itf import ITaskExecutor
from tasks.garlic.locator.GarlicDetector import GarlicDetector


class GrabGarlic(ITaskExecutor):
    def __init__(self, movement_object, cameras_dict):
        self.movement = movement_object
        self.bottom_camera = cameras_dict('bottom_camera')

        self.detector = GarlicDetector()

        self.dest_location = np.array([0, 0])   # docelowe położenie punktu chwytu względem kamery (x, y) [mm]

        self.dest_orientation = 90  # docelowa orientacja elementu [stopnie]

        self.element_size_real = 0.245   # rzeczywista wielkość elementu [mm]
        self.dest_distance = 0  # docelowa odległość punktu chwytu od kamery (z) [mm]
        self.size_distance_factor = 4.05  # wielkość obrazu elementu [px/px] * odległość elementu [mm]
        # ewentualnie wielkość elementu [mm] * ogniskowa kamery [mm]

    def run(self):
        frame = self.download_image()

        lines, size = self.detector.coords_detect(frame)
        line, orientation_error = self.choose_line(lines)
        location_error = self.choose_point(line)

        # przeliczenie wielkości elemetu [px/px] na odległość [m]
        distance_error = self.size_distance_factor / size - self.dest_distance

        # przeliczenie uchybu położenia z [px/px] na [m]
        location_error_real = self.element_size_real / size * location_error

        self.move(location_error_real, orientation_error, distance_error)

        return True

    def download_image(self):
        return self.bottom_camera.get_image()

    # dobór pod względem orientacji, zwraca linię oraz jej orientację [0, 180]
    def choose_line(self, lines):
        orientation_error_list = []
        for line in lines:
            orientation = self.find_orientation(line)
            orientation_error_list.append(orientation - self.dest_orientation)

        if abs(orientation_error_list[0]) < abs(orientation_error_list[1]):
            return lines[0], orientation_error_list[0]
        else:
            return lines[1], orientation_error_list[1]

    # dobór pod względem położenia, zwraca położenie punktu [px]
    def choose_point(self, line):
        location_error_list = []
        location_error_sqr_list = []

        for point in line:
            location_error = point - self.dest_location
            location_error_sqr = location_error[0] ** 2 + location_error[1] ** 2
            location_error_list.append(location_error)
            location_error_sqr_list.append(location_error_sqr)

        if location_error_sqr_list[0] < location_error_sqr_list[1]:
            return location_error_list[0]
        else:
            return location_error_list[1]

    @staticmethod
    def normalize_coordinates(lines, frame):
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                lines[i][j] = np.array([(lines[i][j][0] - (frame.shape[1] / 2)) / (frame.shape[1] / 2),
                                        ((frame.shape[0] / 2) - lines[i][j][1]) / (frame.shape[0] / 2)])

    @staticmethod
    def normalize_location(location, frame):
        return [(location[0] - (frame.shape[1] / 2)) / (frame.shape[1] / 2),
                ((frame.shape[0] / 2) - location[1]) / (frame.shape[0] / 2)]

    # zwraca orientację linii w zakresie [0, 180]
    @staticmethod
    def find_orientation(line):
        vector = line[0] - line[1]
        orientation = math.atan2(vector[1], vector[0])
        orientation_degrees = orientation * 360 / (2 * math.pi)
        if orientation_degrees < 0:
            orientation_degrees += 180
        return orientation_degrees

    # obsługa ruchu
    def move(self, location_error, orientation_error, distance_error):
        self.move_XY(location_error)
        self.rotate(orientation_error)
        self.move_Z(distance_error)

    # przemieść w poziomie
    def move_XY(self, locationError):
        self.movement.move_distance(locationError[0], locationError[1], 0)

    # obróć yaw
    def rotate(self, orientationError):
        self.movement.rotate_angle(0, 0, orientationError)

    # przemieść w pionie
    def move_Z(self, distanceError):
        self.movement.move_distance(0, 0, distanceError)
