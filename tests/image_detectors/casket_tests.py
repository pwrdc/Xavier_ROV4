import cv2
import os
import json
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from tasks.casket.locator.cv_solution.locator import Locator as CVLocator

PATH_DIRECOTRY = "./tests/image_detectors/casket/"
DELTA_CORDINATES = 0.05

class TestRunner:
	def __init__(self):
		self.runner = TextTestRunner(verbosity=2)

	def run(self):
		test_suite = TestSuite(tests=[
			makeSuite(TestCasketLocatorCV)#,
			#makeSuite(TestCasketLocatorML)
		])
		return self.runner.run(test_suite)

class TestCasketLocatorCV(TestCase):
	def test_get_open_coffin_coordinates(self):
		# Test get_open_coffin_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "open_coffin_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_open_coffin.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_open_coffin_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_closed_coffin_coordinates(self):
		# Test get_closed_coffin_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "closed_coffin_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_closed_coffin.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_closed_coffin_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_coffin_lock_coordinates(self):
		# Test coffin_lock_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "coffin_lock_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_coffin_lock.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_coffin_lock_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_vampire_coordinates(self):
		# Test get_vampire_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "vampire_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_vampire.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_vampire_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)


class TestCasketLocatorML(TestCase):
	def test_get_open_coffin_coordinates(self):
		pass
	def test_get_closed_coffin_coordinates(self):
		pass
	def test_get_coffin_lock_coordinates(self):
		pass
	def test_get_vampire_coordinates(self):
		pass

if __name__ == '__main__':
	print("Casket tester")
	test_runner = TestRunner()
	results = test_runner.run()

	if results.failures:
		print("Tests fail")