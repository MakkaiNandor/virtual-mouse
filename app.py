import cv2
from camera.capture import CameraCapture
from camera.window import WindowManager
from hands.tracker import HandTracker
from hands.utils import *
import time

class App():
    def __init__(self):
        self._window = WindowManager("Virtual Mouse", self.onKeyPress)
        self._capture = CameraCapture(0)
        self._tracker = HandTracker(self.processHandLandmarks)

    def onKeyPress(self, keycode):
        print('onKeyPress', keycode)
        if keycode == 27 or keycode == 113:
            self._window.destroyWindow()

    def processHandLandmarks(self, landmarker_result, mp_image, timestamp_ms):
        print(timestamp_ms)
        frame = drawLandmarksOnImage(mp_image.numpy_view(), landmarker_result)
        self._window.setFrame(frame)

    def run(self):
        """Run the main loop"""
        start_timestamp = time.time()
        prev_timestamp = None
        self._window.createWindow()
        while self._window.isWindowOpened and self._capture.isCaptureOpened:
            # self._capture.enterFrame()
            self._window.showFrame(self._capture.fps)
            # print(self._capture.fps)

            frame_ok = self._capture.readNextFrame()

            if frame_ok is None:
                break
            elif frame_ok == False:
                continue

            frame = self._capture.frame

            timestamp = int(time.time() - start_timestamp)

            if prev_timestamp is not None and  timestamp <= prev_timestamp:
                timestamp = prev_timestamp + 1

            frame = cv2.flip(frame, 1)

            self._tracker.findHands(frame, timestamp * 1000)

            prev_timestamp = timestamp

            self._window.processEvents()

if __name__ == "__main__":
    App().run()