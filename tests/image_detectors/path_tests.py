import cv2
import os
import json
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from tasks.path.locator.cv_solution.locator import Locator as CVLocator

PATH_DIRECOTRY = "./tests/image_detectors/path/"
DELTA_CORDINATES = 0.05
DELTA_ANGLE = 5

class TestRunner:
    def __init__(self):
        self.runner = TextTestRunner(verbosity=2)

    def run(self):
        test_suite = TestSuite(tests=[
            makeSuite(TestPathLocatorCV)#,
            #makeSuite(TestPathLocatorML)
        ])
        return self.runner.run(test_suite)

class TestPathLocatorCV(TestCase):
    def test_get_path_cordinates(self):
        # Test get_path_cordinates method of CV solution
        with open(PATH_DIRECOTRY + "coordinates.json", "r") as read_file:
            all_expected_coordinates = json.load(read_file)

        for filename in os.listdir(PATH_DIRECOTRY):
            if filename.endswith(".png"):
                relative_filename = PATH_DIRECOTRY+filename

                image = cv2.imread(relative_filename)
                locator = CVLocator()
                cordinates = locator.get_path_cordinates(image)
                expected_coordinates = all_expected_coordinates[filename]

                self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)


    def test_get_rotation_angle(self):
        # Test get_rotation_angle method of CV solution
        with open(PATH_DIRECOTRY + "angles.json", "r") as read_file:
            all_expected_angles = json.load(read_file)

        for filename in all_expected_angles:
            image = cv2.imread("./path" + filename)
            locator = CVLocator()
            angle = locator.get_rotation_angle(image)

            expected_angle = all_expected_angles[filename]

            self.assertAlmostEqual(expected_angle, angle, delta=DELTA_ANGLE)


class TestPathLocatorML(TestCase):
    def test_get_path_cordinates(self):
        pass


    def test_get_rotation_angle(self):
        pass

if __name__ == '__main__':
    print("Path tester")
    test_runner = TestRunner()
    results = test_runner.run()

    if results.failures:
        print("Tests fail")