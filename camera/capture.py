import cv2
import time

class CameraCapture():
    """
    Video capture class that reads the frames from the video source (file or camera) and retrieve them for further processing.

    Usage:
        cap = CameraCapture(0)
        cap.start()
        width, height = cap.captureSize
        while cap.isCaptureOpened:
            fps = cap.fps
            timestamp = cap.timestampMs

            if not cap.readNextFrame():
                break
            
            frame = cap.frame
            # further image processing
        cap.release()
    """

    def __init__(self, video_source):
        """Constructor
        
        Parameters:
        -----------
        video_source
            video file path or camera id
        """
        self._source = video_source
        self._capture = cv2.VideoCapture()
        self._frame = None
        
        self._start_time = None
        self._prev_frame_time = None
        self._frame_time = None

    def start(self):
        """Start the VideoCapture object"""
        if not self.isCaptureOpened:
            self._capture.open(self._source)

    def release(self):
        """Release the VideoCapture object"""
        if self.isCaptureOpened:
            self._capture.release()

    def readNextFrame(self):
        """Read the next frame"""
        if not self.isCaptureOpened:
            return False

        if self._start_time is None:
            self._start_time = time.time()

        self._prev_frame_time = self._frame_time
        self._frame_time = time.time()

        ok, self._frame = self._capture.read()

        return ok

    @property
    def frame(self):
        """Retrieve the previously read frame"""
        if not self.isCaptureOpened:
            return None

        return self._frame
        
    @property
    def fps(self):
        """Retrieve the calculated FPS"""
        if self._prev_frame_time is not None and self._frame_time is not None:
            return str(int(1 / (self._frame_time - self._prev_frame_time)))
        return None
    
    @property
    def isCaptureOpened(self):
        """Check if the VideoCapture object is opened"""
        return self._capture.isOpened()

    @property
    def captureSize(self):
        """Retrieve the video source dimensions (width and height)"""
        return (self._capture.get(cv2.CAP_PROP_FRAME_WIDTH), self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def timestampMs(self):
        """Retrieve the absolute timestamp in milliseconds"""
        return int((time.time() - self._start_time) * 1000)