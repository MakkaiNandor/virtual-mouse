import cv2
import os
import shutil
import numpy as np
from camera.capture import CameraCapture
from camera.window import WindowManager
from settings import settings
from face.utils import *

class FaceDetectorTrainer():
    def __init__(self):
        self._window = WindowManager('Train Face Detector', self.onKeyPressed)
        self._detector = cv2.CascadeClassifier(PATHS['cascade_file'])

        createDirIfNotExists(PATHS['images'])
        createDirIfNotExists(PATHS['models'])

        if settings['face_method'] in METHODS:
            self._method_data = METHODS[settings['face_method']]
            self._model = self._method_data['function']()
            self._model_file = self._method_data['file']
        else:
            self._method_data = None
            self._model = None
            self._model_file = None

    def onKeyPressed(self, keycode):
        if keycode == 27 or keycode == ord('q'):
            self._window.destroyWindow()
        
    def captureImages(self):
        self._capture = CameraCapture(settings['camera'])
        self._window.createWindow()
        self._images_count = 0
        self._frame_count = 0

        while self._window.isWindowOpened and self._capture.isCaptureOpened:
            self._frame_count += 1
            # Read the next frame and process it if exists
            if self._capture.readNextFrame():
                frame = self._capture.frame

                # Mirror the captured image
                frame = cv2.flip(frame, 1)

                # Process image
                if self._images_count < TRAIN_NR_FACES:
                    frame = self.processImage(frame)
                else:
                    break

                # Process image
                self._window.show(frame)

                # Process user inputs
                self._window.processEvents()

        self._window.destroyWindow()

    def processImage(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        gray_resized = cv2.resize(gray, (gray.shape[1]//RESIZE_FACTOR, gray.shape[0]//RESIZE_FACTOR)) 

        faces = self._detector.detectMultiScale(
            gray_resized,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_SIZE
        )

        if len(faces) > 0:
            # Search the biggest face
            biggest_face_idx = np.argmax(np.array([w * h for (x, y, w, h) in faces]))
            (x, y, w, h) = faces[biggest_face_idx]
        
            x = x * RESIZE_FACTOR
            y = y * RESIZE_FACTOR
            w = w * RESIZE_FACTOR
            h = h * RESIZE_FACTOR

            if self._frame_count % TRAIN_IMG_FREQ == 0:
                # Save the face as image
                self._images_count += 1
                face_resized = cv2.resize(gray[y:y+h, x:x+w], FACE_SIZE)
                cv2.imwrite('%s/%s.png' % (PATHS['images'], self._images_count), face_resized)
                print('Captured image: ', self._images_count)

            cv2.rectangle(image, (x, y), (x+w, y+h), DEFAULT_COLOR, LINE_STROKE)

        return image        

    def train(self):
        imgs = []
        tags = []

        if self._model is None:
            return False

        for fn in os.listdir(PATHS['images']):
            path = os.path.join(PATHS['images'], fn)
            imgs.append(cv2.imread(path, 0))
            tags.append(0)

        if len(imgs) == 0:
            return False

        (imgs, tags) = [np.array(item) for item in [imgs, tags]]

        self._model.train(imgs, tags)
        self._model.save(os.path.join(PATHS['models'], self._model_file))

        return True