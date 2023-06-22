import math
from hands.utils import *

FINGERS = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20]
]

class HandGestureRecognizer():
    class Triangle():
        def __init__(self, p1, p2, p3):
            self._p1 = p1
            self._p2 = p2
            self._p3 = p3

        def area(self):
            return abs((self._p2.x - self._p1.x) * (self._p3.y - self._p1.y) - (self._p2.y - self._p1.y) * (self._p3.x - self._p1.x)) / 2

        def contains(self, p):
            area_sum = HandGestureRecognizer.Triangle(self._p1, self._p2, p).area()
            area_sum += HandGestureRecognizer.Triangle(self._p1, self._p3, p).area()
            area_sum += HandGestureRecognizer.Triangle(self._p2, self._p3, p).area()
            return area_sum <= self.area()

    def recognize(self, hand_detection_result):
        hand_landmarks_list = hand_detection_result.hand_landmarks
        handedness_list = hand_detection_result.handedness
        gesture_result = []

        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            hand_gesture = {
                'type': handedness[0].category_name,
                'status': [0, 0, 0, 0, 0]
            }

            for p in range(5):
                finger = FINGERS[p]
                if p == 0:
                    base = hand_landmarks[FINGERS[1][0]]
                    triangle = self.Triangle(hand_landmarks[0], hand_landmarks[FINGERS[1][-1]], hand_landmarks[FINGERS[-1][-1]])
                    p1 = hand_landmarks[finger[2]]
                    p2 = hand_landmarks[finger[3]]
                    d1 = self.squareDistance(p1, base)
                    d2 = self.squareDistance(p2, base)
                    if d2 > d1 and not triangle.contains(p1) and not triangle.contains(p2):
                        hand_gesture['status'][p] = 1
                else:
                    base = hand_landmarks[0]
                    d1 = self.squareDistance(hand_landmarks[finger[0]], base)
                    d2 = self.squareDistance(hand_landmarks[finger[2]], base)
                    d3 = self.squareDistance(hand_landmarks[finger[3]], base)
                    if d3 > d1 and d3 > d2:
                        hand_gesture['status'][p] = 1

            gesture_result.append(hand_gesture)

        return gesture_result

    def squareDistance(self, p1, p2):
        return pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2)

    def distance(self, p1, p2):
        return math.sqrt(self.square_distance(p1, p2))