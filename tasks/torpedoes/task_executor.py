"""
File contains interface for torpedoes task solver
"""
from tasks.task_executor_itf import ITaskExecutor
from tasks.torpedoes.locator import Locator
from communication.rpi_broker.distance import DistanceSensor
import time

config = {"x_offset": -5,  # torpedoes luncher offset x,y
          "y_offset": -5,
          "distance": 30,  # distance from ROV to target
          "shoting_distance":20,
          "distance_margin":3, #m argin for distance +- val
          "center_margin": 0.1,  # margin for overall object location in camera center
          "shoot_margin":0.05, # shoot margin distance % of camera
          "lin_vel_speeds": 0.3, # max linear speeds for ROV
          "refresh_loops_time":1 # while loops delay in sec
          }


class TaskExecutor(ITaskExecutor):
    """
    TaskExecutor inherit from this interface
    Every sub-algorithm also implement his interface
    """

    def __init__(self, movement_object, cameras_dict):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
        """
        self.movement_object = movement_object
        self.main_camera = cameras_dict['front_cam1']
        self.locator = Locator()
        self.depth_sensor = DistanceSensor()

    def run(self):
        """
        :return: 0 in case of failure, 1 in case of success
        """
        print("Torpedos task run!")
        self.setup_target()
        print("Target setup done")
        self.shoot_heart()
        print("Hearth shooted")
        # self.setup_lever()

        # self.shoot_ellipse()

    def setup_target(self):
        """
        Function setups ROV in front of target to execute task
        """
        global config
        requirements = {"distance": False, "x_centered": False, "y_centered": False}

        while not all(requirements.values()):
            img = self.main_camera.get_image()
            coords = self.locator.get_general_coordinates(img)
            dist = self.movement_object.get_front_distance()

            # Center target in camera center X
            if coords["x"] > config["center_margin"]:
                self.movement_object.set_lin_velocity(right=config["lin_vel_speeds"])
                requirements["x_centered"] = False
            elif coords["x"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(right=-config["lin_vel_speeds"])
                requirements["x_centered"] = False

            else:
                self.movement_object.set_lin_velocity(right=0)
                requirements["x_centered"] = True

            # Center target in camera center Y
            if coords["y"] > config["center_margin"]:
                self.movement_object.set_lin_velocity(up=-config["lin_vel_speeds"])
                requirements["y_centered"] = False
            elif coords["y"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(up=config["lin_vel_speeds"])
                requirements["y_centered"] = False
            else:
                self.movement_object.set_lin_velocity(up=0)
                requirements["y_centered"] = True

            # Setup distance
            if dist < config["distance"] - config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=-config["lin_vel_speeds"])
                requirements["distance"] = False
            elif dist > config["distance"] + config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=config["lin_vel_speeds"])
                requirements["distance"] = False
            else:
                self.movement_object.set_lin_velocity(front = 0)
                requirements["distance"] = True

            time.sleep(config["refresh_loops_time"])

    def shoot_heart(self):
        """
        Function setups ROV on heart and shoot.
        """ 
        global config
        requirements = {"distance": False, "heart_centered": False}

        while not all(requirements.values()):
            img = self.main_camera.get_image()
            gen_coords = self.locator.get_general_coordinates(img)
            heart_coords = self.locator.get_heart_coordinates(img)
            dist = self.movement_object.get_front_distance()

            # Setup  shooting distance
            if dist < config["shoting_distance"] - config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=-config["lin_vel_speeds"])
                requirements["distance"] = False
            elif dist > config["shoting_distance"] + config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=config["lin_vel_speeds"])
                requirements["distance"] = False
            else:
                self.movement_object.set_lin_velocity(front = 0)
                requirements["distance"] = True
        
            # Center heart to shoot in x
            # if  gen_coords["x"]-heart_coords["x"]

            time.sleep(config["refresh_loops_time"])



