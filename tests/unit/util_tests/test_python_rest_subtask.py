import unittest
from utils.python_rest_subtask import PythonRESTSubtask

class TestPythonRestSubtask(unittest.TestCase):
    def setUp(self):
        pass

    def test_waitReady_timeout(self):
        task = PythonRESTSubtask()


if __name__ == '__main__':
    unittest.main()