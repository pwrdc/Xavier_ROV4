from .. import task_executor_itf
import numpy as np
import time


class TaskExecutor(task_executor_itf.ITaskExecutor):

    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


class BaseTask:
    """
    szablon klasy dla kontrolera zadania
    """

    def __init__(self, movements, task_name, task_id, interval, image_size, debug):
        self.movements = movements
        self.task_name = task_name
        self.task_id = task_id
        self.interval = interval
        self.image_size = image_size
        self.debug = debug
        if self.debug:
            print("Start zadania: {name}-{id}".format(name=self.task_name, id=self.task_id))

    def run(self):
        """
        wykonywanie zadania
        :return: czy zadanie zostalo wykonane poprawnie
        """
        return False

    def send_task_info(self):
        """
        wysyla dane o zadaniu do Jetsona
        """
        print('task_name: ' + self.task_name + ' task_id: ' + self.task_id)

    def update_data(self):
        pass

    
class BoundingBox:
    '''
    Trzeba uzupełnić implementację

    '''
    def _init_(self):
        pass

    def get_vision(self):
        gate_detected = False
        gate_y = int()
        gate_z = int()
        crossbar_slope = float()
        height_correct = False
        return_dict = {'gate_detected': gate_detected, 'gate_y': gate_y, 'gate_z': gate_z,
                       'crossbar_slope': crossbar_slope, 'height_correct': height_correct}
        return return_dict

    def get_sensors(self):
        depth = float()
        imuYaw = float()
        return_dict = {'depth': depth, 'imuYaw': imuYaw}
        return return_dict


class GateFinder(BaseTask):
    """
    klasa zadania znalezienia bramki na obrazie
    """

    def __init__(self, movements, bounding_box, v_z=80, v_r=15, rotate_left=False, depth_thresh=2, n_trials=5,
                 interval=0.1, image_size=(1280, 720), debug=False):
        super().__init__(movements=movements, task_name='gate', task_id=1,
                         interval=interval, image_size=image_size, debug=debug)
        self.rotate_left = rotate_left
        self.v_z = -v_z
        self.v_r = (self.rotate_left * 2 - 1) * v_r
        self.depth_threshold = depth_thresh
        self.trials = 0
        self.trial_threshold = n_trials
        self.current_depth = 0  # pobierz dane z interfejsu
        self.last_depth = 0
        self.gate_detected = False
        self.current_orientation = 0
        self.start_orientation = 0
        self.height_correct = False
        self.bounding_box = bounding_box

    def run(self):
        """
        wykonywanie zadania
        :return: czy wykryto bramke
        """
        # wyslij informacje o zadaniu do Jetsona
        self.send_task_info()
        # pobierz aktualne dane
        self.update_data()
        self.start_orientation = self.current_orientation
        self.last_depth = self.current_depth
        detected = False
        # obracaj sie dopoki nie 360 stopni lub nie wykryto bramki
        while not detected:
            if self.search():
                while not self.height_correct:
                    if self.debug:
                        print('Podplywam')
                    self.update_data()
                    self.movements.set_lin_velocity(front=self.v_z, right=0, up=0)
                    if not self.gate_detected:
                        break
                self.movements.set_lin_velocity(front=0, right=0, up=0)
                if self.gate_detected:
                    return True
            else:
                self.trials += 1
                # jezeli przekroczy prog liczb prob zwroc falsz
                if self.trials > self.trial_threshold:
                    return False
                # jesli nie wykryto opusc lodz
                self.drop()

    def search(self):
        """
        obrot i wykrywanie bramki
        :return: True/False w zaleznosci od tego czy wykryto bramke
        """
        if self.debug:
            print("{name}-{id}: szukam bramki".format(name=self.task_name, id=self.task_id))
        half_rotated = False
        while True:
            self.movements.set_ang_velocity(yaw=self.v_r, roll=0, pitch=0)
            time.sleep(self.interval)
            self.update_data()
            if self.gate_detected:
                self.movements.set_ang_velocity(yaw=0, roll=0, pitch=0)
                return True
            else:
                if 170 < self.current_orientation < 190:
                    half_rotated = True
                if half_rotated and (self.current_orientation > 350 or self.current_orientation < 10):
                    self.movements.set_ang_velocity(yaw=0, roll=0, pitch=0)
                    return False

    def drop(self):
        """
        opuszczenie lodzi gdy nie wykryto
        """
        if self.debug:
            print("{name}-{id}: zanurzam".format(name=self.task_name, id=self.task_id))
        start_time = time.time()
        while time.time() - start_time < self.depth_threshold:
            self.movements.set_lin_velocity(front=0, up=self.v_z, right=0)
            time.sleep(self.interval)
            self.update_data()
            self.movements.set_lin_velocity(front=0, up=0, right=0)
        self.last_depth = self.current_depth

    def update_data(self):
        correct = False
        while not correct:
            try:
                sensor_dict = self.bounding_box.get_sensors()
                self.current_depth = sensor_dict['depth']
                # okresl bezwzgledna wartosc orientacji
                cur_orientation = sensor_dict['imuYaw']
                self.current_orientation = (cur_orientation - self.start_orientation) % 360
                vision_dict = self.bounding_box.get_vision()
                self.gate_detected = vision_dict['gate_detected']
                self.height_correct = vision_dict['height_correct']
                correct = True
            except (TypeError, KeyError):
                print('     Odebrano bledne dane')
                time.sleep(1)
                pass


