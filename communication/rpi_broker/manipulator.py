class Manipulator:
    """
    Broker for manipulator
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def close_gripper(self):
        """
        Open gripper of ROV's robotic arm
        """
        self.rpi_reference.mainipulator_close_gripper()

    def open_gripper(self,):
        """
        Open gripper of ROV's robotic arm
        """
        self.rpi_reference.mainipulator_open_gripper()
