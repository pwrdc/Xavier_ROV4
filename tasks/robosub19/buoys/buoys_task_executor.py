import time
import cv2

from tasks.task_executor_itf import ITaskExecutor
from structures.bounding_box import BoundingBox
from utils.stopwatch import Stopwatch
from vision.camera_server import get_image
from neural_networks.utils import extract_prediction
from tasks.gate.locator.ml_solution.yolo_soln import YoloGateLocator
from configs.config import get_config
from utils.signal_processing import mvg_avg
from neural_networks.nn_manager import NNManager
from definitions import ANGLE_BUOYS, MAX_TIME_BUOYS_FORWARD, TIME_BUOYS_RETURN

default_depth = 2.4
time_surface = 4
first_rot = 220
second_rot = 180

TIME_TO_REACH_BUOY = MAX_TIME_BUOYS_FORWARD # 50
TIME_OF_RETURN = TIME_BUOYS_RETURN #10

TIMEOUT_1ST_BUYOY = 40
TIMEOUT_2ST_BUYOY = 40 

ANGLE_1ST_BUYOY = 180
ANGLE_2ST_BUYOY = 176
NEUTRAL_ROTATION = ANGLE_BUOYS #180 + 720 #30#180

MAX_FRONT_VELOCITY = 25
HITTING_SPEED = 20
RETURN_SPEED = 20

HIT_DISTANCE = 70

GO_AROUND_RIGHT = 5
GO_AROUND_FRONT = 0.1

GO_AROUND_DEPTH = 0.8

