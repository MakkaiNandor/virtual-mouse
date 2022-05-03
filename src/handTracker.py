import cv2
import mediapipe as mp

FINGERS = [
    [1, 2, 3, 4],       # thumb
    [5, 6, 7, 8],       # index
    [9, 10, 11, 12],    # middle
    [13, 14, 15, 16],   # ring
    [17, 18, 19, 20]    # pinky
]

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

    def detect_fingers(self, hand):
        status = [0, 0, 0, 0, 0]

        if len(hand) > 0:
            base = hand[0]
            idx = 0
            for finger in FINGERS:
                tip = finger[-1]
                ip = finger[-2]
                d_tip = pow(hand[tip][1] - base[1], 2) + pow(hand[tip][2] - base[2], 2)
                d_ip = pow(hand[ip][1] - base[1], 2) + pow(hand[ip][2] - base[2], 2)
                if d_tip > d_ip:
                    status[idx] = 1
                idx = idx + 1

        return status

if __name__ == "__main__":
    print("This file cannot be used like a standalone Python file.")
    print("If you want to use it, you need to import this file in another Python file.")