from tasks.path.locator.locator_itf import ILocator
import numpy as np
from structures.bounding_box import BoundingBox
import cv2

MIN_RED = 170
MIN_GREEN = 150
MAX_BLUE = 50

class BarbarianLocator():
    def get_path_bounding_box(self, image):
        image = image

        xs = []
        ys = []

        image = cv2.resize(image, (10, 10))

        for x in range(10):
            for y in range(10):
                red_ok = image[y][x][2] > MIN_RED
                green_ok = image[y][x][1] > MIN_GREEN
                blue_ok = image[y][x][0] < MAX_BLUE

                if red_ok and green_ok and blue_ok:
                    xs.append(x)
                    ys.append(y)
        
        if len(xs) == 0 or len(ys) == 0:
            return None

        x_min = np.min(xs)
        x_max = np.max(xs)
        y_min = np.min(ys)
        y_max = np.max(ys)

        w = x_max - x_min
        h = y_max - y_min
        xc = (x_min + x_max) / 2
        yc = (y_min + y_max) / 2

        print(f"X_MIN: {x_min}")
        print(f"X_MAX: {x_max}")
        print(f"Y_MIN: {y_min}")
        print(f"Y_MAX: {y_max}")

        result = BoundingBox(xc, yc, w, h)
        result.normalize(10, 10, True)

        return result