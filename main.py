from logpy.LogPy import Logger
import threading

#Cameras
from communication.unity_driver import UnityDriver
from vision.front_cam_1 import FrontCamera1
from vision.bottom_camera import BottomCamera
from vision.arm_camera import ArmCamera
from vision.bumper_cam_right import BumperCamRight
from vision.bumper_cam_left import BumperCamLeft

#Sensors and control
from communication.communication import Communication

from communication.rpi_broker.ahrs import AHRS
from communication.rpi_broker.depth_sensor import DepthSensor
from communication.rpi_broker.hydrophones import Hydrophones
from communication.rpi_broker.distance import DistanceSensor

from communication.rpi_broker.movements import Movements

#Task sceduller
from tasks.tasks_scheduler import TaskSchedululer

#CHECK MODE
# TODO - replace with checkoing if is conection to simulation or real rpi
from definitions import MAINDEF

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

        # cameras creation
        self.front_cam1 = FrontCamera1(mode, self.unity_driver)
        self.bottom_camera = BottomCamera(mode, self.unity_driver)
        self.arm_camera = ArmCamera(mode, self.unity_driver)
        self.bumper_cam_right = BumperCamRight(mode, self.unity_driver)
        self.bumper_cam_left = BumperCamLeft(mode, self.unity_driver)
        self.logger.log("cameras created")

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
        self.logger.log("control objects created")

        self.control = {'movements': self.movements}

        # task sheduler
        self.task_scheduler = TaskSchedululer(self.control, self.sensors, self.cameras, self.logger)
        self.logger.log("task scheduler created")

    def run(self):
        self.logger.log("main thread is running")
        self.task_scheduler.run()


if __name__== "__main__":
    main = Main()
    main.run()
