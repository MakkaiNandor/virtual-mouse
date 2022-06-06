import cv2
import mediapipe as mp

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
        self.__hands = []

    def find_hands(self, image, draw=True):
        """
        Detect hands on the given image and save their position in pixels.
        Arguments:
            image: The input BGR image
            draw: If True, draw the hand landmarks on the image. Default: True
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.hands.process(image_rgb)
        self.__hands = []
        img_h, img_w, _ = image.shape

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)

                landmarks = {}

                for nr, lm in enumerate(hand_lms.landmark):
                    # convert landmarks to pixels
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    landmarks[nr] = {"x": x, "y": y}

                self.__hands.append(landmarks)

    def get_landmarks(self, hand_index):
        if 0 <= hand_index and hand_index < len(self.__hands):
            return self.__hands[hand_index]
        return {}

if __name__ == "__main__":
    print("This file cannot be used like a standalone Python file.")
    print("If you want to use it, you need to import this file in another Python file.")
