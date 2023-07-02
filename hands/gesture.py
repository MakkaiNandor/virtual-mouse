import math
from hands.utils import *

class HandGestureRecognizer():
    def recognize(self, hand_detection_result):
        hand_landmarks_list = hand_detection_result.hand_landmarks
        handedness_list = hand_detection_result.handedness
        gesture_result = {}

        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            hand_gesture = ['0', '0', '0', '0', '0']

            # thumb is a special case
            finger = FINGERS[0]
            # get index fniger furthest point from the base
            index_p_idx = self.getFurthestPoint(hand_landmarks, hand_landmarks[0], FINGERS[1])
            # get pinky finger furthest point from the base
            pinky_p_idx = self.getFurthestPoint(hand_landmarks, hand_landmarks[0], FINGERS[-1])
            # get the triangle of the three points
            triangle = Triangle(hand_landmarks[0], hand_landmarks[index_p_idx], hand_landmarks[pinky_p_idx])
            # calculate distances
            base = hand_landmarks[FINGERS[1][0]]
            p1 = hand_landmarks[finger[2]]
            d1 = self.squareDistance(p1, base)
            p2 = hand_landmarks[finger[3]]
            d2 = self.squareDistance(p2, base)
            if d2 > d1 and not triangle.contains(p1) and not triangle.contains(p2):
                hand_gesture[0] = '1'

            # test other fingers
            for p in range(1, 5):
                finger = FINGERS[p]
                base = hand_landmarks[0]
                d1 = self.squareDistance(hand_landmarks[finger[0]], base)
                d2 = self.squareDistance(hand_landmarks[finger[2]], base)
                d3 = self.squareDistance(hand_landmarks[finger[3]], base)
                if d3 > d1 and d3 > d2:
                    hand_gesture[p] = '1'

            hand_gesture = ''.join(hand_gesture)
            gesture_result[handedness[0].category_name] = hand_gesture

        return gesture_result

    def getFurthestPoint(self, landmarks, base, finger):
        furthest_idx = -1
        furthest_value = 0

        for idx in finger:
            d = self.squareDistance(landmarks[idx], base)
            if d > furthest_value:
                furthest_idx = idx
                furthest_value = d

        return furthest_idx

    def squareDistance(self, p1, p2):
        return pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2)

    def distance(self, p1, p2):
        return math.sqrt(self.square_distance(p1, p2))