"""
File contains interface for model class
"""
import  abc

class IModel(metaclass=abc.ABCMeta):
    """
    Interfce for algorithm for tasks
    """
    @abc.abstractmethod
    def load(self):
        """ method for loading model from file,
            in algorithm class do nothing
        """
        pass
    @abc.abstractmethod
    def predict(self):
        """ method for runing prediction
        """
        pass
<<<<<<< HEAD

    @abc.abstractmethod
    def release(self):
        """ method for releasing model resources
        """
=======
>>>>>>> 31e0dcd5d3ae73f0c261fe9f28c6d26b70c9839b
