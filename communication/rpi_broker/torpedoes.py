class Torpedoes:
    """
    Control ROV's torpedo launcher
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def is_torpedo_ready(self):
        """
        Check if torpedo is ready to lunch
        :return: True when torpedo is ready to lunch
        """
        self.rpi_reference.is_torpedo_ready()

    def fire(self):
        """
        Lunch single torpedo
        """
        self.rpi_reference.torpedo_fire()
