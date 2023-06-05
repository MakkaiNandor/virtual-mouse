import cv2
import time

class CameraCapture():
    def __init__(self, capture, window_manager = None, mirror = False):
        self.window_manager = window_manager
        self.mirror = mirror

        self._capture = capture
        self._entered_frame = False
        self._frame = None
        
        self._start_time = None
        self._frames_elapsed = 0
        self._fps_estimate = None
        self._timestamp_ms = 0

        self._capture_size = (capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def frame(self):
        if not self.isCaptureOpened:
            return None
        
        if self._frames_elapsed == 0:
            self._start_time = time.time()
            
        if self._entered_frame and self._frame is None:
            _, self._frame = self._capture.read()

        return self._frame
        
    @property
    def fps(self):
        return self._fps_estimate
    
    @property
    def isCaptureOpened(self):
        return self._capture.isOpened()
    
    @property
    def timestampMs(self):
        return self._timestamp_ms
    
    @property
    def captureSize(self):
        return self._capture_size

    def enterFrame(self):
        """Capture the next frame, if any."""
        # But first, check that any previous frame was exited.
        assert not self._entered_frame, 'previous enterFrame() had no matching exitFrame()'
        if self.isCaptureOpened:
            self._entered_frame = self._capture.grab()

    def exitFrame(self):
        """Draw to the window. Release the frame."""

        # Check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame.
        if self.frame is None:
            self._entered_frame = False
            return
        
        time_elapsed = time.time() - self._start_time
        if time_elapsed > 0:
            self._timestamp_ms = self._timestamp_ms + round(time_elapsed * 1000)
            self._fps_estimate = self._frames_elapsed / time_elapsed

        self._frames_elapsed += 1

        # Draw to the window, if any.
        if self.window_manager is not None:
            if self.mirror:
                mirrored_frame = cv2.flip(self._frame, 1)
                self.window_manager.show(mirrored_frame)
            else:
                self.window_manager.show(self._frame)

        # Release the frame.
        self._frame = None
        self._entered_frame = False