class GateAligner(BaseTask):
    """
    klasa ustawienia łodzi na wprost bramki
    """

    def __init__(self, movements, bounding_box, v=50, y_target=640, z_target=200, y_margin=20, z_margin=20,
                 slope_margin=0.1, fix_thresh=1., recovery_thresh=5., interval=0.1, image_size=(1280, 720),
                 debug=False):
        super().__init__(movements=movements, task_name='gate', task_id=2,
                         interval=interval, image_size=image_size, debug=debug)
        self.v_def = v
        self.y_target = y_target
        self.z_target = z_target
        self.y_margin = y_margin
        self.z_margin = z_margin
        self.slope_margin = slope_margin
        self.fix_thresh = fix_thresh
        self.recovery_thresh = recovery_thresh
        # dane z czujnikow
        self.gate_detected = False
        self.gate_y = 0
        self.gate_z = 0
        self.crossbar_slope = 0.
        self.time_not_detected = 0.
        self.bounding_box = bounding_box

    def run(self):
        """
        wykonywanie zadania
        :return: czy ustawiono się na wprost do bramki
        """
        # wyslij informacje o zadaniu do Jetsona
        self.send_task_info()
        # pobierz aktualne dane
        self.update_data()
        # dopasuj kat
        while True:
            if self.align_angle():
                break
            # jezeli bramka zniknie popraw
            if not self.fix():
                # jezeli nie uda sie poprawic - porazka
                if self.debug:
                    print('Powrot do GateFinder')
                return [GateFinder(bounding_box=self.bounding_box, movements=self.movements, debug=self.debug)]
        # dopasuj pozycje
        if self.align_position:
            # jezeli uda się - sukces
            return True
        else:
            # jezeli sie nie uda - porazka
            if self.debug:
                print('Powrot do GateFinder')
            return [GateFinder(bounding_box=self.bounding_box, movements=self.movements, debug=self.debug)]

    def align_angle(self):
        """
        dopasowywanie kata ulozenia lodzi
        :return: True/False w zaleznosci od tego, czy udalo sie ustawic lodz
        """
        if self.debug:
            print("{name}-{id}: dopasowuje kat".format(name=self.task_name, id=self.task_id))
        self.update_data()
        # dopoki nachylenie poprzeczki nie jest wewnatrz przedzialu
        while not -self.slope_margin < self.crossbar_slope < self.slope_margin:
            # obracaj lodz w odpowiednim kierunku
            self.movements.set_ang_velocity(yaw=int(np.sign(self.crossbar_slope) * 15), roll=0, pitch=0)
            # czekaj
            time.sleep(self.interval)
            # aktualizuj dane
            self.update_data()
            # dopoki nie wykryto bramki
            if not self.gate_detected:
                # zapisz czas bez wykrycia
                self.time_not_detected += self.interval
                # prog
                if self.time_not_detected > self.fix_thresh:
                    self.movements.set_ang_velocity(yaw=0, roll=0, pitch=0)
                    return False
            elif self.time_not_detected > 0:
                self.time_not_detected = 0.
        # zakoncz obrot
        self.movements.set_ang_velocity(yaw=0, roll=0, pitch=0)
        return True

    def fix(self):
        """
        poprawka gdyby bramka uciekla z pola widzenia
        :return: True/False w zaleznosci od tego czy udalo sie wrocic
        """
        if self.debug:
            print("{name}-{id}: poprawka".format(name=self.task_name, id=self.task_id))
        recovered = False
        self.update_data()
        self.time_not_detected = 0.
        while not self.gate_detected and not recovered:
            # okresl z ktorej strony ostatnio zauwazono bramke
            side_y = -np.sign(self.image_size[0] // 2 - self.gate_y)
            side_z = np.sign(self.image_size[1] // 2 - self.gate_z)
            # sprawdz czy bramka znajduje sie na srodku
            correct_y = self.image_size[0] // 6 < self.gate_y < 5 * self.image_size[0] // 6
            correct_z = self.image_size[1] // 6 < self.gate_z < 5 * self.image_size[1] // 6
            recovered = correct_y and correct_z
            # wyslij polecenie ruchu do lodzi
            if correct_y:
                self.movements.set_lin_velocity(right=0)
            else:
                self.movements.set_lin_velocity(right=int(side_y * self.v_def))
            if correct_z:
                self.movements.set_lin_velocity(up=0)
            else:
                self.movements.set_lin_velocity(up=int(side_z * self.v_def))
            # czekaj
            time.sleep(self.interval)
            # aktualizuj dane
            self.update_data()
            # prog przy wykrywaniu bramki
            if not self.gate_detected:
                self.time_not_detected += self.interval
                if self.time_not_detected > self.recovery_thresh:
                    self.movements.set_lin_velocity(right=0, up=0)
                    return False
            elif self.time_not_detected > 0:
                self.time_not_detected = 0.
        # zatrzymaj lodz
        self.movements.set_lin_velocity(right=0, up=0)
        return True

    @property
    def align_position(self):
        """
        dopasowanie polozenia lodzi
        :return: True/False w zaleznosci od tego czy udalo sie ustawic lodz
        """
        if self.debug:
            print("{name}-{id}: dopasowuje pozycje.".format(name=self.task_name, id=self.task_id))
        aligned = False
        self.update_data()
        while not aligned:
            if self.debug:
                print('Y: {min} < {center} < {max}'.format(min=self.y_target - self.y_margin,
                                                           center=self.gate_y,
                                                           max=self.y_target + self.y_margin))
                print('Z: {min} < {center} < {max}'.format(min=self.z_target - self.z_margin,
                                                           center=self.gate_z,
                                                           max=self.z_target + self.z_margin))
            # okresl z ktorej strony ostatnio zauwazono bramke
            side_y = -np.sign(self.image_size[0] // 2 - self.gate_y)
            side_z = np.sign(self.image_size[1] // 2 - self.gate_z)
            # sprawdz czy bramka znajduje sie na srodku
            aligned_y = self.y_target - self.y_margin < self.gate_y < self.y_target + self.y_margin
            aligned_z = self.z_target - self.z_margin < self.gate_z < self.z_target + self.z_margin
            aligned = aligned_y and aligned_z
            # wyslij polecenie ruchu do lodzi
            if aligned_y:
                self.movements.set_lin_velocity(right=0)
            else:
                self.movements.set_lin_velocity(right=int(side_y * self.v_def))
            if aligned_z:
                self.movements.set_lin_velocity(up=0)
            else:
                self.movements.set_lin_velocity(up=int(side_z * self.v_def))
            # czekaj
            time.sleep(self.interval)
            # aktualizuj dane
            self.update_data()
            if not self.gate_detected:
                self.time_not_detected += self.interval
                if self.time_not_detected > self.fix_thresh:
                    self.movements.set_lin_velocity(right=0, up=0)
                    return False
            elif self.time_not_detected > 0:
                self.time_not_detected = 0.
        # zatrzymaj lodz
        self.movements.set_lin_velocity(right=0, up=0)
        # jezeli bardzo odchyli sie od docelowej pozycji
        if abs(self.crossbar_slope) > 1.5 * self.slope_margin:
            if self.align_angle():
                return True
            else:
                # ponowne dopasowanie pozycji
                return self.align_position
        return True

    def update_data(self):
        correct = False
        while not correct:
            try:
                vision_dict = self.bounding_box.get_vision()
                self.gate_detected = vision_dict['gate_detected']
                if self.gate_detected:
                    self.gate_y = vision_dict['gate_y']
                    self.gate_z = vision_dict['gate_z']
                    self.crossbar_slope = vision_dict['crossbar_slope']
                correct = True
            except (TypeError, KeyError):
                print('     Odebrano bledne dane')
                time.sleep(1)
                pass


class GateDriver(BaseTask):
    def __init__(self, bounding_box, movements, v_x=80, y_margin=20, z_margin=20, slope_margin=0.3,
                 disappear_thresh=0.5, wait_time=5., err_thresh=1., interval=0.1, image_size=(1280, 720), debug=False):
        super().__init__(movements=movements, task_name='gate', task_id=2,
                         interval=interval, image_size=image_size, debug=debug)

        self.v_x = v_x
        self.y_margin = y_margin
        self.z_margin = z_margin
        self.slope_margin = slope_margin
        self.disappear_thresh = disappear_thresh
        self.wait_time = wait_time
        self.err_thresh = err_thresh
        # dane z czujnikow
        self.gate_detected = False
        self.gate_y = 0
        self.gate_z = 0
        self.crossbar_slope = 0
        self.err_time = 0.
        self.time_not_detected = 0.
        self.bounding_box = bounding_box

    def run(self):
        # wyslij informacje o zadaniu do Jetsona
        self.send_task_info()
        # pobierz aktualne dane
        self.update_data()
        if self.debug:
            print("{name}-{id}: plyne przez bramke".format(name=self.task_name, id=self.task_id))
        while True:
            # plyn do przodu
            self.movements.set_lin_velocity(front=self.v_x, right=0, up=0)
            # czekaj
            time.sleep(self.interval)
            # aktualizuj dane
            self.update_data()
            # jesli przekroczy prog nachylenia poprzeczki
            if abs(self.crossbar_slope) > 0.3:
                self.err_time += self.interval
                if self.err_time > self.err_thresh:
                    if self.debug:
                        print('Powrot do GateAligner')
                    return [GateAligner(movements=self.movements, bounding_box=self.bounding_box, debug=self.debug)]
            elif self.err_time > 0:
                self.err_time = 0.
            # zgubiono bramke
            if not self.gate_detected:
                self.time_not_detected += self.interval
                if self.time_not_detected > self.disappear_thresh:
                    # plyn dalej przez bramke
                    time.sleep(self.wait_time)
                    self.movements.set_lin_velocity(front=0, right=0, up=0)
                    return True
            elif self.time_not_detected > 0:
                self.time_not_detected = 0.

    def update_data(self):
        correct = False
        while not correct:
            try:
                vision_dict = self.bounding_box.get_vision()
                self.gate_detected = vision_dict['gate_detected']
                if self.gate_detected:
                    self.gate_y = vision_dict['gate_y']
                    self.gate_z = vision_dict['gate_z']
                    self.crossbar_slope = vision_dict['crossbar_slope']
                correct = True
            except (TypeError, KeyError):
                print('     Odebrano bledne dane')
                time.sleep(1)
                pass
