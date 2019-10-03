
class DistanceSensor:
    """
    Distance Sensor
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def get_front_distance(self):
        '''
        Get distance from obstacle in front of ROV

        :return: distance in cm as single float
        '''
        return 300#return float(self.rpi_reference.get_front_distance())
