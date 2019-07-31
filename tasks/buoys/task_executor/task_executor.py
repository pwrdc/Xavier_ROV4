"""
File contains interface for buoys task solver
"""
from tasks.task_executor_itf import ITaskExecutor
from tasks.buoys.locator.locator import Locator
import time

config = {"end_yaw":100, # yaw to set after task
          "end_depth":1.02, # depth to set after task
          "distance": 50,  # distance from ROV to target
          "distance_margin": 2,  # m argin for distance +- val
          "center_margin": 0.05,  # margin for overall object location in camera center 1=100%
          "lin_vel_speeds": 0.3,  # max linear speeds for ROV
          "speed_multiplier": 1,  # value times distance element to center
          "refresh_loops_time": 1,  # while loops delay in sec
          "exit_time": 3 # time to move forward after last task
          }
MAX_FRONT_VELOCITY = 0.25

TIMEOUT_1ST_buoy = 40
TIMEOUT_2ST_buoy = 40


class TaskExecutor(ITaskExecutor):
    """
    TaskExecutor inherit from this interface
    Every sub-algorithm also implement his interface
    """

    def __init__(self, movement_object, sensors_dict,cameras_dict):
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
        self.sensors = sensors_dict

    def run(self):
        """
        :return: 0 in case of failure, 1 in case of success
        """
        global config

        #TODO get actual yaw
        config["end_yaw"]=self.sensors.get("yaw")
        config["end_depth"]=self.sensors.get("depth")

        print("Buoys task run!")
        self.hit_jiangshi()
        print("jiangshi hitted")
        self.hit_triangle()
        print("triangle hitted")
        self.exit_tasks()
        print("task ended")

    def hit_jiangshi(self):
        global config
        requirements = {"distance": False, "x_centered": False, "y_centered": False}

        while not all(requirements.values()):
            img = self.main_camera.get_image()
            coords = self.locator.get_jiangshi_coordinates(img)
            dist = self.sensors.get("distance")

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
        

        time_of_hit = self.hit_buoy(TIMEOUT_1ST_buoy)
        self.return_from_hit_buoy(time_of_hit)
        return 

    def hit_triangle(self):
        global config
        requirements = {"distance": False, "x_centered": False, "y_centered": False}

        while not all(requirements.values()):
            img = self.main_camera.get_image()
            coords = self.locator.get_rectangle_coordinates(img)
            dist = self.sensors.get("distance")

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
        
        time_of_hit = self.hit_buoy(TIMEOUT_2ST_buoy)
        self.return_from_hit_buoy(time_of_hit)
        return 

    def exit_tasks(self):
        global config

        self.movement_object.pid_set_yaw(config["end_yaw"])
        self.movement_object.pid_set_depth(config["end_depth"])

        time.sleep(3) # time to setup pids


        self.movement_object.set_lin_velocity(front = config["lin_vel_speeds"])
        time.sleep(config["exit_time"])
        self.movement_object.set_lin_velocity(front = 0)

        return


    def hit_buoy(self, timeout_to_hit):
        '''
        :return: time of manuver 
        '''
        TIMEOUT_FOR_HIT = 40 

        HIT_DISTANCE = 10

        start_time = time.time()

        self.movement_object.pid_set_yaw(self.sensors.get("yaw"))
        self.movement_object.set_lin_velocity(front=MAX_FRONT_VELOCITY)

        hit = False
        hit_time = time.time() + TIMEOUT_FOR_HIT
        while not hit:
            if self.sensors.get("distance") < HIT_DISTANCE:
                time.sleep(2)
                break
            
            if time.time() > hit_time:
                break

            time.sleep(0.1)

        self.movement_object.set_lin_velocity()
        return time.time() - start_time

    def return_from_hit_buoy(self, time_of_return):
        self.movement_object.pid_set_yaw(time_of_return)
        self.movement_object.set_lin_velocity(front=-MAX_FRONT_VELOCITY)
    
        time.sleep(time_of_return)
        self.movement_object.set_lin_velocity()