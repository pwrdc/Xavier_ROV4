import cv2
import os
import json
from unittest import TestCase, TestSuite, TextTestRunner, makeSuite

from tasks.buoys.locator.cv_solution.locator import Locator as CVLocator

PATH_DIRECOTRY = "./tests/image_detectors/buoys/"
DELTA_CORDINATES = 0.05

class TestRunner:
	def __init__(self):
		self.runner = TextTestRunner(verbosity=2)

	def run(self):
		test_suite = TestSuite(tests=[
			makeSuite(TestBuoyLocatorCV)#,
			#makeSuite(TestBuoyLocatorML)
		])
		return self.runner.run(test_suite)

class TestBuoyLocatorCV(TestCase):
	def test_get_jiangshi_coordinates(self):
		# Test get_jiangshi_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "jiangshi_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_jiangshi.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_jiangshi_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_rectangle_coordinates(self):
		# Test get_rectangle_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "rectangle_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_rectangle.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_rectangle_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_draugr_wall_coordinates(self):
		# Test get_draugr_wall_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "draugr_wall_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_draugr_wall.png"):
				relative_filename = PATH_DIRECOTRY+filenamedr

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_draugr_wall_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_aswang_wall_coordinates(self):
		# Test get_aswang_wall_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "aswang_wall_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_aswang_wall.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_aswang_wall_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)

	def test_get_vetelas_wall_coordinates(self):
		# Test get_vetelas_wall_coordinates method of CV solution
		with open(PATH_DIRECOTRY + "vetelas_wall_coordinates.json", "r") as read_file:
			all_expected_coordinates = json.load(read_file)

		for filename in os.listdir(PATH_DIRECOTRY):
			if filename.endswith("_vetelas_wall.png"):
				relative_filename = PATH_DIRECOTRY+filename

				image = cv2.imread(relative_filename)
				locator = CVLocator()
				cordinates = locator.get_vetelas_wall_cordinates(image)
				expected_coordinates = all_expected_coordinates[filename]

				self.assertAlmostEqual(expected_coordinates['x'], cordinates['x'], delta=DELTA_CORDINATES)
				self.assertAlmostEqual(expected_coordinates['y'], cordinates['y'], delta=DELTA_CORDINATES)


class TestBuoyLocatorML(TestCase):
	def test_get_jiangshi_coordinates(self):
		pass
	def test_get_rectangle_coordinates(self):
		pass
	def test_get_draugr_wall_coordinates(self):
		pass
	def test_get_aswang_wall_coordinates(self):
		pass
	def test_get_vetalas_wall_coordinates(self):
		pass

if __name__ == '__main__':
	print("Buoy tester")
	test_runner = TestRunner()
	results = test_runner.run()

	if results.failures:
		print("Tests fail")