import cv2
import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from hands.utils import *

class HandTracker:
    def __init__(self, callback=None, num_hands=1):
        base_options = python.BaseOptions(model_asset_path=PATHS['model_file'])
        options = vision.HandLandmarkerOptions(base_options=base_options, running_mode=vision.RunningMode.LIVE_STREAM, result_callback=callback, num_hands=num_hands)
        self._detector = vision.HandLandmarker.create_from_options(options)

    def findHands(self, image, timestamp_ms):
        """
        Detect hands on the given image.
        Arguments:
            image: The input BGR image
            timestamp_ms: Timestamp in miliseconds
        """
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        self._detector.detect_async(mp_image, timestamp_ms)

    def drawOnImage(self, rgb_image, hands_result):
        hand_landmarks_list = hands_result.hand_landmarks
        handedness_list = hands_result.handedness
        annotated_image = np.copy(rgb_image)

        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            # Draw the hand landmarks.
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style()
            )

            # Get the top left corner of the detected hand's bounding box.
            height, width, _ = annotated_image.shape
            x_coordinates = [landmark.x for landmark in hand_landmarks]
            y_coordinates = [landmark.y for landmark in hand_landmarks]
            text_x = int(min(x_coordinates) * width)
            text_y = int(min(y_coordinates) * height) - MARGIN

            # Draw handedness (left or right hand) on the image.
            putTextOnImage(annotated_image, f'{handedness[0].category_name}', (text_x, text_y), COLOR_ORANGE)

        return annotated_image