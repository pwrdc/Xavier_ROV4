import time

from tasks.task_executor_itf import ITaskExecutor


class TestAHRS(ITaskExecutor):
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
        default_depth = 1.0
        time_surface = 5
        time_move_front = 20
        time_rotate = 3

        time.sleep(2)

        self.movements.pid_yaw_turn_on()
        self.movements.set_ang_velocity()
        self.logger.log("test_ahrs: dive")
        self.movements.pid_turn_on()
        self.movements.pid_set_depth(default_depth)
        time.sleep(time_surface)

        # first rotation
        time.sleep(1)
        self.logger.log("test_ahrs: rotate cw")
        self.movements.set_ang_velocity(yaw=30)
        time.sleep(time_rotate)
        self.movements.set_ang_velocity()

        # second rotation
        time.sleep(1)
        self.logger.log("test_ahrs: rotate ccw")
        self.movements.set_ang_velocity(yaw=-30)
        time.sleep(time_rotate)
        self.movements.set_ang_velocity()

        # front
        time.sleep(1)
        self.logger.log("test_ahrs: move front")
        self.movements.set_lin_velocity(front=30)
        time.sleep(time_move_front)
        self.movements.set_lin_velocity()

        # surface
        time.sleep(1)
        self.logger.log("test_ahrs: surface")
        self.movements.pid_set_depth(0.0)
        time.sleep(time_surface)
        self.movements.pid_turn_off()
        self.movements.pid_yaw_turn_off()

        self.logger.log("test_ahrs: end")
