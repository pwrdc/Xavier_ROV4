"""
File contains interface for torpedoes task solver
"""
from tasks.task_executor_itf import ITaskExecutor
from tasks.torpedoes.locator import Locator
import time

config = {"x_offset": -0.01,  # torpedoes luncher offset x,y 1=100%
          "y_offset": -0.2,
          "distance": 30,  # distance from ROV to target
          "shoting_distance": 20,
          "distance_margin": 3,  # m argin for distance +- val
          "center_margin": 0.1,  # margin for overall object location in camera center 1=100%
          "shoot_margin": 0.05,  # shoot margin distance % of camera
          "lin_vel_speeds": 0.3,  # max linear speeds for ROV
          "speed_multiplier": 1, # value times distance element to center 
          "refresh_loops_time": 1  # while loops delay in sec
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

    def run(self):
        """
        :return: 0 in case of failure, 1 in case of success
        """
        print("Torpedos task run!")
        self.setup_target()
        print("Target setup done")
        self.shoot_heart()
        print("Hearth shooted")

        #TODO
        # self.setup_lever()

        self.shoot_ellipse()

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
                self.movement_object.set_lin_velocity(right=min(config["lin_vel_speeds"], coords["x"]*config["speed_multiplier"]))
                requirements["x_centered"] = False
            elif coords["x"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(right=-min(config["lin_vel_speeds"], coords["x"]*config["speed_multiplier"]))
                requirements["x_centered"] = False

            else:
                self.movement_object.set_lin_velocity(right=0)
                requirements["x_centered"] = True

            # Center target in camera center Y
            if coords["y"] > config["center_margin"]:
                self.movement_object.set_lin_velocity(up=-min(config["lin_vel_speeds"], coords["y"]*config["speed_multiplier"]))
                requirements["y_centered"] = False
            elif coords["y"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(up=min(config["lin_vel_speeds"], coords["y"]*config["speed_multiplier"]))
                requirements["y_centered"] = False
            else:
                self.movement_object.set_lin_velocity(up=0)
                requirements["y_centered"] = True

            # Setup distance
            if dist < config["distance"] - config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=-min(config["lin_vel_speeds"], dist/100*config["speed_multiplier"]))
                requirements["distance"] = False
            elif dist > config["distance"] + config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=min(config["lin_vel_speeds"], dist/100*config["speed_multiplier"]))
                requirements["distance"] = False
            else:
                self.movement_object.set_lin_velocity(front=0)
                requirements["distance"] = True

            time.sleep(config["refresh_loops_time"])

    def shoot_heart(self):
        """
        Function setups ROV on heart and shoot.
        """
        global config
        requirements = {"distance": False, "heart_centered_x": False, "heart_centered_y": False}

        while not all(requirements.values()):
            img = self.main_camera.get_image()
            heart_coords = self.locator.get_heart_coordinates(img)
            dist = self.movement_object.get_front_distance()

            # Setup  shooting distance
            if dist < config["shoting_distance"] - config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=-min(config["lin_vel_speeds"], dist/100 *config["speed_multiplier"]))
                requirements["distance"] = False
            elif dist > config["shoting_distance"] + config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=min(config["lin_vel_speeds"], dist/100*config["speed_multiplier"]))
                requirements["distance"] = False
            else:
                self.movement_object.set_lin_velocity(front=0)
                requirements["distance"] = True

            # Center heart to shoot in X
            if heart_coords["x"] - config["x_offset"] > config["center_margin"]:
                self.movement_object.set_lin_velocity(right=min(config["lin_vel_speeds"], heart_coords["x"]*config["speed_multiplier"]))
                requirements["heart_centered_x"] = False
            elif heart_coords["x"] - config["x_offset"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(right=-min(config["lin_vel_speeds"], heart_coords["x"]*config["speed_multiplier"]))
                requirements["heart_centered_x"] = False

            else:
                self.movement_object.set_lin_velocity(right=0)
                requirements["heart_centered_x"] = True

            # Center heart to shoot in Y
            if heart_coords["y"] - config["y_offset"] > config["center_margin"]:
                self.movement_object.set_lin_velocity(up=-min(config["lin_vel_speeds"], heart_coords["y"]*config["speed_multiplier"]))
                requirements["heart_centered_y"] = False
            elif heart_coords["y"] - config["y_offset"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(up=min(config["lin_vel_speeds"], heart_coords["y"]*config["speed_multiplier"]))
                requirements["heart_centered_y"] = False
            else:
                self.movement_object.set_lin_velocity(up=0)
                requirements["heart_centered_y"] = True

            time.sleep(config["refresh_loops_time"])

        # TODO
        # lunch.torpedo()

    def shoot_ellipse(self):
        """
        Function setups ROV on ellpse and shoot.
        """
        global config
        requirements = {"distance": False, "ellipse_centered_x": False, "ellipse_centered_y": False}

        while not all(requirements.values()):
            img = self.main_camera.get_image()
            ellipse_coords = self.locator.get_ellipse_coordinates(img)
            dist = self.movement_object.get_front_distance()

            # Setup  shooting distance
            if dist < config["shoting_distance"] - config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=-min(config["lin_vel_speeds"], dist))
                requirements["distance"] = False
            elif dist > config["shoting_distance"] + config["distance_margin"]:
                self.movement_object.set_lin_velocity(front=min(config["lin_vel_speeds"], dist))
                requirements["distance"] = False
            else:
                self.movement_object.set_lin_velocity(front=0)
                requirements["distance"] = True

            # Center ellipse to shoot in X
            if ellipse_coords["x"] - config["x_offset"] > config["center_margin"]:
                self.movement_object.set_lin_velocity(right=min(config["lin_vel_speeds"], ellipse_coords["x"]*config["speed_multiplier"]))
                requirements["ellipse_centered_x"] = False
            elif ellipse_coords["x"] - config["x_offset"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(right=-min(config["lin_vel_speeds"], ellipse_coords["x"]*config["speed_multiplier"]))
                requirements["ellipse_centered_x"] = False

            else:
                self.movement_object.set_lin_velocity(right=0)
                requirements["ellipse_centered_x"] = True

            # Center ellipse to shoot in Y
            if ellipse_coords["y"] - config["y_offset"] > config["center_margin"]:
                self.movement_object.set_lin_velocity(up=-min(config["lin_vel_speeds"], ellipse_coords["y"]*config["speed_multiplier"]))
                requirements["ellipse_centered_y"] = False
            elif ellipse_coords["y"] - config["y_offset"] < -config["center_margin"]:
                self.movement_object.set_lin_velocity(up=min(config["lin_vel_speeds"], ellipse_coords["y"]*config["speed_multiplier"]))
                requirements["ellipse_centered_y"] = False
            else:
                self.movement_object.set_lin_velocity(up=0)
                requirements["ellipse_centered_y"] = True

            time.sleep(config["refresh_loops_time"])

        # TODO
        # lunch.torpedo()

#TODO
# Dodać "rewolwer" z torpedami jako mniejsza klasę aby zwracała aktualny
#  potrzebny offset jaki należy ustawiać dla torpedy która ma być wystrzelona.

# class TorpedosRevolver():
#     config:{"t_1":[x=-15,y=-14],
#             "t_2":[x=-10,y=-12],
#     }

#     torpedo_to_lunch = 1

#     lunch_torpedo():
#         lunching torpedo, change current torpedo to lunch and offset

#     get_offset():
#         returns offset from camera center to acctually prepared torpedo