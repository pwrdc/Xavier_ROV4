from utils.project_managment import PROJECT_ROOT
from subprocess import Popen
from typing import Optional
import atexit

class PythonSubtask:
    def __init__(self, path: str):
        """
        :param path: Path to python script that is run, relative to project root
        """
        path = path.replace("/", ".").replace(".py", "")

        self.path = path
        self.process: Optional[Popen] = None

    def start(self, arguments: str = "") -> bool:
        """
        Starts a python subtask
        :param arguments: Arguments provided to the running script
        :return: None
        """
        if self.process is None:
            try:
                self.process = Popen(["python3", "-m", self.path, *arguments.split(" ")], cwd=PROJECT_ROOT)
                atexit.register(self.process.terminate)
                return True
            except:
                return False

    def kill(self):
        """
        Kills running subtask
        :return: None
        """
        if self.process is not None:
            while self.process.poll() is None:
                self.process.kill()
            self.process = None

    @staticmethod
    def run(path: str, arguments=""): # -> optional[PythonSubtask]
        """
        Factory method for creating and starting a python subtask
        :param path: Path to python script that is run, relative to project root
        :param arguments: arguments provided to python script
        :return: PythonSubtask class with task already started
        """
        task = PythonSubtask(path)

        if task.start(arguments):
            return task
        else:
            return None

    def __del__(self):
        self.kill()
