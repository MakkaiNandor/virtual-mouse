import cv2

class WindowManager():
    def __init__(self, window_name, keypress_callback = None):
        self.keypress_callback = keypress_callback
        self._window_name = window_name
        self._window_created = False

    @property
    def isWindowCreated(self):
        return self._window_created
    
    @property
    def isWindowOpened(self):
        return self._window_created and cv2.getWindowProperty(self._window_name, cv2.WND_PROP_VISIBLE) >= 1
    
    def createWindow(self):
        cv2.namedWindow(self._window_name)
        self._window_created = True

    def show(self, frame):
        cv2.imshow(self._window_name, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._window_name)
        self._window_created = False

    def processEvents (self):
        keycode = cv2.waitKey(1)
        if self.keypress_callback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypress_callback(keycode)