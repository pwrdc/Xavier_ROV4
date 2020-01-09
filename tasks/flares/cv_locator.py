import cv2 as cv
import numpy as np


def countLinesAverage(lines):
    sumX1 = 0
    sumX2 = 0
    sumY1 = 0
    sumY2 = 0
    counter = 0
    lineFinal = 0

    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            sumX1 += l[0]
            sumY1 += l[1]
            sumX2 += l[2]
            sumY2 += l[3]
            counter += 1

        lineFinal = np.array(
            [int(sumX1 / counter), int(sumY1 / counter), int(sumX2 / counter), int(sumY2 / counter)])

    return lineFinal


def detectLines(image):
    linesP = cv.HoughLinesP(image, 1, np.pi / 180, 50, None, 50, 10)

    return linesP


def cannyEdges(image):
    lowThreshCanny = 0
    highThreshCanny = 255 * 2
    cv.Canny(image, lowThreshCanny, highThreshCanny)

    return image


def blurImage(image):
    cv.blur(image, (9, 9))

    return image


class FlareDetector:
    def __init__(self):
        pass

    color = "red"

    lowHRed = 140
    highHRed = 179
    lowSRed = 30
    highSRed = 255
    lowVRed = 100
    highVRed = 255

    lowHYellow = 60
    highHYellow = 80
    lowSYellow = 50
    highSYellow = 255
    lowVYellow = 70
    highVYellow = 255
    
    kernel = np.ones((9, 9), np.uint8)

    def setLowThreshRed(self, lowHRed, lowSRed, lowVRed):
        self.lowHRed = lowHRed
        self.lowSRed = lowSRed
        self.lowVRed = lowVRed

    def setLowThreshYellow(self, lowHYellow, lowSYellow, lowVYellow):
        self.lowHYellow = lowHYellow
        self.lowSYellow = lowSYellow
        self.lowVYellow = lowVYellow

    def setHighThreshRed(self, highHRed, highSRed, highVRed):
        self.highHRed = highHRed
        self.highSRed = highSRed
        self.highVRed = highVRed

    def setHighThreshYellow(self, highHYellow, highSYellow, highVYellow):
        self.highHYellow = highHYellow
        self.highSYellow = highSYellow
        self.highVYellow = highVYellow

    def prepareImageRed(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        image = cv.inRange(image, np.array([self.lowHRed, self.lowSRed, self.lowVRed]),
                           np.array([self.highHRed, self.highSRed, self.highVRed]))
        image = self.doMorphOperations(image)
        image = blurImage(image)
        image = cannyEdges(image)
        return image

    def prepareImageYellow(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        image = cv.inRange(image, np.array([self.lowHYellow, self.lowSYellow, self.lowVYellow]),
                           np.array([self.highHYellow, self.highSYellow, self.highVYellow]))
        image = self.doMorphOperations(image)
        image = blurImage(image)
        image = cannyEdges(image)
        return image

    def doMorphOperations(self, image):
        cv.erode(image, self.kernel, iterations=1)
        cv.dilate(image, self.kernel, iterations=1)
        cv.dilate(image, self.kernel, iterations=1)
        cv.erode(image, self.kernel, iterations=1)

        return image

    def findMiddlePoint(self, image):
        imageCloned = image
        image = self.prepareImageRed(image)
        lines = detectLines(image)

        if lines is None:
            image = self.prepareImageYellow(imageCloned)
            lines = detectLines(image)
            self.color = "yellow"

        line = countLinesAverage(lines)

        x = int((line[0] + line[2]) / 2) / (image.shape[0])
        y = int((line[1] + line[3]) / 2) / (image.shape[1])

        point = {
            "x": x,
            "y": y,
            "color": self.color
        }

        return point
