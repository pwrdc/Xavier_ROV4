import cv2
import numpy as np

THRESH = 180
SHIFT = 10
BLUR_MASK = (3, 3)
CANNY_UP = 200
CANNY_DOWN = 195
CNT_COLOUR = (0, 255, 0)
MIN_AREA = 20000
RATIO = 0.55
RATIO1 = 0.225


class GarlicDetector:

    @staticmethod
    def prepare_img(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        ret, thresh = cv2.threshold(blur, THRESH, 199, 200)
        return thresh

    @staticmethod
    def max_rgb_filter(img):
        (b, g, r) = cv2.split(img)

        m = np.maximum(np.maximum(r + 236, g), b)
        r[r < m] = 0
        g[g < m] = 0
        b[b < m] = 0

        return cv2.merge([b, g, r])

    def canny_detect(self, img):
        img_mrgb = self.max_rgb_filter(img)

        lower_red0 = np.array([0, 70, 50])
        lower_red1 = np.array([170, 70, 50])
        upper_red = np.array([10, 255, 255])

        img = cv2.cvtColor(img_mrgb, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(img, lower_red0, upper_red)
        mask2 = cv2.inRange(img, lower_red1, upper_red)

        mask = mask1 | mask2
        output = cv2.bitwise_and(img, img, mask=mask)
        output = self.prepare_img(output)
        edges = cv2.Canny(output, CANNY_DOWN, CANNY_UP)
        return edges

    @staticmethod
    def lines_average(avg_x, avg_y, num_of_lines):
        middle = (int(avg_x / num_of_lines), int(avg_y / num_of_lines))
        return middle

    def get_values(self, middle, l, r, up, down):
        width = np.sqrt((r[0] - l[0])**2 + (r[1] - l[1])**2)
        height = np.sqrt((down[0]-up[0])**2 + (down[1]-up[1])**2)

        a1 = (r[1]-l[1]) / (r[0]-l[0])
        a2 = (up[1]-down[1]) / (up[0]-down[0])

        sin_theta1, cos_theta1, sin_theta2, cos_theta2 = self.angle_function(a1, a2)

        add_char = [1, 1, 1, 1]

        if l[1] < middle[1]:
            add_char[0] = -1
        x0 = l[0] + width * RATIO1 * cos_theta1
        y0 = l[1] - add_char[0]*width * RATIO1 * sin_theta1

        if r[1] > middle[1]:
            add_char[1] = -1
        x1 = r[0] - width * RATIO1 * cos_theta1
        y1 = r[1] + add_char[1] * width * RATIO1 * sin_theta1

        if up[0] > middle[0]:
            add_char[2] = -1
        x2 = up[0] + add_char[2] * height * RATIO1 * cos_theta2
        y2 = up[1] + height * RATIO1 * sin_theta2

        if down[0] < middle[0]:
            add_char[3] = -1
        x3 = down[0] - add_char[3] * height * RATIO1 * cos_theta2
        y3 = down[1] - height * RATIO1 * sin_theta2

        coords = [[np.array((x0, y0), int), np.array((x1, y1), int)], [np.array((x2, y2), int), np.array((x3, y3), int)]]

        return coords

    @staticmethod
    def angle_function(a1, a2):
        angle1 = abs(np.arctan(a1))
        angle2 = abs(np.arctan(a2))

        sin_theta1 = np.sin(angle1)
        cos_theta1 = np.cos(angle1)

        sin_theta2 = np.sin(angle2)
        cos_theta2 = np.cos(angle2)

        return np.array((sin_theta1, cos_theta1, sin_theta2, cos_theta2))

    @staticmethod
    def calculate_position(distance, points, m, b):
        ya = (distance**2 - points[0] + b/m) / (-1/m - 1)
        xa = (ya - b) / m
        return xa, ya

    @staticmethod
    def calculate_width(p1, p2):
        width = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        return np.round(width, 2)

    def coords_detect(self, img): # ! returns np.array type and float type object !
        img = self.cut_frame(img)
        edges = self.canny_detect(img)
        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=10, lines=np.array([]), minLineLength = 10, maxLineGap=10)
        a, b, c = lines.shape
        l_narrow, r_narrow, up_narrow, down_narrow = ([10e8, 0], [0, 0], [0, 10e8], [0, 0])
        avg_x, avg_y = (0.0, 0.0)
        for i in range(a-1):
            for x1, y1, x2, y2 in lines[i]:
                if x1 == 0 or x2 == 0:
                    continue
                else:
                    if x1 < l_narrow[0]:
                        l_narrow[0] = x1
                        l_narrow[1] = y1
                    if x2 > r_narrow[0]:
                        r_narrow[0] = x2
                        r_narrow[1] = y2
                    if y1 < up_narrow[1]:
                        up_narrow[1] = y1
                        up_narrow[0] = x1
                    if y2 > down_narrow[1]:
                        down_narrow[1] = y2
                        down_narrow[0] = x2
                    avg_x = avg_x + x1
                    avg_y = avg_y + y1

        middle = self.lines_average(avg_x, avg_y, a)
        points_coords = self.get_values(middle, l_narrow, r_narrow, up_narrow, down_narrow)
        width = self.calculate_width(l_narrow, r_narrow)
        self.show_points(points_coords, img)
        self.normalize_coordinates(points_coords, img)
        width = self.normalize_size(width, img)
        return points_coords, width

    @staticmethod
    def show_points(lines, image):
        image_copy = image
        for line in lines:
            for point in line:
                for i in range(-2, 2):
                    for j in range(-2, 2):
                        image_copy[point[1] + i][point[0] + j] = (255, 0, 0)

# parę punktów się nie zgadza, późniejsze obliczenia niedostosowane do tego formatu
    @staticmethod
    def normalize_lines(lines, frame):
        const = frame.shape[1] / 2
        lines = lines.astype(float)
        for i in range(lines.shape[0]):
            lines[i][0] = [(lines[i][0][0] - const) / const,
                           (const - lines[i][0][1]) / const,
                           (lines[i][0][2] - const) / const,
                           (const - lines[i][0][3]) / const]
        return lines

    @staticmethod
    def cut_frame(frame):
        frame_cut = frame[0:frame.shape[0], int((frame.shape[1]/2) - (frame.shape[0]/2)):int((frame.shape[1]/2) + (frame.shape[0]/2))]
        return frame_cut

    @staticmethod
    def normalize_coordinates(lines, frame):
        const = frame.shape[0] / 2
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                lines[i][j] = np.array([(lines[i][j][0] - const) / const,
                                        (const - lines[i][j][1]) / const])

    @staticmethod
    def denormalize_coordinates(lines, frame):
        const = frame.shape[0] / 2
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                lines[i][j] = np.array([int(const * (lines[i][j][0] + 1)),
                                        int(const * (1 - lines[i][j][1]))])

    @staticmethod
    def normalize_size(size, frame):
        size /= frame.shape[0]/2
        return size
