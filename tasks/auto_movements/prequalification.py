import time

from tasks.task_executor_itf import ITaskExecutor

class Prequalification(ITaskExecutor):
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
        default_depth = 1.3
        time_surface = 5
        time_move_front = 60
        time_short_mov_front = 5
        
        time.sleep(2)

        self.movements.pid_yaw_turn_on()
        self.movements.set_ang_velocity()
        self.logger.log("Pre-qualification: dive")
        self.movements.pid_turn_on()
        self.movements.pid_set_depth(default_depth)
        time.sleep(time_surface)

        time.sleep(1)

        # first front
        self.logger.log("Pre-qualification: move front")
        self.movements.set_lin_velocity(front=30)
        time.sleep(time_move_front)
        self.movements.set_lin_velocity()
        
        
        #rotation
        time.sleep(1)
        #self.movements.pid_yaw_turn_off()
        self.logger.log("Pre-qualification: first rotate 90 degrees")
        #self.movements.set_ang_velocity(yaw=40)
        self.movements.pid_set_yaw(self.ahrs.get_yaw()+90)
        time.sleep(2)
        self.movements.set_ang_velocity()
        
        # short front
        #self.movements.pid_yaw_turn_on()
        self.logger.log("Pre-qualification: move front - short")
        self.movements.set_lin_velocity(front=30)
        time.sleep(time_short_mov_front)
        self.movements.set_lin_velocity()

        # second rotation
        time.sleep(1)
        #self.movements.pid_yaw_turn_off()
        self.logger.log("Pre-qualification: second rotate 90 degrees")
        #self.movements.set_ang_velocity(yaw=40)
        self.movements.pid_set_yaw(self.ahrs.get_yaw()+90)
        time.sleep(2)
        self.movements.set_ang_velocity()
        #self.movements.pid_yaw_turn_on()

        # second long front
        time.sleep(1)
        self.logger.log("Pre-qualification: second move front")
        self.movements.set_lin_velocity(front=30)
        time.sleep(time_move_front-2)
        self.movements.set_lin_velocity()

        # surface
        self.logger.log("Pre-qualification: surface")
        self.movements.pid_set_depth(0.0)
        time.sleep(time_surface)
        self.movements.pid_turn_off()
        self.movements.pid_yaw_turn_off()

        self.logger.log("Pre-qualification: end")
