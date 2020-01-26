import cv2
import os
import json
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from tasks.robosub19.garlic.locator.cv_solution.locator import Locator as CVLocator

PATH_DIRECOTRY = "./tests/image_detectors/robosub19/garlic/"
DELTA_CORDINATES = 0.05

class TestRunner:
	def __init__(self):
		self.runner = TextTestRunner(verbosity=2)

	def run(self):
		test_suite = TestSuite(tests=[
			makeSuite(TestGarlicLocatorCV)#,
			#makeSuite(TestGarlicLocatorML)
		])
		return self.runner.run(test_suite)

class TestGarlicLocatorCV(TestCase):
	def test_get_garlic_coordinates(self):
		# Test get_garlic_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "garlic_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_garlic.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_garlic_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_garlic_handle_coordinates(self):
		# Test get_garlic_handle_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "garlic_handle_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_garlic_handle.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_garlic_handle_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)


class TestGarlicLocatorML(TestCase):
	def test_get_garlic_coordinates(self):
		pass
	def test_get_garlic_handle_coordinates(self):
		pass

if __name__ == '__main__':
	print("Garlic tester")
	test_runner = TestRunner()
	results = test_runner.run()

	if results.failures:
		print("Tests fail")