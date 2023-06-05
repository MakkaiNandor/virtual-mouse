import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, callback):
        base_options = python.BaseOptions(model_asset_path="hands/hand_landmarker.task")
        options = vision.HandLandmarkerOptions(base_options=base_options, running_mode=vision.RunningMode.LIVE_STREAM, result_callback=callback)
        self._detector = vision.HandLandmarker.create_from_options(options)

    def findHands(self, image, timestamp_ms):
        """
        Detect hands on the given image and save their position in pixels.
        Arguments:
            image: The input BGR image
        """
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        self._detector.detect_async(mp_image, timestamp_ms)