import time

from tasks.task_executor_itf import ITaskExecutor

default_depth = 1.3
time_surface = 4
time_move_front = 20
first_rot = 220
second_rot = 180

TIMEOUT_1ST_buoy = 40
TIMEOUT_2ST_buoy = 40

ANGLE_1ST_buoy = 230
ANGLE_2ST_buoy = 180
NEUTRAL_ANGLE = 190

MAX_FRONT_VELOCITY = 0.25

class GateMrn(ITaskExecutor):
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
        time_of_hit = self.hit_buoy(TIMEOUT_1ST_buoy, ANGLE_1ST_buoy)
        self.return_from_hit_buoy(time_of_hit)

        time_of_hit = self.hit_buoy(TIMEOUT_2ST_buoy, ANGLE_2ST_buoy)
        self.return_from_hit_buoy(time_of_hit)
        
        self.miss_buoys()
        
        
    def hit_buoy(self, timeout_to_hit, buoy_angle):
        '''
        :return: time of manuver 
        '''
        TIME_TO_HIT = 40
        TIMEOUT_FOR_HIT = 40 

        HIT_DISTANCE = 10

        start_time = time.time()

        self.movements.pid_set_yaw(buoy_angle)
        self.movements.set_lin_velocity(front=MAX_FRONT_VELOCITY)

        hit = False
        hit_time = time.time() + TIMEOUT_FOR_HIT
        while not hit:
            if self.distance < HIT_DISTANCE:
                time.sleep(2)
                break
            
            if time.time() > hit_time:
                break

            time.sleep(0.1)

        self.movements.set_lin_velocity()
        return time.time() - start_time

    def return_from_hit_buoy(self, time_of_return):
        self.movements.pid_set_yaw(time_of_return)
        self.movements.set_lin_velocity(front=-MAX_FRONT_VELOCITY)
       
        time.sleep(time_of_return)
        self.movements.set_lin_velocity()

    def miss_buoys(self):
        RIGHT_MOVEMENT_TIME = 20
        FRONT_MOVEMENT_TIME = 20

        # right
        self.movements.pid_set_yaw(NEUTRAL_ANGLE)
        self.movements.set_lin_velocity(right=MAX_FRONT_VELOCITY)
        time.sleep(RIGHT_MOVEMENT_TIME)

        # front
        self.movements.set_lin_velocity(front=MAX_FRONT_VELOCITY)
        time.sleep(FRONT_MOVEMENT_TIME)

        # left
        self.movements.set_lin_velocity(right=MAX_FRONT_VELOCITY)
        time.sleep(RIGHT_MOVEMENT_TIME)


