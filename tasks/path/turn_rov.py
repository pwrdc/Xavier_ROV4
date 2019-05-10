import time

class PathHandle():

    SLEEP_TIME = 0.1
    #loop sleep time
    STOP_SPEED = 1
    #difference between current angle and previous angle that
    #is thought as boat is stopped
    DEMANDED_ACCURACY = 5
    #demanded turn accuracy in degrees
    DEMANDED_POSITIONING = 0.05
    #how accurate has AUV be above the path (0;1)
    MAX_SPEED = 0.05
    #maximum gradient of velocity that is considered static
    TURN_DETECTION = 30
    #value of angle that is interpreted as path turn
    AFTER_TURN_CHECKS = 5
    #how many times ROV will be centered on path after turn

    def __init__(self,path_locator,rpi_ref):
        '''
        Handling whole positioning, swimming along and turning on the path
        1. Cente on path
        2. Turn into path direction
        3. Swim along until path curve is finded (while loop)
        4. Do the turn
        5. Centre on path
        6. Swim forward until end of path (10*SLEEP_TIME)

        Parameters described in class methods
        '''
        PathHandle.centre_on_path(path_locator,rpi_ref)
        PathHandle.turn(path_locator.get_rotation_angle(path_locator.captureSingleFrame()),rpi_ref)
        while abs(path_locator.get_rotation_angle(path_locator.captureSingleFrame()))<PathHandle.TURN_DETECTION:
            rpi_ref.set_lin_velocity(0.3,0,0)
            time.sleep(PathHandle.SLEEP_TIME)
        PathHandle.turn(path_locator.get_rotation_angle(path_locator.captureSingleFrame()),rpi_ref)
        PathHandle.centre_on_path(path_locator,rpi_ref)
        rpi_ref.set_lin_velocity(0.3,0,0)
        time.sleep(PathHandle.SLEEP_TIME*10)

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
        
        while abs(req_angle-cur_angle)>PathHandle.DEMANDED_ACCURACY or abs(cur_angle-prev_angle)>PathHandle.STOP_SPEED:
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
            time.sleep(PathHandle.SLEEP_TIME)
            prev_angle = cur_angle
            current_values = rpi_ref.get_rotation()
            cur_angle = current_values['yaw']

    @staticmethod
    def centre_on_path(path_locator, rpi_ref):
        """
        Sets ROV4 above the center of the path.
        :param path_locator: object of class that gets path position and angle from an image
        :param rpi_ref: Pyro4 reference to control the AUV
        """
                
        path_coordinates = path_locator.get_path_cordinates(path_locator.captureSingleFrame())
        speed = 0
        previous_x = 0
        previous_y = 0

        while (abs(path_coordinates['x'])>PathHandle.DEMANDED_POSITIONING or
        abs(path_coordinates['y'])>PathHandle.DEMANDED_POSITIONING) or speed > PathHandle.MAX_SPEED:
            rpi_ref.set_lin_velocity(path_coordinates['y']/2,path_coordinates['x']/2,0)
            speed = ((path_coordinates['y']-previous_y)**2+(path_coordinates['x']-previous_x)**2)**0.5
            previous_y = path_coordinates['y']
            previous_x = path_coordinates['x']
            path_locator.get_path_cordinates(path_locator.captureSingleFrame())
