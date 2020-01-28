from tasks.task_executor_itf import ITaskExecutor, Cameras
from communication.rpi_broker.movements import Movements
from tasks.navigation.locator.ml_solution.yolo_soln import YoloGateLocator
from utils.stopwatch import Stopwatch
from structures.bounding_box import BoundingBox
from utils.signal_processing import mvg_avg
from configs.config import get_config
from time import sleep
import cv2
import math as m
import numpy as np

class GateTaskExecutor(ITaskExecutor):

    ###Initialization###
    def __init__(self, contorl_dict: Movements, sensors_dict, cameras_dict: Cameras, main_logger):
        self._control = contorl_dict
        self._front_camera = cameras_dict['front_cam1']
        self._bounding_box = BoundingBox(0, 0, 0, 0)
        self._logger = main_logger
        self.config = get_config("tasks")['gate_task']
        self.img_server = PythonRESTSubtask("utils/img_server.py", 6669)
        self.img_server.start()
        # For which path we are taking angle. For each path, rotation
        # angle might be set differently in config.json
        self.number = 0
        self.path = []


    ###Start the gate algorithm###
    def run(self):
        MAX_TIME_SEC = self.config['max_time_sec'] #w configu trzeba zmienic bo na razie jest do samego gate
        self._logger.log("Gate task executor started")
        self._control.pid_turn_on()

        stopwatch = Stopwatch()
        stopwatch.start()

        if stopwatch >= MAX_TIME_SEC:
            self._logger.log("TIME EXPIRED GATE NOT FOUND")
            self._control.set_ang_velocity(0, 0, 0)

        if not self.dive():
            self._logger.log("GateTE: diving in progress")

        if not self.find_gate():
            self._logger.log("GateTE: finding the gate in progress")

        if not self.go_trough_gate():
            self._logger.log("GateTE: going through the gate")