class BuoysTaskExecutor(ITaskExecutor):
    def __init__(self, control_dict, sensors_dict, cameras_dict, main_logger):
        """
        @param: movement_object is object of Movements Class
            (repository RPi_ROV4: RPi_ROV4/blob/master/control/movements/movements_itf.py)
        @param: camras_dict is dictionary of references to camera objects
            keywords: arm_camera; bottom_camera; front_cam1;
            for cameras objects look at /vision/front_cam_1.py
        """
        self.control_dict = control_dict
        self._sensors = sensors_dict
        self.cameras_dict = cameras_dict
        self._logger = main_logger
        self.movements = control_dict['movements']
        self.ahrs = sensors_dict['ahrs']

        self.distance = sensors_dict['distance'].get_front_distance

        self.front_hit_time = 0.0

        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self.config = get_config("robosub19_tasks")['gate_task']

    def run(self):
        self._logger.log("run buoy")
        

        self.movements.pid_turn_on()
        self.movements.pid_set_depth(default_depth)
        self.movements.pid_yaw_turn_on()
        time.sleep(2)
        self._logger.log("buoy: set depth to default")

        #self._logger.log("buoy: move fornt - first")
        #self.movements.set_lin_velocity(front=25)
        #time.sleep(TIME_TO_REACH_BUOY)
        #self.movements.set_lin_velocity()

        self.find_buyoy_front()

        if self.find_buyoy("buoy1"):
            self._logger.log("buoy: hit first buyoy")
            time_of_hit = self.hit_buyoy(TIMEOUT_1ST_BUYOY, ANGLE_1ST_BUYOY, "buoy1")
            self.return_from_hit_buyoy(TIME_OF_RETURN)

        if self.find_buyoy("buoy2"): # TODO: 2
            self._logger.log("buoy2: hit second buyoy")
            time_of_hit = self.hit_buyoy(TIMEOUT_2ST_BUYOY, ANGLE_2ST_BUYOY, "buoy2") 
            self.return_from_hit_buyoy(TIME_OF_RETURN)
        
        self.go_around()

    def find_buyoy_front(self):
        self._logger.log("Checking if buoys are nearby ")
        self.movements.set_lin_velocity(front=25)
        MOVING_AVERAGE_DISCOUNT = 0.9
        CONFIDENCE_THRESHOLD = 0.9
        MAX_TIME_SEC = TIME_TO_REACH_BUOY

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("searted find buoy loop")

        confidence = 0
        while(True):
            img = get_image("front") # self._front_camera.get_image()
            img = cv2.resize(img, (416, 416))
            bounding_box = extract_prediction(NNManager.get_yolo_model("buoy").predict(img), "buoy1")

            if bounding_box is not None:
                confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT)
                self._bounding_box = bounding_box # mvg avg?
                self._logger.log(f"buoy: somoething detected. Confidence: {confidence}")
            else:
                confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)
                self._logger.log(f"buoy: Nothing detected. Confidence: {confidence}")

            # Abort if we are running far away...
            if stopwatch.time() > MAX_TIME_SEC:
                self._logger.log("buoy not found in front. Stopping!")
                self.movements.set_ang_velocity(0,0,0)
                return False


            # Stop and report sucess if we are sure we found a path!
            if confidence > CONFIDENCE_THRESHOLD:
                self._logger.log("buoy found. Stopping!")
                self.movements.set_ang_velocity(0,0,0)
                return True 

    def find_buyoy(self, buoy_name):
        self._logger.log("finding the buoy - "+buoy_name)
        MOVING_AVERAGE_DISCOUNT = 0.7
        CONFIDENCE_THRESHOLD = 0.9
        MAX_TIME_SEC = 99
        ANGLE_DELTA = 2
        BUOY1_MIN_TRESHOLD = 0.3

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("searted find buoy loop")

        confidence = 0
        while(True):
            img = get_image("front") # self._front_camera.get_image()
            img = cv2.resize(img, (416, 416))
            bounding_box = extract_prediction(NNManager.get_yolo_model("buoy").predict(img), buoy_name)

            if bounding_box is not None:
                confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT)
                self._bounding_box = bounding_box # mvg avg?
                self._logger.log(f"buoy: somoething detected. Confidence: {confidence}")
            else:
                confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)
                self._logger.log(f"buoy: Nothing detected. Confidence: {confidence}")
                self.movements.rotate_angle(0,0,ANGLE_DELTA)


            # Abort if we are running far away...
            if stopwatch.time() > MAX_TIME_SEC:
                self._logger.log("buoy not found - aboart")
                self.movements.set_ang_velocity(0,0,0)
                return False


            # Stop and report sucess if we are sure we found a path!
            if confidence > CONFIDENCE_THRESHOLD:
                if buoy_name == "bouy1" and bounding_box.p < BUOY1_MIN_TRESHOLD:
                    continue

                self._logger.log("buoy found")
                self.movements.set_ang_velocity(0,0,0)
                return True 


    def hit_buyoy(self, timeout_to_hit, buyoy_angle, buoy_name):
        '''
        :return: time of manuver 
        '''
        self._logger.log("starting to hit "+buoy_name)
        start_time = time.time()

        #self.movements.pid_set_yaw(buyoy_angle)
        #self.movements.set_lin_velocity(front=MAX_FRONT_VELOCITY)

        hit_time = time.time() + timeout_to_hit
        while True:
            self.center_on_buoy(buoy_name, HITTING_SPEED)
            #self.movements.set_lin_velocity(front=MAX_FRONT_VELOCITY)
            self._logger.log("after centred")
            #print(self.distance())
            if self.distance() < HIT_DISTANCE:
                time.sleep(0.5)
                self._logger.log("buoy: was hit")
                self.movements.set_lin_velocity()
                break
            
            if time.time() > hit_time:
                self._logger.log("buoy: didn't hit buyoy - aboart")
                self.movements.set_lin_velocity()
                break

            time.sleep(0.1)

        return time.time() - start_time

    def return_from_hit_buyoy(self, time_of_return):
        #self.movements.pid_set_yaw(time_of_return)
        self.movements.set_lin_velocity(front=-RETURN_SPEED)
        time.sleep(time_of_return)
        self.movements.set_lin_velocity()

    def go_around(self):
        #self._logger.log("buoy: go around - right")
        #self.movements.move_distance(right=GO_AROUND_RIGHT)
        #self._logger.log("buoy: go around - frint")
        #self.movements.move_distance(front=GO_AROUND_FRONT)
        #self._logger.log("buoy: go around - left")
        #self.movements.move_distance(right=-GO_AROUND_RIGHT)
        self._logger.log("buyoy: rotate to ")
        self.movements.pid_set_yaw(NEUTRAL_ROTATION)
        time.sleep(4)
        self._logger.log("buoy: go up")
        self.movements.pid_set_depth(GO_AROUND_DEPTH)
        time.sleep(2)
        self._logger.log("buoy: go around - front")
        self.movements.move_distance(front=GO_AROUND_FRONT)

    def center_on_buoy(self, buoy_name, fron_val=0):
        self._logger.log("starting centering")

        ENGINE_POWER = 40
        MOVING_AVERAGE_DISCOUNT = 0.5
        MAXIMAL_DISTANCE_CENTER = 0.1
        MAX_TIME_SEC = 10

        hit_time = time.time() +5        
        stopwatch = Stopwatch()
        stopwatch.start() 

        while(True):
            try:
                img = get_image("front") # self._front_camera.get_image()
                img = cv2.resize(img, (416, 416))
                bounding_box = extract_prediction(NNManager.get_yolo_model("buoy").predict(img), buoy_name)

                if stopwatch.time() > MAX_TIME_SEC:
                    self.movements.set_lin_velocity(0,0,0)
                    return False

                # Try again if yolo did not return a box
                # TODO: Maybe go back?
                if bounding_box is None:
                    continue

                self._bounding_box = bounding_box # .mvg_avg(bounding_box, MOVING_AVERAGE_DISCOUNT, True)
            
                xc = (self._bounding_box.x1 + self._bounding_box.x2) / 2 - 0.5
                yc = (self._bounding_box.y1 + self._bounding_box.y2) / 2 - 0.5

                self._logger.log(f"Current detection x: {xc}")
                self._logger.log(f"Current detection y: {yc}")

                # Stop if centered...
                # TODO: Because of moving avg probably we are too far. Might be problem
                if abs(xc) < MAXIMAL_DISTANCE_CENTER:
                    self.movements.set_lin_velocity(fron_val,0,0)
                    self._logger.log("buoy: Centered!")
                    return True

                # Stop if centering too long...
                

                # New speed is based on path distance from center
                right_speed = ENGINE_POWER * xc

                self.movements.set_lin_velocity(fron_val, right_speed, 0)
            except Exception as e:
                self._logger.log(f"Problem with centering {e}")
