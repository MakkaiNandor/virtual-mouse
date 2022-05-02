import cv2
import mediapipe as mp

class HandTracker():
    def __init__(self, static_mode=False, max_hands=2, detection_con=0.5, tracking_con=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=tracking_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, image, draw=True):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
                    tmp.append([nr, x, y])

                self.position.append(tmp)

        return image

    def convert_to_pixels(self, landmark):
        pass