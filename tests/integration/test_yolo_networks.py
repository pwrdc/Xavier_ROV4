import unittest
from utils.python_rest_subtask import PythonRESTSubtask
from tasks.gate.locator.ml_solution.yolo_soln import YoloGateLocator
from tasks.path.locator.ml_solution.yolo_soln import YoloPathLocator
import numpy as np

class TestPythonRestSubtask(unittest.TestCase):
    def setUp(self):
        pass

    def test_memory_stability(self):
        img = np.random.randn(400, 400, 3) * 255
        
        for i in range(20):
            YoloGateLocator().get_gate_cordinates(img)
            YoloPathLocator().get_path_cordinates(img)
    
    def test_all_networks(self):
        img = np.random.randn(400, 400, 3) * 255

        YoloGateLocator().get_gate_cordinates(img)
        YoloPathLocator().get_path_cordinates(img)


if __name__ == '__main__':
    unittest.main()