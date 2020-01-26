import cv2
import os
import json
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from tasks.torpedoes.holes_detector import HeartDetector as CVLocatorHeart
from tasks.torpedoes.holes_detector import EllipseDetector as CVLocatorEllipse

PATH_DIRECOTRY = "./tests/image_detectors/torpedoes/"
DELTA_CORDINATES = 0.05

class TestRunner:
    def __init__(self):
        self.runner = TextTestRunner(verbosity=2)

    def run(self):
        test_suite = TestSuite(tests=[
            makeSuite(TestTorpedoLocatorCV)#,
            #makeSuite(TestTorpedoLocatorML)
        ])
        return self.runner.run(test_suite)

class TestTorpedoLocatorCV(TestCase):
    '''
    def test_get_general_coordinates(self):
        # Test get_general_coordinates method of CV solution
        with open(PATH_DIRECOTRY + "general_coordinates.json", "r") as read_file:
            all_expected_coordinates = json.load(read_file)

        for filename in os.listdir(PATH_DIRECOTRY):
            if filename.endswith("_general.png"):
                relative_filename = PATH_DIRECOTRY+filename

                image = cv2.imread(relative_filename)
                locator = CVLocator()
                cordinates = locator.get_general_cordinates(image)
                expected_coordinates = all_expected_coordinates[filename]

                self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

    '''
    def test_get_heart_coordinates(self):
        # Test get_heart_coordinates method of CV solution
        with open(PATH_DIRECOTRY + "heart_coordinates.json", "r") as read_file:
            all_expected_coordinates = json.load(read_file)

        for filename in os.listdir(PATH_DIRECOTRY):
            if filename.endswith("_heart.png"):
                relative_filename = PATH_DIRECOTRY+filename

                image = cv2.imread(relative_filename)
                locator = CVLocatorHeart()
                coordinates = locator.get_heart_cordinates(image)
                expected_coordinates = all_expected_coordinates[filename]

                self.assertAlmostEqual(expected_coordinates['x'], coordinates['x'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['y'], coordinates['y'], delta=DELTA_CORDINATES)

    def test_get_ellipse_coordinates(self):
        # Test get_heart_coordinates method of CV solution
        with open(PATH_DIRECOTRY + "ellipse_coordinates.json", "r") as read_file:
            all_expected_coordinates = json.load(read_file)

        for filename in os.listdir(PATH_DIRECOTRY):
            if filename.endswith("_ellipse.png"):
                relative_filename = PATH_DIRECOTRY+filename

                image = cv2.imread(relative_filename)
                locator = CVLocatorEllipse()
                coordinates = locator.get_ellipse_cordinates(image)
                expected_coordinates = all_expected_coordinates[filename]

                self.assertAlmostEqual(expected_coordinates['x_open'], coordinates['x_open'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['y_open'], coordinates['y_open'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['x_closed'], coordinates['x_closed'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['y_closed'], coordinates['y_closed'], delta=DELTA_CORDINATES)

    '''
    def test_get_lever_coordinates(self):
        # Test get_lever_coordinates method of CV solution
        with open(PATH_DIRECOTRY + "lever_coordinates.json", "r") as read_file:
            all_expected_coordinates = json.load(read_file)

        for filename in os.listdir(PATH_DIRECOTRY):
            if filename.endswith("_lever.png"):
                relative_filename = PATH_DIRECOTRY+filename

                image = cv2.imread(relative_filename)
                locator = CVLocator()
                cordinates = locator.get_lever_cordinates(image)
                expected_coordinates = all_expected_coordinates[filename]

                self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)
    '''


class TestTorpedoLocatorML(TestCase):
    def test_get_general_coordinates(self):
        pass
    def test_get_heart_coordinates(self):
        pass
    def test_get_ellipse_coordinates(self):
        pass
    def test_get_lever_coordinates(self):
        pass

if __name__ == '__main__':
    print("Torpedo tester")
    test_runner = TestRunner()
    results = test_runner.run()

    if results.failures:
        print("Tests fail")