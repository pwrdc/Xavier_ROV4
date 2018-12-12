import abc

class Commmunication_itf(metaclass=abc.ABCMeta):
    """
    Comunicaton
    """
    @abc.abstractmethod
    def foo(self):
        """...
        """
        pass
