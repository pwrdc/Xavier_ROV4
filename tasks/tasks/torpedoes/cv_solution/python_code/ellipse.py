import cv2
import numpy as np
import math

MIN_AREA = 2000  # in order to ignore too small areas
PI = 3.14159265358979323846
MAX_TOL = 5  # depends on proximity, ca. 5 if ellipses are close
THRESH = 134  # depends on light intensity: no water -> 120, simulation -> 134


class EllipseDetector:
    def __init__(self, img):
        self.img = img

    def img_area(self):
        img_info = self.img.shape
        x_img = img_info[0]
        y_img = img_info[1]
        max_area = x_img * y_img
        return max_area

    def prepare_img(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, THRESH, 255, 0)
        return thresh

    def detect(self):
        thresh = self.prepare_img()
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        ellipse_coords = []
        for cnt in contours:
            actual_area = abs(cv2.contourArea(cnt))
            if actual_area < MIN_AREA:
                continue

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            x0 = box[0, 0]
            y0 = box[0, 1]

            x1 = box[1, 0]
            y1 = box[1, 1]

            x2 = box[2, 0]
            y2 = box[2, 1]

            x = x2 - x1
            y = y0 - y1

            ratio = 1
            circle_radius = math.sqrt(x ** 2 / 4 + y ** 2 / 4)
            circle_area = PI * circle_radius ** 2
            ellipse_area = PI * x * y / 4
            if x > 0 and y > 0:
                if x > y:
                    ratio = x/y  # ideally 1.6
                else:
                    ratio = y/x

            if ellipse_area:
                if (circle_area / ellipse_area < MAX_TOL) and (circle_area / self.img_area() * 100 < MAX_TOL):
                    if (ratio > 1.5) and (ratio < 2.5):
                        # if np.any(img[x0, y0] == 0):
                        ellipse = cv2.fitEllipse(cnt)
                        cv2.ellipse(self.img, ellipse, (0, 0, 255), 2)
                        # print(x*y)
                        # print(("x{} y{}").format(x, y))
                        ellipse_coords.append(dict({"x": ((x0-x1)/2+x1), "y": (y1-y2)/2+y2}))
        cv2.imshow("Keypoints", self.img)
        return ellipse_coords




