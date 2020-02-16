import cv2 as cv
import numpy as np
from bounding_box import *


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


def findBoxDimensions(lines):
    minX = 300000
    minY = 300000
    maxX = 0
    maxY = 0
    h = 0
    w = 0

    '''''
    Finding maximum and minimum values of lines found by Probabilistic Hough lines algorithm
    '''''

    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            if l[0] < minX or l[2] < minX:
                if l[0] < l[2]:
                    minX = l[0]
                else:
                    minX = l[2]
            if l[1] < minY or l[3] < minY:
                if l[1] < l[3]:
                    minY = l[1]
                else:
                    minY = l[3]
            if l[0] > maxX or l[3] > maxX:
                if l[0] > l[2]:
                    maxX = l[0]
                else:
                    maxX = l[2]
            if l[1] > maxY or l[3] > maxY:
                if l[1] > l[3]:
                    maxY
                else:
                    maxY = l[1]

        h = maxY - minY
        w = maxX - minX

        size = (h, w)

        return size


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

    '''''
    Parameters used for threshold. Bottom and top values represented in HSV color model where
    H stands for hue
    S stands for saturation
    V stands for value
    Change of parameters may be needed due to conditions in pool (light etc.) 
    '''''
    lowHRed = 110
    highHRed = 179
    lowSRed = 0
    highSRed = 160
    lowVRed = 0
    highVRed = 200

    lowHYellow = 32
    highHYellow = 87
    lowSYellow = 0
    highSYellow = 180
    lowVYellow = 80
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

    def doMorphOperations(self, image):
        cv.erode(image, self.kernel, iterations=1)
        cv.dilate(image, self.kernel, iterations=1)
        cv.dilate(image, self.kernel, iterations=1)
        cv.erode(image, self.kernel, iterations=1)

        return image

    def prepareImageYellow(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        image = cv.inRange(image, np.array([self.lowHYellow, self.lowSYellow, self.lowVYellow]),
                           np.array([self.highHYellow, self.highSYellow, self.highVYellow]))
        image = self.doMorphOperations(image)
        image = blurImage(image)
        image = cannyEdges(image)
        return image

    def findMiddlePoint(self, image):
        imageCloned = image

        '''''
        Checking whether flare is red or yellow based on verifying if any lines where found
        for HSV set for red flare  
        '''''
        image = self.prepareImageRed(image)
        lines = detectLines(image)

        if lines is None:
            image = self.prepareImageYellow(imageCloned)
            lines = detectLines(image)
            self.color = "yellow"

        '''''
        :param x: x coordinate of alleged flare's center point 
        :param y: y coordinate of alleged flare's center point 
        :param h: height of bounding box
        :param w: width of bounding box
        :return: return BoundingBox object, and color of the recognized flare
        '''''

        line = countLinesAverage(lines)
        size = findBoxDimensions(lines)

        x = int((line[0] + line[2]) / 2)
        y = int((line[1] + line[3]) / 2)
        h = size[0]
        w = size[1] 

        box = BoundingBox(x, y, w, h, 1)

        return box, self.color


