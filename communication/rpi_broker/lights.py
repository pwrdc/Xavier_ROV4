class Lights:
    """
    Control ROV's Lights brightness
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def power_lights(self):
        """
        Check if torpedo is ready to lunch
        :return: True when torpedo is ready to lunch
        """
        self.rpi_reference.power_lights()

    def turn_on(self):
        """
        Lunch single torpedo
        """
        self.rpi_reference.lights_turn_on()

    def turn_off(self):
        """
        Lunch single torpedo
        """
        self.rpi_reference.lights_turn_off()
