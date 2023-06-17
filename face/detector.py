import cv2
import os
from face.utils import *

class FaceDetector():
    def __init__(self, method):
        self._detector = cv2.CascadeClassifier(PATHS['cascade_file'])
        self._model_exists = False

        if method in METHODS:
            self._method_data = METHODS[method]
            self._model = self._method_data['function']()
            self._treshold = self._method_data['treshold']
            self._model_file = self._method_data['file']
            path = os.path.join(PATHS['models'], self._model_file)
            if os.path.isfile(path):
                self._model_exists = True
                self._model.read(path)

    def detect(self, image):
        if not self._model_exists:
            return None, image

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_resized = cv2.resize(gray, (gray.shape[1]//RESIZE_FACTOR, gray.shape[0]//RESIZE_FACTOR))     

        faces = self._detector.detectMultiScale(
            gray_resized,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_SIZE
        )

        idx = 0
        user_recognised = False
        for (x, y, w, h) in faces:
            idx = idx + 1
            x = x * RESIZE_FACTOR
            y = y * RESIZE_FACTOR
            w = w * RESIZE_FACTOR
            h = h * RESIZE_FACTOR

            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(gray[y:y+h, x:x+w], FACE_SIZE)
            confidence = self._model.predict(face_resized)

            if confidence[1] < self._treshold:
                user_recognised = True
                cv2.rectangle(image, (x, y), (x+w, y+h), SUCCESS_COLOR, LINE_STROKE)
                cv2.putText(image, 'User - %.0f' % (confidence[1]), (x-10, y-10), FONT_FAMILY, FONT_SIZE, SUCCESS_COLOR, FONT_WEIGHT)
            else:
                cv2.rectangle(image, (x, y), (x+w, y+h), FAILURE_COLOR, LINE_STROKE)
                cv2.putText(image, 'Unknown - %.0f' % (confidence[1]), (x-10, y-10), FONT_FAMILY, FONT_SIZE, FAILURE_COLOR, FONT_WEIGHT)

        return user_recognised, image