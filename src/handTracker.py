import cv2
import mediapipe as mp
import math

FINGER_THUMB = [1, 2, 3, 4]
FINGER_INDEX = [5, 6, 7, 8]
FINGER_MIDDLE = [9, 10, 11, 12]
FINGER_RING = [13, 14, 15, 16]
FINGER_PINKY = [17, 18, 19, 20]

FINGERS = [
    FINGER_THUMB,
    FINGER_INDEX,
    FINGER_MIDDLE,
    FINGER_RING,
    FINGER_PINKY
]

class HandTracker:
    def __init__(self, static_mode=False, max_hands=2, detection_con=0.5, tracking_con=0.5):
        """
        Constructor of HandTracker class.
        Arguments:
            static_mode: If False, treats the input images as a video stream, when hands are detected it simply track them. If True, hand detection runs on every input image. Default: False
            max_hands: Maximum number of hands to detect. Default: 2
            detection_con: Minimum confidence value ([0.0, 1.0]) for hand detection. Default: 0.5
            tracking_con: Minimum confidence value ([0.0, 1.0]) for hand tracking. Default: 0.5
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=tracking_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, image, draw=True):
        """
        Detect hands on the given image and save their position in pixels.
        Arguments:
            image: The input BGR image
            draw: If True, draw the hand landmarks on the image. Default: True
        Returns:
            The image.
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.hands.process(image_rgb)
        self.position = []
        img_h, img_w, _ = image.shape

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)

                tmp = []

                for nr, lm in enumerate(hand_lms.landmark):
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    tmp.append({"id": nr, "x": x, "y": y})

                self.position.append(tmp)

        return image

    def detect_fingers(self, hand):
        """
        Detect which fingers are up.
        Arguments:
            hand: Position of a single hand.
        Returns:
            An array of finger's status. (0 - down, 1 - up)
        """
        status = [0, 0, 0, 0, 0]

        if len(hand) > 0:
            for idx in range(5):
                finger = FINGERS[idx]
                if idx == 0:
                    base = hand[5]
                    continue
                else:
                    base = hand[0]
                d1 = self.square_distance(hand[finger[0]], base)
                d2 = self.square_distance(hand[finger[2]], base)
                d3 = self.square_distance(hand[finger[3]], base)
                if d3 > d1 and d3 > d2:
                    status[idx] = 1

        return status

    def square_distance(self, p1, p2):
        """
        Calculate the square distance between two points.
        Arguments:
            p1: The first point
            p2: The second point
        Returns:
            The square distance between points.
        """
        return pow(p1['x'] - p2['x'], 2) + pow(p1['y'] - p2['y'], 2)

    def distance(self, p1, p2):
        """
        Calculate the distance between two points.
        Arguments:
            p1: The first point
            p2: The second point
        Returns:
            The distance between points.
        """
        return math.sqrt(self.square_distance(p1, p2))

if __name__ == "__main__":
    print("This file cannot be used like a standalone Python file.")
    print("If you want to use it, you need to import this file in another Python file.")