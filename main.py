from logpy.LogPy import Logger
import threading

# Cameras
from vision.camera import Camera

# Task running
from utils.python_subtask import PythonSubtask

# Sensors
from communication.communication import Communication

from communication.rpi_broker.ahrs import AHRS
from communication.rpi_broker.depth_sensor import DepthSensor
from communication.rpi_broker.hydrophones import Hydrophones
from communication.rpi_broker.distance import DistanceSensor

# Control
from communication.rpi_broker.movements import Movements
from communication.rpi_broker.torpedoes import Torpedoes
from communication.rpi_broker.manipulator import Manipulator
from communication.rpi_broker.dropper import Dropper

#Task sceduller
from tasks.tasks_scheduler import TaskSchedululer
from tasks.erl_task_scheduler import TaskSchedululer as ErlTaskScheduler

#CHECK MODE
# TODO - replace with checkoing if is conection to simulation or real rpi
from definitions import MAINDEF, CAMERAS

#simulation
if MAINDEF.MODE == "SIMULATION":
    from communication.unity_driver import UnityDriver


class Main():
    '''
    Creates object of all sensor types, packs their references into
    a list. Creates Communication thread.
    '''
    def __init__(self):
        '''
        Creates and stores references of all slave objects.
        '''
        mode = MAINDEF.MODE

        self.logger = Logger(filename='main', title="Main")

        # Simulation initialisation
        self.unity_driver = None
        if mode == "SIMULATION":
            self.unity_driver = UnityDriver()

        # cameras 
#        camera_process = PythonSubtask.run("vision/camera_server.py")
        self.front_cam1 = Camera("front", mode, self.unity_driver)
        self.bottom_camera = Camera("bottom", mode, self.unity_driver)
        self.arm_camera = Camera("arm", mode, self.unity_driver)
        self.bumper_cam_right = Camera("bumper_right", mode, self.unity_driver)
        self.bumper_cam_left = Camera("bumper_left", mode, self.unity_driver)
        self.logger.log("Cameras created")

        self.cameras = {'arm_camera': self.arm_camera,
                        'bottom_camera': self.bottom_camera,
                        'front_cam1': self.front_cam1,
                        'bumper_cam_right': self.bumper_cam_right,
                        'bumper_cam_left': self.bumper_cam_left}

        #communication
        self.communication = Communication()
        self.rpi_reference = self.communication.rpi_reference
        self.logger.log("communication was established")

        # sensors
        self.ahrs = AHRS(self.rpi_reference)
        self.depth_sensor = DepthSensor(self.rpi_reference)
        self.distance_sensor = DistanceSensor(self.rpi_reference)
        self.hydrophones = Hydrophones(self.rpi_reference)
        self.logger.log("sensors created")

        self.sensors = {'ahrs': self.ahrs,
                        'depth': self.depth_sensor,
                        'distance': self.distance_sensor,
                        'hydrophones': self.hydrophones}
        #control
        self.movements = Movements(self.rpi_reference)
        self.torpedoes = Torpedoes(self.rpi_reference)
        self.manipulator = Manipulator(self.rpi_reference)
        self.dropper = Dropper(self.rpi_reference)
        self.logger.log("control objects created")

        self.control = {'movements': self.movements,
                        'torpedoes': self.torpedoes,
                        'manipulator': self.manipulator,
                        'dropper': self.dropper}

        # task sheduler
        if mode == "ROV3":
            self.task_scheduler = ErlTaskScheduler(self.control, self.sensors, self.cameras, self.logger)
            self.logger.log("ERL task scheduler created")
        else:
            self.task_scheduler = TaskSchedululer(self.control, self.sensors, self.cameras, self.logger)
            #self.movements.pid_turn_on()
            #self.movements.set_lin_velocity(up=1)
            self.logger.log("Robosub task scheduler created")

    def run(self):
        self.logger.log("main thread is running")
        self.task_scheduler.run()


if __name__ == "__main__":
    main = Main()
    main.run()
