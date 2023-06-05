import cv2
from camera.capture import CameraCapture
from camera.window import WindowManager

CAMERA_SOURCE = 1

class App():
    def __init__(self):
        self._window = WindowManager("Virtual Mouse", self.onKeyPress)
        self._capture = CameraCapture(cv2.VideoCapture(CAMERA_SOURCE), self._window, True)

    def onKeyPress(self, keycode):
        print('onKeyPress', keycode)
        if keycode == 27 or keycode == 113:
            self._window.destroyWindow()

    def run(self):
        """Run the main loop"""
        self._window.createWindow()
        while self._window.isWindowOpened and self._capture.isCaptureOpened:
            self._capture.enterFrame()
            frame = self._capture.frame

            # TODO: Filter the frame

            print("FPS:", self._capture.fps)
            self._capture.exitFrame()
            self._window.processEvents()

if __name__ == "__main__":
    App().run()