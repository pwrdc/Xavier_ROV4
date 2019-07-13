"""
File contains interface for locator class for holes locator
"""
import cv2
import numpy as np

CURRENT_DIRECTORY = "tasks/torpedoes/"


class HolesDetector():
    def __init__(self, current_directory= "tasks/torpedoes/"):
        self.CURRENT_DIRECTORY = current_directory

        template = cv2.imread(self.CURRENT_DIRECTORY + 'heart_template.png', cv2.CV_8UC1)
        self.contours_template, self.hierarchy_template = cv2.findContours(template, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    def prepareImage(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame = self.thresholdImage(frame)
        frame = self.doMorphOperations(frame)
        #frame = self.blurrImage(frame)
        return frame

    def thresholdImage(self, frame):
        lower_h = 50
        lower_s = 100
        lower_v = 100
        lower_arr = np.array([lower_h, lower_s, lower_v])
        upper_h = 70
        upper_s = 255
        upper_v = 255
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
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    def compareImages(self, contours, hierarchy):
        thresh = 0.05
        hole = np.array([])
        for i in range(0, int(hierarchy[0].size / 4)):
            child = hierarchy[0][i][2]
            if child != -1: # if contour has inner contour
                comparison = cv2.matchShapes(self.contours_template[0], contours[i], 1, 0.0)  # outer contour
                if comparison < thresh:
                    comparison = cv2.matchShapes(self.contours_template[1], contours[child], 1, 0.0)  # inner contour
                    if comparison < thresh:
                        hole = contours[child]
                        break
        return hole

    def get_heart_cordinates(self, image):
        image = self.prepareImage(image)
        contours, hierarchy = self.findContours(image)
        hole = self.compareImages(contours, hierarchy)
        coordinates = {}
        if hole.size != 0:
            coordinates = self.find_coordinates(hole, image)
        return coordinates

    def find_coordinates(self, hole, frame):
        leftmost = hole[hole[:, :, 0].argmin()][0]
        rightmost = hole[hole[:, :, 0].argmax()][0]
        topmost = hole[hole[:, :, 1].argmin()][0]
        bottommost = hole[hole[:, :, 1].argmax()][0]

        size_x = rightmost[0] - leftmost[0]
        size_y = bottommost[1] - topmost[1]
        a = max(size_x, size_y)

        x = leftmost[0] + (size_x/2)
        y = topmost[1] + (size_y/2)

        x, y = self.normalize_coordinates(x, y, frame)
        coordinates = {"x": x, "y": y, "a": a}
        return coordinates

    def normalize_coordinates(self, x, y, frame):
        x = (x - (frame.shape[1] / 2)) / (frame.shape[1] / 2)
        y = ((frame.shape[0] / 2) - y) / (frame.shape[0] / 2)
        return x, y

if __name__ == '__main__':
    h = HolesDetector(current_directory="")
