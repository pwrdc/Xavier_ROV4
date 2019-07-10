import Pyro4


class Communication:

    def __init__(self):
        self.rpi_reference = Pyro4.Proxy("PYRONAME:RPI_communication")