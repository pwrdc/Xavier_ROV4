class Dropper:
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def drop_marker(self):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """
        self.rpi_reference.drop_marker()
