import cv2
import time

class CameraCapture():
    def __init__(self, video_source):
        self._capture = cv2.VideoCapture(video_source)
        self._frame = None
        
        self._frames_elapsed = 0
        self._timestamp_ms = 0

        self._capture_size = (self._capture.get(cv2.CAP_PROP_FRAME_WIDTH), self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self._prev_frame_time = None
        self._frame_time = None

    def readNextFrame(self):
        if not self.isCaptureOpened:
            return None

        self._prev_frame_time = self._frame_time
        self._frame_time = time.time()

        ok, self._frame = self._capture.read()

        return ok

    @property
    def frame(self):
        if not self.isCaptureOpened:
            return None

        return self._frame
        
    @property
    def fps(self):
        if self._prev_frame_time is not None and self._frame_time is not None:
            return str(int(1 / (self._frame_time - self._prev_frame_time)))
        return None
    
    @property
    def isCaptureOpened(self):
        return self._capture.isOpened()

    @property
    def captureSize(self):
        return self._capture_size