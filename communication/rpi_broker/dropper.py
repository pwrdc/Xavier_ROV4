
class Dropper:
    """
    Depth Sensor
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def drop_marker(self):
        return self.rpi_reference.drop_marker()
