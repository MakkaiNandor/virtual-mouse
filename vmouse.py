import cv2
import time
import numpy as np
from camera.capture import CameraCapture
from camera.window import WindowManager
from hands.tracker import HandTracker
from hands.gesture import HandGestureRecognizer
from face.detector import FaceDetector
from mouse.control import MouseControl
from settings import settings, getMainHand, getReferencePoints
from utils import *

class VirtualMouse():
    def __init__(self):
        self._capture = CameraCapture(int(settings['camera']))
        self._window = WindowManager('Virtual Mouse', self.onKeyPress)
        self._hand_tracker = HandTracker(self.processHandLandmarks, settings['hands'])
        self._gesture_finder = HandGestureRecognizer()
        self._face_detector = FaceDetector(settings['face_method'])
        self._mouse = MouseControl(settings['hands'], settings['navigation'], getMainHand(), getReferencePoints(), settings['mouse_sensitivity'])

    def onKeyPress(self, keycode):
        """Process key press events"""

        print('onKeyPress', keycode)

        # Close the window if ESC or 'q' is pressed
        if keycode == 27 or keycode == ord('q'):
            self._capture.release()
            self._window.destroyWindow()

    def landmarksToPixels(self, landmarker_result):
        hand_landmarks = landmarker_result.hand_landmarks
        for i in range(len(hand_landmarks)):
            hand = hand_landmarks[i]
            for j in range(len(hand)):
                landmark = hand[j]
                landmarker_result.hand_landmarks[i][j].x = int(landmark.x * self._capture.captureSize[0])
                landmarker_result.hand_landmarks[i][j].y = int(landmark.y * self._capture.captureSize[1])
        return landmarker_result

    def processHandLandmarks(self, landmarker_result, mp_image, timestamp_ms):
        """Process the image adter hand detection"""
        frame = self._hand_tracker.drawOnImage(mp_image.numpy_view(), landmarker_result)
        landmarker_result = self.landmarksToPixels(landmarker_result)
        hand_gesture = self._gesture_finder.recognize(landmarker_result)
        print(hand_gesture)
        method = self._mouse.execute(landmarker_result, hand_gesture)
        self._window.setFrame(frame)

    def run(self):
        """Run the main loop"""
        prev_timestamp = None
        self._capture.start()
        self._window.createWindow()
        while self._window.isWindowOpened and self._capture.isCaptureOpened:
            self._window.showFrame(self._capture.fps)

            # Read the next frame and process it if exists
            if self._capture.readNextFrame():
                frame = self._capture.frame
                timestamp = self._capture.timestampMs

                # Make sure the timestamp is monotonically increasing
                if prev_timestamp is not None and  timestamp <= prev_timestamp:
                    timestamp = prev_timestamp + 1

                # Mirror the captured image
                frame = cv2.flip(frame, 1)

                # Recognise face if enabled
                skip_hand_tracking = False
                if settings['face']:
                    recognised, frame = self._face_detector.detect(frame)
                    skip_hand_tracking = recognised == False

                # Detect hands on the image
                if not skip_hand_tracking:
                    self._hand_tracker.findHands(frame, timestamp)
                else:
                    self._window.setFrame(frame)

                prev_timestamp = timestamp

                # Process user inputs
                self._window.processEvents()

        self._capture.release()
        self._window.destroyWindow()

if __name__ == '__main__':
    VirtualMouse().run()