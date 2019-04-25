import time

class TurnROV():

    SLEEP_TIME = 0.1
    #loop sleep time
    STOP_SPEED = 1
    #difference between current angle and previous angle that
    #is thought as boat is stopped
    DEMANDED_ACCURACY = 5
    #demanded turn accuracy in degrees

    @staticmethod
    def turn(demanded_angle, rpi_ref):
        """
        Turns the AUV to requested angle
        :param req_angle: demanded angle to turn
        :param rpi_ref: Pyro4 reference to control the AUV
        """
        current_values = rpi_ref.get_rotation()
        cur_angle = current_values['yaw']
        prev_angle = 0
        req_angle = cur_angle + demanded_angle
        
        while abs(req_angle-cur_angle)>TurnROV.DEMANDED_ACCURACY or abs(cur_angle-prev_angle)>TurnROV.STOP_SPEED:
            speed = (demanded_angle/180)*((req_angle-cur_angle)/demanded_angle)
            #SPEED CALCULATION:
            #1. for max demanded turn (90 degree) power is limited to 0.5
            #decreases speed as the difference between requested and current angle drops down
            if abs(speed)<= 0.5:
                rpi_ref.set_angular_velocity(0,0,speed)
            elif speed >0.5:
                rpi_ref.set_angular_velocity(0,0,0.5)
            else:
                rpi_ref.set_angular_velocity(0,0,-0.5)
            time.sleep(TurnROV.SLEEP_TIME)
            prev_angle = cur_angle
            current_values = rpi_ref.get_rotation()
            cur_angle = current_values['yaw']