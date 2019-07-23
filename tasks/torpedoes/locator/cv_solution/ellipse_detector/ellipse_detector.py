"""
File contains interface for locator class for holes locator
"""
import cv2
import numpy as np

CURRENT_DIRECTORY = "tasks/torpedoes/"


class EllipseDetector:
    def __init__(self, current_directory="tasks/torpedoes/"):
        self.CURRENT_DIRECTORY = current_directory
    
    def draw_contours(self, contours, image, name,  hierarchy=None):
        image_copy = np.zeros((image.shape[0], image.shape[1], 3))
        if hierarchy is not None:
            for i in range(0, int(hierarchy[0].size / 4)):
                cv2.drawContours(image_copy, contours, i, (0, 0, 255), 1)
                cv2.imshow(name, image_copy)
        else:
            cv2.drawContours(image_copy, contours, -1, (0, 0, 255), 1)
            cv2.imshow(name, image_copy)

    def prepareImage(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_thresh = self.thresholdImage(frame)
        return frame, frame_thresh    # nieprogowany i progowany. potrzebne do rozpoznawania otwartego otworu

    def thresholdImage(self, frame):
        lower_h = 60
        lower_s = 165
        lower_v = 127
        lower_arr = np.array([lower_h, lower_s, lower_v])
        upper_h = 85
        upper_s = 255
        upper_v = 165
        upper_arr = np.array([upper_h, upper_s, upper_v])
        frame = cv2.inRange(frame, lower_arr, upper_arr)
        return frame

    def doMorphOperations(self, frame):
        kernel = (19, 19)

        frame = cv2.erode(frame, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel))
        frame = cv2.dilate(frame, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel))
        frame = cv2.dilate(frame, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel))
        frame = cv2.erode(frame, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel))
        return frame

    def blurrImage(self, frame):
        kernel = (9, 9)
        sigma_x = 0
        sigma_y = 0
        frame = cv2.GaussianBlur(frame, kernel, sigma_x, sigma_y)
        return frame

    def findContours(self, frame):
        # tylko zewnętrzne kontury
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    def compareImages(self, contours, hierarchy):
        area_min = 1000
        hole_list = []
        roundness_min = 11  # próg od którego kontur jest uznawany za elipsę
        for i in range(0, int(hierarchy[0].size / 4)):
            area = cv2.contourArea(contours[i])
            print("area: ", area)
            if area > area_min:
                perimeter = cv2.arcLength(contours[i], True)
                print("perimeter: ", perimeter)
                roundness = area/perimeter
                print("okraglosc: ", roundness)
                if roundness > roundness_min:
                    hole_list.append(contours[i])
        return hole_list

    def get_holes_cordinates(self, image):
        image, image_thresh = self.prepareImage(image)
        contours, hierarchy = self.findContours(image_thresh)
        coordinates = {}
        if contours:
            hole_list = self.compareImages(contours, hierarchy)
            #print("hole_list: ", hole_list)
            if hole_list:   # jeśli znalazł otwór
                coordinates = self.find_coordinates(hole_list, image)
        print(coordinates)
        return coordinates

    def find_coordinates(self, hole_list, frame):
        coordinates = {"x_open": None,
                       "y_open": None,
                       "x_closed": None,
                       "y_closed": None}
        coordinates_list = []
        for hole in hole_list:
            leftmost = hole[hole[:, :, 0].argmin()][0]
            rightmost = hole[hole[:, :, 0].argmax()][0]
            topmost = hole[hole[:, :, 1].argmin()][0]
            bottommost = hole[hole[:, :, 1].argmax()][0]

            size_x = rightmost[0] - leftmost[0]
            size_y = bottommost[1] - topmost[1]
            #a = max(size_x, size_y)

            x = leftmost[0] + (size_x/2)
            y = topmost[1] + (size_y/2)

            coordinates_list.append([x, y])
        if self.find_open(coordinates_list, frame):
            self.normalize_coordinates(coordinates_list, frame)
            coordinates["x_open"] = coordinates_list[0][0]
            coordinates["y_open"] = coordinates_list[0][1]
            coordinates["x_closed"] = coordinates_list[1][0]
            coordinates["y_closed"] = coordinates_list[1][1]
        else:
            self.normalize_coordinates(coordinates_list, frame)
            coordinates["x_open"] = coordinates_list[1][0]
            coordinates["y_open"] = coordinates_list[1][1]
            coordinates["x_closed"] = coordinates_list[0][0]
            coordinates["y_closed"] = coordinates_list[0][1]

        return coordinates

    def normalize_coordinates(self, coordinates_list, frame):
        for coordinates in coordinates_list:
            coordinates[0] = (coordinates[0] - (frame.shape[1] / 2)) / (frame.shape[1] / 2)
            coordinates[1] = ((frame.shape[0] / 2) - coordinates[1]) / (frame.shape[0] / 2)
        return coordinates_list

    @staticmethod
    def show_points(lines, image):
        image_copy = image
        for line in lines:
                for i in range(-2, 2):
                    for j in range(-2, 2):
                        image_copy[int(line['y']) + i][int(line['x']) + j] = (255, 0, 0)
        cv2.imshow("punkty", image_copy)
        cv2.imwrite("punkty.png", image_copy)
        cv2.waitKey()

    # zwraca True jeśli pierwszy otwór jest otwarty, przeciwnie False
    @staticmethod
    def find_open(coordinates_list, frame):
        color_1 = frame[int(coordinates_list[0][1]), int(coordinates_list[0][0]), 0]
        color_2 = frame[int(coordinates_list[1][1]), int(coordinates_list[1][0]), 0]
        #print("color1: ", color_1)
        #print("color2: ", color_2)
        return color_1 > color_2

if __name__ == '__main__':
    h = EllipseDetector(current_directory="")
