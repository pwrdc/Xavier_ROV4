
class DepthSensor:
    """
    Depth Sensor
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def get_depth(self):
        '''
        Get current depth
        :return: depth as single integer in cm
        '''
        return self.rpi_reference.get_depth()
