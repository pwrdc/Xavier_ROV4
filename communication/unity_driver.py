import time
from cv2 import COLOR_RGB2BGR, cvtColor, imshow, imwrite, rectangle, waitKey

from communication.pytransdec.pytransdec.communication import TransdecCommunication
import rpi_com.rov_comm as rov_comm
import rpi_com.ports as ports


class UnityDriver():

    unity_ready = False
    transdec_communication = None
    engine_movement = None
    engine_slave = None
    imu_master = None
    depth_master = None
    vector_observation = None
    is_pad_only = True
    focused_camera = 0 # 0 - front camera
                       # 1 - bottom  camera

    def __init__(self, is_pad_only=False):
        self.engine_slave = rov_comm.Client(ports.ENGINE_MASTER_PORT)
        self.is_pad_only = is_pad_only
        if(not self.is_pad_only):
            self.imu_master = rov_comm.Client(ports.AHRS_DRIVER_PORT)
            self.depth_master = rov_comm.Client(ports.DEPTH_DRIVER_PORT)

        self.transdec_communication = TransdecCommunication()
        self.unity_ready = True
        print("Unity simulation is ready")

    def run(self):
        self.transdec_communication.reset()
        while self.unity_ready:
            try:
                t0 = time.time()
                self.update_engine()
                print("Engine update: {}".format(time.time() - t0))
                t1 = time.time()
                self.transdec_communication.step([self.engine_movement['front'],
                                                self.engine_movement['right'],
                                                self.engine_movement['up'],
                                                self.engine_movement['roll'],
                                                self.focused_camera])
                print("Simulation update: {}".format(time.time() - t1))
                t2 = time.time()
                if(not self.is_pad_only):
                    self.vector_observation = self.transdec_communication.vector
                    self.update_IMU()
                    #print ("imu")
                    # self.update_depth_sensor()
                    #print ("depth")
                    self.update_visual_observation()
                    print("Update obseration: {}".format(time.time() - t2))
                    time.sleep(0.002) # to reduce number of the movements server errors
            except TypeError as e:
                print(type(e).__name__)
                time.sleep(0.005)

            except Exception as e:
                print(type(e).__name__)
                print("Error: {}".format(e))
                time.sleep(2)

    def get_engine_data(self):
        return self.engine_slave.get_data()

    def update_engine(self):
        self.engine_movement = self.get_engine_data()

    def get_IMU_data(self):
        output = {}

        output['lineA_x'] = self.vector_observation['acceleration_x']
        output['lineA_y'] = self.vector_observation['acceleration_y']
        output['lineA_z'] = self.vector_observation['acceleration_z']

        output['yaw'] = self.vector_observation['rotation_x']
        output['pitch'] = self.vector_observation['rotation_y']
        output['roll'] = self.vector_observation['rotation_z']

        output['angularA_x'] = self.vector_observation['angular_acceleration_x']
        output['angularA_y'] = self.vector_observation['angular_acceleration_y']
        output['angularA_z'] = self.vector_observation['angular_acceleration_z']

        return output

    def update_IMU(self):
        dict = self.get_IMU_data()
        self.imu_master.send_data(dict)

    def get_depth_data(self):
        return self.vector_observation['depth']

    def update_depth_sensor(self):
        depth = self.get_depth_data()
        print("depth "+str(depth))
        self.depth_master.send_data(depth)
        print("depth updated")

    def update_visual_observation(self):
        observation = cvtColor(self.transdec_communication.visual[0], COLOR_RGB2BGR)
        #imwrite('img.png', observation)
        #TODO server to send visual observation
        imshow('picture', observation)

    def set_camera_focus(self, camera_to_focus):
        self.focused_camera = camera_to_focus

    def get_image(self):
        return cvtColor(self.transdec_communication.visual[0], COLOR_RGB2BGR)

if __name__ == '__main__':
    unity_driver = UnityDriver(is_pad_only=False)
    print("prepare to run")
    unity_driver.run()
