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

    def run(self):
        default_depth = 1.6
        time_surface = 5
        time_move_front = 20
        time_short_mov_front = 3

        self.logger.log("Pre-qualification: dive")
        self.movements.pid_set_depth(default_depth)
        self.movements.pid_turn_on()
        time.sleep(time_surface)

        self.logger.log("Pre-qualification: move front")
        self.movements.set_lin_velocity(front=50)
        time.sleep(time_move_front)
        self.movements.set_lin_velocity()

        self.logger.log("Pre-qualification: first rotate 90 degrees")
        self.movements.rotate_angle(yaw=90.0)
        
        self.logger.log("Pre-qualification: move front - short")
        self.movements.set_lin_velocity(front=50)
        self.movements.set_lin_velocity(time_short_mov_front)
        self.movements.set_lin_velocity()

        self.logger.log("Pre-qualification: second rotate 90 degrees")
        self.movements.rotate_angle(yaw=90.0)

        self.logger.log("Pre-qualification: second move front")
        self.movements.set_lin_velocity(front=50)
        time.sleep(time_move_front)
        self.movements.set_lin_velocity()

        self.logger.log("Pre-qualification: surface")
        self.movements.pid_set_depth(0.0)
        time.sleep(time_surface)
        self.movements.pid_turn_off()

        self.logger.log("Pre-qualification: end")
