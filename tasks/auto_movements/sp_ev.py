'''
Run code from main Xavier_ROV4 directory
'''
import time
from tasks.task_executor_itf import ITaskExecutor

DEFAULT_DEPTH = 1
DIPPING_TIME = 5
TIME_TO_CROSS_POOL = 15
TIME_TO_CHANGE_PATH = 4
TIME_TO_TURN = 2
TURNS_NUMBER = 5
FRONT_SPEED = 30
TURN_SPEED = 50

class Sponsor_Event(ITaskExecutor):
   
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

    def run(self):
        time.sleep(2)

        #self.movements.pid_yaw_turn_on()
        self.turn(1)  #obrót na powierzchni

        self.movements.pid_turn_on()
        self.movements.pid_set_depth(DEFAULT_DEPTH)  #zanurzenie
        self.logger.log("Sponsor_Event: dipping")
        time.sleep(DIPPING_TIME)

        i=0
        for i in range(TURNS_NUMBER):
            #naprzód
            self.forward()
            #w lewo
            self.turn(-1)
            #krótko naprzód
            self.short_forward()
            #w lewo
            self.turn(-1)
            #naprzód
            self.forward()
            #w prawo
            self.turn(1)
            #krótko naprzód
            self.short_forward()
            #w prawo
            self.turn(1)

        self.logger.log("Sponsor_Event: effusion")
        self.movements.pid_set_depth(0.0)
        time.sleep(DIPPING_TIME)
        self.movements.pid_turn_off()
        #self.movements.pid_yaw_turn_off()
        self.logger.log("Sponsor_Event: end")



    def forward(self):
        self.movements.set_lin_velocity(front=FRONT_SPEED)
        self.logger.log("Sponsor_Event: forward")
        time.sleep(TIME_TO_CROSS_POOL)
        self.movements.set_lin_velocity(front=0)

    def short_forward(self):
        self.movements.set_lin_velocity(front=FRONT_SPEED)
        self.logger.log("Sponsor_Event: short forward")
        time.sleep(TIME_TO_CHANGE_PATH)
        self.movements.set_lin_velocity(front=0)

    def turn(self, direction):
        '''
        @param: direction -1=left turn; 1=right turn
        '''
        self.movements.set_ang_velocity(yaw=TURN_SPEED*direction)
        self.logger.log("Sponsor_Event: turn")
        time.sleep(TIME_TO_TURN)
        self.movements.set_ang_velocity(yaw=0)
