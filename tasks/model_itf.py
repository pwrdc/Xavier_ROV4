import  abc

class Model_itf(metaclass=abc.ABCMeta):
    """
    Interfce for algorithm for tasks
    """
    @abc.abstractmethod
    def load(self):
        """ method for load model from file,
            in algorithm classes do nothing
        """
        pass
    @abc.abstractmethod
    def predict(self):
        """ method for access data from algorithm
        """
        pass