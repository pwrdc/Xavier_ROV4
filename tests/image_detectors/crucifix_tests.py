import cv2
import os
import json
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from tasks.crucifix.locator.cv_solution.locator import Locator as CVLocator

PATH_DIRECOTRY = "./tests/image_detectors/crucifix/"
DELTA_CORDINATES = 0.05
DELTA_ANGLE = 5

class TestRunner:
    def __init__(self):
        self.runner = TextTestRunner(verbosity=2)

    def run(self):
        test_suite = TestSuite(tests=[
            makeSuite(TestCrucifixLocatorCV)#,
            #makeSuite(TestCrucifixLocatorML)
        ])
        return self.runner.run(test_suite)

class TestCrucifixLocatorCV(TestCase):
    def test_get_intersection_cordinates(self):
        # Test get_crucifix_cordinates method of CV solution
        with open(PATH_DIRECOTRY + "coordinates.json", "r") as read_file:
            all_expected_coordinates = json.load(read_file)

        for filename in os.listdir(PATH_DIRECOTRY):
            if filename.endswith(".png"):
                relative_filename = PATH_DIRECOTRY+filename

                image = cv2.imread(relative_filename)
                locator = CVLocator()
                cordinates = locator.get_intersection_cordinates(image)
                expected_coordinates = all_expected_coordinates[filename]

                self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
                self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)



class TestCrucifixLocatorML(TestCase):
    def test_get_intersection_cordinates(self):
        pass


if __name__ == '__main__':
    print("Crucifix tester")
    test_runner = TestRunner()
    results = test_runner.run()

    if results.failures:
        print("Tests fail")