import cv2
import time
from camera.capture import CameraCapture
from camera.window import WindowManager
from hands.tracker import HandTracker
from hands.utils import *
from settings import settings

class App():
    def __init__(self):
        self._window = WindowManager("Virtual Mouse", self.onKeyPress)
        self._capture = CameraCapture(settings["camera"])
        self._tracker = HandTracker(self.processHandLandmarks, settings["hands"])

    def onKeyPress(self, keycode):
        """Process key press events"""

        print('onKeyPress', keycode)

        # Close the window if ESC or 'q' is pressed
        if keycode == 27 or keycode == ord('q'):
            self._window.destroyWindow()

    def processHandLandmarks(self, landmarker_result, mp_image, timestamp_ms):
        """Process the image adter hand detection"""
        frame = drawLandmarksOnImage(mp_image.numpy_view(), landmarker_result)
        self._window.setFrame(frame)

    def run(self):
        """Run the main loop"""
        prev_timestamp = None
        self._window.createWindow()
        while self._window.isWindowOpened and self._capture.isCaptureOpened:
            self._window.showFrame(self._capture.fps)

            # Read the next frame and process it if exists
            if self._capture.readNextFrame():
                frame = self._capture.frame
                timestamp = self._capture.timestamp_ms

                # Make sure the timestamp is monotonically increasing
                if prev_timestamp is not None and  timestamp <= prev_timestamp:
                    timestamp = prev_timestamp + 1

                # Mirror the captured image
                frame = cv2.flip(frame, 1)

                # Detect hands on the image
                self._tracker.findHands(frame, timestamp)

                prev_timestamp = timestamp

                # Process user inputs
                self._window.processEvents()

if __name__ == "__main__":
    App().run()