import cv2
import time
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from definitions import CAMERAS, MAINDEF
from vision.front_cam_1 import FrontCamera1
from vision.bottom_camera import BottomCamera
from vision.arm_camera import ArmCamera
from vision.bumper_cam_left import BumperCamLeft
from vision.bumper_cam_right import BumperCamRight

PATH_DIRECOTRY = "./tests/image_detectors/crucifix/"


class TestRunner:
    def __init__(self):
        self.runner = TextTestRunner(verbosity=2)

    def run(self):
        test_suite = TestSuite(tests=[
            makeSuite(TestFrontCamera1),
            makeSuite(TestBottomCamera),
            makeSuite(TestArmCamera),
            makeSuite(TestBumperCameraLeft),
            makeSuite(TestBumperCameraRight)
        ])
        return self.runner.run(test_suite)

class TestFrontCamera1(TestCase):
    def test_front_get_image(self):
        # Test get_crucifix_cordinates method of CV solution
        camera = FrontCamera1(mode=MAINDEF.MODE)
        frame = camera.get_image()
        cv2.imwrite("front_cam_1_camera_test.png", frame)
        camera.__del__()
        time.sleep(2)

class TestBottomCamera(TestCase):
    def test_get_image(self):
        # Test get_crucifix_cordinates method of CV solution
        camera = BottomCamera(mode=MAINDEF.MODE)
        frame = camera.get_image()
        cv2.imwrite("bottom_camera_test.png", frame)
        camera.__del__()
        time.sleep(2)

class TestArmCamera(TestCase):
    def test_get_image(self):
        # Test get_crucifix_cordinates method of CV solution
        camera = ArmCamera(mode=MAINDEF.MODE)
        frame = camera.get_image()
        cv2.imwrite("arm_camera_test.png", frame)
        time.sleep(2)

class TestBumperCameraLeft(TestCase):
    def test_get_image(self):
        # Test get_crucifix_cordinates method of CV solution
        camera = BumperCamLeft(mode=MAINDEF.MODE)
        frame = camera.get_image()
        cv2.imwrite("bumper_left_camera_test.png", frame)
        time.sleep(2)

class TestBumperCameraRight(TestCase):
    def test_get_image(self):
        # Test get_crucifix_cordinates method of CV solution
        camera = BumperCamLeft(mode=MAINDEF.MODE)
        frame = camera.get_image()
        cv2.imwrite("bumper_right_camera_test.png", frame)
        time.sleep(2)

if __name__ == '__main__':
    print("Crucifix tester")
    test_runner = TestRunner()
    results = test_runner.run()

    if results.failures:
        print("Tests fail")
