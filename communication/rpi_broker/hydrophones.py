
class Hydrophones:
    """
    Depth Sensor
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def get_angle(self):
        return self.rpi_reference.get_angle()