#Przycina obraz, zostaje sam bbox
    def post_image(self, img, bounding_box = None):
        if bounding_box is not None:
            self.img_server.post("set_img", img, unpickle_result=False)
            bb = bounding_box.denormalize(img.shape[1], img.shape[0])
            p1 = (int(bb.x1), int(bb.y1))
            p2 = (int(bb.x2), int(bb.y2))
            img = cv2.rectangle(img, p1, p2, (255,0,255))
        self._logger.log("img posted")
        self.img_server.post("set_img", img, unpickle_result=False)

    ###Find gate###
    def find_gate(self):
        self._logger.log("finding the gate")
        config = self.config['search']
        MAX_ANG_SPEED = config['max_ang_speed']
        MOVING_AVERAGE_DISCOUNT = config['moving_avg_discount']
        CONFIDENCE_THRESHOLD = config['confidence_threshold']


        self._control.set_ang_velocity(0, 0, MAX_ANG_SPEED)

        stopwatch = Stopwatch()
        stopwatch.start()
        self._logger.log("started find gate loop")

        while True:
            img = self._front_camera.get_image()

            if self.is_this_gate(img):
                # TODO: zlokalizuj bramkę
                # gate = {"x", "y", "angle"}
                # TODO: zlokalizuj przeszkodę
                # obstacle = "{"x", "y"}
                # more info in create_path comment
                self.create_path(gate, obstacle)    #W trajektorii musi byc uwzgledniona przeszkoda funkcja wyszukujaca przeszkode is_this_obstacle(bounding_box, img):
                return True



    ###Dive###
    def dive (self):
        #self._logger.log("Dive: setting depth")
        #self._control.pid_set_depth(depth)
        #Czy trzeba najpierw ustawic glebokosc, czy mozna od razu w hold depth to robic?
        DEPTH = get_config('max_depth')
        self._logger.log("Dive: holding depth")
        self._control.pid_hold_depth(DEPTH)

    def is_this_gate(self, bounding_box, img):

        confidence = 0
        MOVING_AVERAGE_DISCOUNT = get_config('moving_avg_discount')
        CONFIDENCE_THRESHOLD = get_config('confidence_threshold')

        bounding_box = YoloGateLocator().get_gate_bounding_box(img)
        self.post_image(img, bounding_box)

        if bounding_box is not None:
            confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT) #co robi funkcja mvg_avg
            self._bounding_box.mvg_avg(bounding_box, 0.5, True)
            self._logger.log("is_this_gate: somoething detected")
        else:
            confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)

        # Stop and report sucess if we are sure we found a path!
        if confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this_gate: gate found")
            self._control.set_ang_velocity(0, 0, 0)
            return True

    def is_this_obstacle(self, bounding_box, img):

        confidence = 0
        MOVING_AVERAGE_DISCOUNT = get_config('moving_avg_discount')
        CONFIDENCE_THRESHOLD = get_config('confidence_threshold')

        bounding_box = YoloGateLocator().get_obstacle_bounding_box(img)  # Funkcja rozpoznawania przeszkody do dodania
        self.post_image(img, bounding_box)

        if bounding_box is not None:
            confidence = mvg_avg(1, confidence, MOVING_AVERAGE_DISCOUNT)
            self._bounding_box.mvg_avg(bounding_box, 0.5, True)
            self._logger.log("is_this-obstacle: somoething detected")
        else:
            confidence = mvg_avg(0, confidence, MOVING_AVERAGE_DISCOUNT)

        # Stop and report sucess if we are sure we found a path!
        if confidence > CONFIDENCE_THRESHOLD:
            self._logger.log("is_this-obstacle: obstacle found")
            self._control.set_ang_velocity(0, 0, 0)
            return True

    '''
    returns path  angles to rotate in radians [rad] and forward distances to travel in meters [m]
    first rotate, then move forward!
    input:  gate = {"x", "y", "angle"},where "x" and "y" are coords of gate middle in meters [m],
            "angle" is an angle between normal to gate and AUV's forward X axis in radians [rad]
            obstacle = {"x", "y"}, where "x" and "y" are coords of obstacle middle in meters [m]
    return [{"angle": angle, "distance": distance}]
    '''
    def create_path(self, gate, obstacle):
        # distance at which to stop in front of the gate if necessary [m]
        GATE_DISTANCE_FRONT = 1
        # distance at which to stop after passing the gate [m]
        GATE_DISTANCE_BACK = 1
        # maximal allowed angle between path and normal to gate [rad]
        MAX_ORIENTATION_ERROR = m.radians(10)
        # minimal distance to keep from an obstacle [m]
        MIN_DISTANCE_FROM_OBSTACLE = 1

        def correct_gate_approach():
            alpha = m.atan2(path[-1][1] - path[-2][1], path[-1][0] - path[-2][0])
            if abs(alpha - gate["alpha"]) > MAX_ORIENTATION_ERROR:
                path.pop()
                # point in front of the gate on the line perpendicular to the gate
                p_gf = np.array([gate["x"] - GATE_DISTANCE_FRONT * m.cos(gate["alpha"]),
                                 gate["y"] - GATE_DISTANCE_FRONT * m.sin(gate["alpha"])])
                path.append(p_gf)

                p_gb[0] = gate["x"] + GATE_DISTANCE_BACK * m.cos(gate["alpha"])
                p_gb[1] = gate["y"] + GATE_DISTANCE_BACK * m.sin(gate["alpha"])

                path.append(p_gb)

        def correct_obstacle_passing():
            if obstacle:
                path_line = points_to_line(path[0], path[1])
                # if obstacle is on the path, correct path
                if get_point_from_line_distance(np.array([obstacle["x"], obstacle["y"]]),
                                                path_line) < MIN_DISTANCE_FROM_OBSTACLE:
                    tangents_from_vehicle = get_tangents(path[0], np.array([obstacle["x"], obstacle["y"]]),
                                                         MIN_DISTANCE_FROM_OBSTACLE)
                    # from p_gf if exists, else from p_gb
                    tangents_from_gate = get_tangents(path[1], np.array([obstacle["x"], obstacle["y"]]),
                                                      MIN_DISTANCE_FROM_OBSTACLE)
                    p_cross_1 = get_crossing(tangents_from_vehicle[0], tangents_from_gate[1])
                    p_cross_2 = get_crossing(tangents_from_vehicle[1], tangents_from_gate[0])

                    # choose point closer to original path
                    if get_point_from_line_distance(p_cross_1, path_line) \
                            < get_point_from_line_distance(p_cross_2, path_line):
                        path.insert(1, p_cross_1)
                    else:
                        path.insert(1, p_cross_2)

                    # changing path might have changed gate approach angle - correct it if necessary
                    # (to be precise, path point close to the obstacle should be then changed too,
                    # but change would be minimal so it can be ignored)
                    correct_gate_approach()

        # returns path transformed to angle to rotate and forward distance to travel
        # first rotate, then move forward!
        # return path_transformed = [{"angle": angle, "distance": distance}]
        def get_transformed_path():
            path_transformed = []
            angle_sum = 0
            for i in range(1, len(path)):
                displacement = np.array([path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]])
                distance = m.sqrt(displacement[0] ** 2 + displacement[1] ** 2)
                # angle between subsequent path fragments
                angle = (m.degrees(m.atan2(displacement[1], displacement[0])) - angle_sum) % 360
                if abs(angle) > 180:
                    angle -= 360 * np.sign(angle)
                angle_sum += angle
                path_transformed.append({"angle": angle, "distance": distance})
            return path_transformed

        # returns distance from point p=np.array([x, y]) to line l=[a, b]), where y = ax + b
        def get_point_from_line_distance(p, l):
            return abs(l[0] * p[0] - p[1] + l[1]) / m.sqrt(l[0] ** 2 + 1)

        # returns function of the line between points p0 and p1=np.array([x, y]) l=[a, b], where y = ax + b
        def points_to_line(p0, p1):
            a = (p1[1] - p0[1]) / (p1[0] - p0[0])
            b = p0[1] - a * p0[0]
            return [a, b]

        # returns 2 tangents to circle with middle in p_o and radius d, through p
        # p, p_o = np.array([x, y])
        # return [[a1, b1], [a2, b2]], where line function is y = ax + b
        def get_tangents(p, p_o, d):
            # ancillary variables, for safety and not to count this monstrosity twice
            numerator1 = -m.sqrt(
                -d ** 4 + d ** 2 * p_o[0] ** 2 - 2 * d ** 2 * p_o[0] * p[0] + d ** 2 * p[0] ** 2 + d ** 2 * p_o[
                    1] ** 2 - 2 * d ** 2 * p_o[1] * p[1] + d ** 2 * p[1] ** 2)
            numerator2 = - p_o[0] * p_o[1] + p_o[0] * p[1] + p[0] * p_o[1] - p[0] * p[1]
            denominator = (d ** 2 - p_o[0] ** 2 + 2 * p_o[0] * p[0] - p[0] ** 2)
            # divide by zero protection
            if denominator == 0:
                denominator += 0.0001

            a1 = (-numerator1 + numerator2) / denominator
            b1 = p[1] - a1 * p[0]

            a2 = (numerator1 + numerator2) / denominator
            b2 = p[1] - a2 * p[0]

            return [[a1, b1], [a2, b2]]

        # returns crossing point of 2 lines
        def get_crossing(l1, l2):
            x = (l2[1] - l1[1]) / (l1[0] - l2[0])
            y = l1[0] * x + l1[1]
            return np.array([x, y])

        # list of points (numpy arrays) to subsequently reach (first to do is first on the list)
        # in relation to current AUV coordinate system
        path = []
        # path starting point
        path.append(np.array([0, 0]))
        # point behind the gate on the line connecting AUV and gate middle, where AUV ends task
        alpha = m.atan2(gate["y"], gate["x"])
        p_gb = np.array([gate["x"] + GATE_DISTANCE_BACK * m.cos(alpha),
                         gate["y"] + GATE_DISTANCE_BACK * m.sin(alpha)])
        path.append(p_gb)

        # if angle between path and gate is greater than limit, correct path
        correct_gate_approach()

        # if obstacle is found
        correct_obstacle_passing()

        self.path = get_transformed_path()

    ###Swim through the gate###
    def go_trough_gate(self):
        self._logger.log("go thtough the gate")
        config = self.config['go']
        #MAX_ENGINE_POWER = config['max_engine_power']
        #GO_TIME = config['go_time_seconds']
        for segment in self.path:
            self._control.rotate_angle(yaw=segment["angle"])
            self._control.move_distance(front=segment["distance"])
        self._logger.log("passed through the gate")
        return True
