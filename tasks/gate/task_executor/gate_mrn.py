import time

from tasks.task_executor_itf import ITaskExecutor
from definitions import ANGLE_GATE, TIME_GATE_FRONT_FIRST, TIME_GATE_FRONT_SECOND

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
        self.movements = control_dict # ['movements']
        self.ahrs = sensors_dict['ahrs']

    def run(self):
        default_depth = 1.5
        time_surface = 4
        time_move_front = TIME_GATE_FRONT_FIRST #50
        time_second_front = TIME_GATE_FRONT_SECOND #40
        default_rotation = ANGLE_GATE#173 # IN Beta: 180 #ind d 20
        
        time.sleep(2)

        self.movements.pid_yaw_turn_on()
        self.movements.set_ang_velocity()
        self.movements.pid_set_yaw(default_rotation)
        self.logger.log("Gate_mrn: dive")
        self.movements.pid_turn_on()
        self.movements.pid_set_depth(default_depth)
        time.sleep(time_surface)

        time.sleep(1)

        #rotation
        time.sleep(1)
        #self.movements.pid_yaw_turn_off()
        self.logger.log("Gate_mrn: first rotate 90 degrees")
        #self.movements.set_ang_velocity(yaw=40)
        time.sleep(2)
        self.movements.set_ang_velocity()

        time.sleep(1)

        # first front
        self.logger.log("Gate_mrn: move front")
        self.movements.set_lin_velocity(front=30)
        time.sleep(time_move_front)
        self.movements.set_lin_velocity()
        

        # second rotation
        time.sleep(1)
        #self.movements.pid_yaw_turn_off()
        self.logger.log("Gate_mrn: second rotate 90 degrees")
        #self.movements.set_ang_velocity(yaw=40)
        self.movements.pid_set_yaw(default_rotation+180)
        time.sleep(4)
        self.movements.set_ang_velocity()
        #self.movements.pid_yaw_turn_on()
        self.movements.pid_set_yaw(default_rotation+360)
        time.sleep(4)
        self.movements.set_ang_velocity()

        self.logger.log("Gate_mrn: rotate 720 degrees")
        #self.movements.set_ang_velocity(yaw=40)
        self.movements.pid_set_yaw(default_rotation+540)
        time.sleep(4)
        self.movements.set_ang_velocity()
        #self.movements.pid_yaw_turn_on()
        self.movements.pid_set_yaw(default_rotation+720)
        time.sleep(4)
        self.movements.set_ang_velocity()



        # second long front
        time.sleep(1)
        self.logger.log("Gate_mrn: second move front")
        self.movements.set_lin_velocity(front=25)
        time.sleep(time_second_front)
        self.movements.set_lin_velocity()

        return 0
