"""
Module includes IMovements
"""

class Movements:
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def set_lin_velocity(self, front=0, right=0, up=0):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """
        self.rpi_reference.set_lin_velocity(front, right, up)

    def set_ang_velocity(self, roll=0, pitch=0, yaw=0):
        """
        Set angular velocity as 100% of engines power
        @param: roll int in range [-100, 100], case negative - reverse direction
        @param: pitch int in range [-100, 100], case negative - reverse direction
        @param: yaw int in range [-100,100], case negative - reverse direction
        """
        self.rpi_reference.set_ang_velocity(roll, pitch, yaw)

    def move_distance(self, front=0.0, right=0.0, up=0.0):
        """
        Make precise linear movement, valeues in meters
        @param: front float in range [-10, 10], case negative value move back
        @param: right float in range [-10, 10], case negative value move down
        @param: up float in range [-10,10], case negative value move down

        Not shure if it is going to work correctly
        """
        self.rpi_reference.move_distance(front, right, up)

    def rotate_angle(self, roll=0.0, pitch=0.0, yaw=0.0):
        """
        Make precise angular movement
        @param: roll float in range [-360, 360], case negative - reverse direction
        @param: pitch float in range [-360, 360], case negative - reverse direction
        @param: yaw flaot in range [-360, 360], case negative - reverse direction
        """
        self.rpi_reference.rotate_angle(roll, pitch, yaw)
        
    def pid_turn_on(self):
        """
        Turn on PID
        """
        self.rpi_reference.pid_depth_turn_on()

    def pid_turn_off(self):
        """
        Turn off PID
        """
        self.rpi_reference.pid_depth_turn_off()

    def pid_hold_depth(self):
        """
        Set the current depth as the default depth
        Function DOESN'T activate pid, use pid_turn_on additionally
        """
        self.rpi_reference.pid_hold_depth()

    def pid_set_depth(self, depth):
        """
        Set depth, function DOESN'T activate pid, use pid_turn_on additionally
        :param: depth - float - target depth for PID
        """
        self.rpi_reference.pid_set_depth(depth)

    def pid_yaw_turn_on(self):
        self.rpi_reference.pid_yaw_turn_on()

    def pid_yaw_turn_off(self):
        self.rpi_reference.pid_yaw_turn_on()

    def pid_set_yaw(self, yaw):
        self.rpi_reference.pid_set_yaw(yaw)
