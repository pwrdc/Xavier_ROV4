import time

from tasks.task_executor_itf import ITaskExecutor

default_depth = 1.3
time_surface = 4
time_move_front = 20
first_rot = 220
second_rot = 180

TIMEOUT_1ST_BUYOY = 40
TIMEOUT_2ST_BUYOY = 40

ANGLE_1ST_BUYOY = 50
ANGLE_2ST_BUYOY = 30
NEUTRAL_ROTATION = 42

MAX_FRONT_VELOCITY = 0.25

class BuoysMrn(ITaskExecutor):
    def __init__(self, control_dict, sensors_dict, cameras_dict, main_logger):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
        """
        self.control_dict = control_dict
        self.sensors_dict = sensors_dict
        self.cameras_dict = cameras_dict
        self.logger = main_logger
        self.movements = control_dict['movements']
        self.ahrs = sensors_dict['ahrs']

        self.distance = sensors_dict['distance'].get_front_distance

        self.front_hit_time = 0.0

    def run(self):
        TIME_TO_REACH_BUOY = 20

        self.movements.pid_set_depth(3)
        time.sleep(2)

        self.movements.set_lin_velocity(front=0.25)
        time.sleep(TIME_TO_REACH_BUOY)
        self.movements.set_lin_velocity()

        time_of_hit = self.hit_buyoy(TIMEOUT_1ST_BUYOY, ANGLE_1ST_BUYOY)
        self.return_from_hit_buyoy(time_of_hit)

        time_of_hit = self.hit_buyoy(TIMEOUT_1ST_BUYOY, ANGLE_2ST_BUYOY)
        self.return_from_hit_buyoy(time_of_hit)
        
        self.go_around()

    def hit_buyoy(self, timeout_to_hit, buyoy_angle):
        '''
        :return: time of manuver 
        '''
        TIMEOUT_FOR_HIT = 20 

        HIT_DISTANCE = 10

        start_time = time.time()

        self.movements.pid_set_yaw(buyoy_angle)
        self.movements.set_lin_velocity(front=MAX_FRONT_VELOCITY)

        hit_time = time.time() + TIMEOUT_FOR_HIT
        while True:
            if self.distance() < HIT_DISTANCE:
                time.sleep(0.5)
                break
            
            if time.time() > hit_time:
                break

            time.sleep(0.1)

        return time.time() - start_time

    def return_from_hit_buyoy(self, time_of_return):
        self.movements.pid_set_yaw(time_of_return)
        self.movements.set_lin_velocity(front=-MAX_FRONT_VELOCITY)
        time.sleep(time_of_return)
        self.movements.set_lin_velocity()

    def go_around(self):
        self.movements.move_distance(right=2)
        self.movements.move_distance(front=3)
        self.movements.move_distance(right=-2)
