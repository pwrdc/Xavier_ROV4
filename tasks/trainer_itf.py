"""
File contains interface for triner class
"""
import  abc

class ITrainer(metaclass=abc.ABCMeta):
    """
    Interfce for trainer class
    """
    @abc.abstractmethod
    def fit(self):
        """ method for training
        """
        pass
