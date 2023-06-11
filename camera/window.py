import cv2

class WindowManager():
    def __init__(self, window_name, keypress_callback = None, show_fps=None):
        self.keypress_callback = keypress_callback
        self._window_name = window_name
        self._window_created = False
        self._frame_to_show = None

    @property
    def isWindowCreated(self):
        return self._window_created
    
    @property
    def isWindowOpened(self):
        return self._window_created and cv2.getWindowProperty(self._window_name, cv2.WND_PROP_VISIBLE) >= 1
    
    def createWindow(self):
        cv2.namedWindow(self._window_name)
        self._window_created = True

    def setFrame(self, frame):
        self._frame_to_show = frame

    def showFrame(self, fps=None):
        if self._frame_to_show is not None:
            if fps is not None:
                cv2.putText(self._frame_to_show, fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow(self._window_name, self._frame_to_show)
            self._frame_to_show = None

    def show(self, frame):
        cv2.imshow(self._window_name, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._window_name)
        self._window_created = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypress_callback is not None and keycode != -1:
            self.keypress_callback(keycode & 0xFF)