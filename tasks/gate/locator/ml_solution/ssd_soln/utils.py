from collections import namedtuple
import cv2


class Box:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.x1 = x - w/2
        self.x2 = x + w/2
        self.y1 = y - h/2
        self.y2 = y + h/2

        self.p1 = (self.x1, self.y1)
        self.p2 = (self.x2, self.y2)

    @staticmethod
    def from_points(x1, y1, x2, y2):
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        w = x2 - x1
        h = y2 - y1

        return Box(x, y, w, h)

    def normalize(self, img_widh, img_height):
        return Box(self.x / img_widh,
                   self.y / img_height,
                   self.w / img_widh,
                   self.h / img_height)


AnchorBoxDims = namedtuple("AnchodBoxSize", ["width", "height"])
FeatureMap = namedtuple("FeatureMap", ["width", "height", "aspect_ratios"])


def intersection_over_union(boxA: Box, boxB: Box):
    xA = max(boxA.x1, boxB.x1)
    yA = max(boxA.y1, boxB.y1)
    xB = min(boxA.x2, boxB.x2)
    yB = min(boxA.y2, boxB.y2)

    interArea = max(0.0, xB - xA) * max(0.0, yB - yA)

    boxAArea = boxA.w * boxA.h
    boxBArea = boxB.w * boxB.h

    unionArea = boxAArea + boxBArea - interArea

    return interArea / unionArea


def draw_box(img, box: Box, color = (255, 0 ,0), thickness=3):
    x1 = int((box.x - box.w / 2) * img.shape[1])
    x2 = int((box.x + box.w / 2) * img.shape[1])
    y1 = int((box.y - box.h / 2) * img.shape[0])
    y2 = int((box.y + box.h / 2) * img.shape[0])

    img = cv2.circle(img,(int(box.x * img.shape[1]), int(box.y *img.shape[0])), 2, (0,0,255), -1)
    img = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    cv2.imshow('image', img)
    cv2.waitKey(0)

    return img

