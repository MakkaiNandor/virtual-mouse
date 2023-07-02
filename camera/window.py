import cv2
from utils import *

class WindowManager():
    """
    Basic window manager class that creates a named window and shows images within that. It can handle key press events and optionally can show the FPS.

    Usage:
        def callback(key):
            if key == 27:
                win.destroyWindow()

        def asyncProcess():
            image = ...
            win.setFrame(image)

        win = WindowManager('Main Window', callback)
        win.createWindow()
        while win.isWindowOpened:
            # 1. Synchronous way
            image = ...
            fps = ...
            win.show(image, fps)

            # 2. Asynchronous way
            asyncProcess()
            fps = ...
            win.showFrame(fps)

            win.processEvents()
        win.destroyWindow()
    """

    def __init__(self, window_name, keypress_callback = None):
        """Constructor
        
        Parameters:
        -----------
        window_name
            the name of the window
        keypress_callback (default: None)
            the callback that handles the keypress event
        """
        self.keypress_callback = keypress_callback
        self._window_name = window_name
        self._window_created = False
        self._frame_to_show = None

    @property
    def isWindowCreated(self):
        """Check if the window is created"""
        return self._window_created
    
    @property
    def isWindowOpened(self):
        """Check if the window is opened"""
        if not self._window_created:
            return False

        try:
            cv2.getWindowProperty(self._window_name, cv2.WND_PROP_VISIBLE)
            opened = True
        except:
            opened = False

        return opened
    
    def createWindow(self):
        """Create the window"""
        if not self.isWindowCreated:
            cv2.namedWindow(self._window_name)
            self._window_created = True

    def destroyWindow(self):
        """Destroy the window"""
        if self.isWindowCreated:
            cv2.destroyWindow(self._window_name)
            self._window_created = False

    def setFrame(self, frame):
        """Set the frame which should be shown next in the window
        
        Parameters:
        -----------
        frame
            the image to set
        """
        self._frame_to_show = frame

    def showFrame(self, fps=None):
        """Show the frame
        
        Parameters:
        -----------
        fps (default: None)
            number of FPS to show
        """
        if self._frame_to_show is not None:
            self.show(self._frame_to_show, fps)
            self._frame_to_show = None

    def show(self, frame, fps=None):
        """Show an image in the window

        Parameters:
        -----------
        frame
            the image to show
        fps (default: None)
            number of FPS to show
        """
        if fps is not None:
            putTextOnImage(frame, fps, (10, 30), COLOR_BLUE)
        cv2.imshow(self._window_name, frame)

    def processEvents(self):
        """Call the keypress_callback to handle events"""
        keycode = cv2.waitKey(1)
        if self.keypress_callback is not None and keycode != -1:
            self.keypress_callback(keycode & 0xFF)