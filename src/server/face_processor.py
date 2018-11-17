import numpy as np
import dlib
import cv2
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
from imutils import face_utils


class FaceProcessor:
    ERROR_BAD_IMAGE = 1
    ERROR_BAD_EYE = 2

    __EYE_AR_THRESH = 0.15
    __EYE_AR_CONSEC_FRAMES = 3

    def __init__(self):
        self.__detector = dlib.get_frontal_face_detector()
        self.__predictor = dlib.shape_predictor("res/face_detector.dat")

        (self.__lEyeStart, self.__lEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.__rEyeStart, self.__rEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def __eye_closed(self, eye_coord):
        a = dist.euclidean(eye_coord[1], eye_coord[5])
        b = dist.euclidean(eye_coord[2], eye_coord[4])
        c = dist.euclidean(eye_coord[0], eye_coord[3])

        ear = (a + b) / (2.0 * c)

        if ear < self.__EYE_AR_THRESH:
            return True

        return False

    def __crop_image_by_mask(self, mask, image):
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

    def get_eye_data(self, face_image_path):
        """
        Args:
        image_path: relative path to the face image (.jpg)

        Returns:
        [left_eye_image_path, right_eye_image_path]

        Images are stored in the same directory named like the original image name with suffixes appended.

        left_eye_image_path: relative path to the left eye image (.jpg)
        right_eye_image_path: relative path to the left eye image (.jpg)
        """

        try:
            image = cv2.imread(face_image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rect = self.__detector(gray, 0)[0]
            shape = self.__predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
        except:
            return self.ERROR_BAD_IMAGE

        left_eye = shape[self.__lEyeStart:self.__lEyeEnd]
        right_eye = shape[self.__rEyeStart:self.__rEyeEnd]

        if self.__eye_closed(left_eye) or self.__eye_closed(right_eye):
            return self.ERROR_BAD_EYE

        left_eye_hull = cv2.convexHull(left_eye)
        right_eye_hull = cv2.convexHull(right_eye)

        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [left_eye_hull], -1, 255, -1)
        left_eye = self.__crop_image_by_mask(mask, image)

        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [right_eye_hull], -1, 255, -1)
        right_eye = self.__crop_image_by_mask(mask, image)

        original_image_name = face_image_path[:face_image_path.find('.')]
        left_eye_image_location = original_image_name + '_left_eye.jpg'
        right_eye_image_location = original_image_name + '_right_eye.jpg'

        cv2.imwrite(left_eye_image_location, left_eye)
        cv2.imwrite(right_eye_image_location, right_eye)

        return [left_eye_image_location, right_eye_image_location]