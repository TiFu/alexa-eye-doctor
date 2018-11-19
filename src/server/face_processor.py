import numpy as np
import pickle
import dlib
import cv2
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
from imutils import face_utils


class FaceProcessor:
    ERROR_BAD_IMAGE = 1
    ERROR_BAD_EYE = 2

    __EYE_AR_THRESH = 0.25
    __EYE_AR_CONSEC_FRAMES = 3

    def __init__(self):
        self.__detector = dlib.get_frontal_face_detector()
        self.__predictor = dlib.shape_predictor("res/face_detector.dat")
        with open('res/eye_color_classifier.pkl', 'rb') as f:
            self.__eye_color_predictor = pickle.load(f)

        (self.__lEyeStart, self.__lEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.__rEyeStart, self.__rEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def __increase_image_brightness(self, image, value):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        cur_brightness = np.mean(v)

        if cur_brightness < value:
            diff = int(value - cur_brightness)
            lim = 255 - diff
            v[v > lim] = 255
            v[v <= lim] += diff

        final_hsv = cv2.merge((h, s, v))
        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return image

    def __eye_closed(self, eye_coord):
        a = dist.euclidean(eye_coord[1], eye_coord[5])
        b = dist.euclidean(eye_coord[2], eye_coord[4])
        c = dist.euclidean(eye_coord[0], eye_coord[3])

        ear = (a + b) / (2.0 * c)

        if ear < self.__EYE_AR_THRESH:
            return True

        return False

    def __crop_eye_by_eye_hull(self, hull, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [hull], -1, 255, -1)

        out = np.zeros_like(image)
        (x, y) = np.where(mask == 255)

        (top_x, top_y) = (np.min(x), np.min(y))
        (bottom_x, bottom_y) = (np.max(x), np.max(y))

        delta_x, delta_y = bottom_x - top_x, bottom_y - top_y
        top_x, bottom_x = top_x - int(0.5 * delta_x), bottom_x + int(0.2 * delta_x) + 1
        top_y, bottom_y = top_y - int(0.2 * delta_y), bottom_y + int(0.2 * delta_y) + 1

        for x in range(top_x, bottom_x):
            for y in range(top_y, bottom_y):
                out[x][y] = image[x][y]

        return out[top_x:bottom_x, top_y:bottom_y]

    def __crop_iris_by_eye_hull(self, hull, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(gray)

        cv2.drawContours(mask, [np.vstack([hull[1], hull[2], hull[4], hull[5]])], -1, 255, -1)

        out = np.zeros_like(image)
        (x, y) = np.where(mask == 255)

        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))

        for x in range(topx, bottomx + 1):
            for y in range(topy, bottomy + 1):
                if mask[x][y] == 255:
                    out[x][y] = image[x][y]

        return out[topx:bottomx + 1, topy:bottomy + 1]

    def __get_iris_color(self, eye):
        Z = eye.reshape((-1, 3))
        Z = np.float32(Z)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 4
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((eye.shape))

        unique, counts = np.unique(label, return_counts=True)
        clusters = sorted(np.asarray((unique, counts)).T.tolist(), key=lambda x: -x[1])
        top_cluster = clusters[1][0] if center[clusters[0][0]].mean() < 10 else clusters[0][0]

        return center[top_cluster][::-1]

    def get_eye_data(self, face_image_path):
        """
        Args:
        image_path: relative path to the face image (.jpg)

        Returns:
        [left_eye_image_path, right_eye_image_path, color_probability]

        Images are stored in the same directory named like the original image name with suffixes appended.

        left_eye_image_path: relative path to the left eye image (.jpg)
        right_eye_image_path: relative path to the left eye image (.jpg)
        color_probability: a dictionary with keys ["blue", "brown", "green"] and a float probability in range [0;1]
        for eye iris being that color
        """

        image = cv2.imread(face_image_path)
        image_brightened = self.__increase_image_brightness(image, 150)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rect = self.__detector(gray, 0)[0]
        shape = self.__predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        left_eye = shape[self.__lEyeStart:self.__lEyeEnd]
        right_eye = shape[self.__rEyeStart:self.__rEyeEnd]

        if self.__eye_closed(left_eye) or self.__eye_closed(right_eye):
            return self.ERROR_BAD_EYE

        left_eye_hull = cv2.convexHull(left_eye)
        right_eye_hull = cv2.convexHull(right_eye)

        left_eye = self.__crop_eye_by_eye_hull(left_eye_hull, image)
        right_eye = self.__crop_eye_by_eye_hull(right_eye_hull, image)

        original_image_name = face_image_path[:face_image_path.find('.')]
        left_eye_image_location = original_image_name + '_left_eye.jpg'
        right_eye_image_location = original_image_name + '_right_eye.jpg'

        cv2.imwrite(left_eye_image_location, left_eye)
        cv2.imwrite(right_eye_image_location, right_eye)

        ### Get eye color
        left_eye = self.__crop_iris_by_eye_hull(left_eye_hull, image_brightened)
        right_eye = self.__crop_iris_by_eye_hull(right_eye_hull, image_brightened)

        left_iris_color = self.__get_iris_color(left_eye)
        right_iris_color = self.__get_iris_color(right_eye)
        iris_color = (left_iris_color.astype(np.int) + right_iris_color.astype(np.int)) / 2

        iris_color_proba = self.__eye_color_predictor.predict_proba([iris_color])
        color_proba = {
            "green": round(iris_color_proba[0][0], 2),
            "blue": round(iris_color_proba[0][1], 2),
            "brown": round(iris_color_proba[0][2], 2)
        }

        return [left_eye_image_location, right_eye_image_location, color_proba]