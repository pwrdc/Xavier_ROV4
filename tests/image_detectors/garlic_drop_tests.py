import cv2
import os
import json
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from tasks.garlic_drop.locator.cv_solution.locator import Locator as CVLocator

PATH_DIRECOTRY = "./tests/image_detectors/garlic_drop/"
DELTA_CORDINATES = 0.05

class TestRunner:
	def __init__(self):
		self.runner = TextTestRunner(verbosity=2)

	def run(self):
		test_suite = TestSuite(tests=[
			makeSuite(TestGarlicDropLocatorCV)#,
			#makeSuite(TestGarlicDropLocatorML)
		])
		return self.runner.run(test_suite)

class TestGarlicDropLocatorCV(TestCase):
	def test_get_drop_zone_coordinates(self):
		# Test get_drop_zone_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "drop_zone_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_drop_zone.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_drop_zone_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

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

	def test_wolf_coordinates(self):
		# Test wolf_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "wolf_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_wolf.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_wolf_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_bat_coordinates(self):
		# Test get_bat_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "bat_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_bat.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_bat_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)


class TestGarlicDropLocatorML(TestCase):
	def test_get_drop_zone_coordinates(self):
		pass
	def test_get_lever_coordinates(self):
		pass
	def test_get_wolf_coordinates(self):
		pass
	def test_get_bat_coordinates(self):
		pass

if __name__ == '__main__':
	print("GarlicDrop tester")
	test_runner = TestRunner()
	results = test_runner.run()

	if results.failures:
		print("Tests fail")