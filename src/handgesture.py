import math

FINGERS = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20]
]

class HandGestureDetector:
    def detect(self, landmarks):
        """
        Detect which fingers are up and which mouse action is active.
        Arguments:
            landmarks: Position of a single hand.
        Returns:
            Mouse action to do depending the hand gesture.
        """
        status = [0, 0, 0, 0, 0] # Thumb, Index, Middle, Ring and Pinky finger.

        if landmarks:
            for idx in range(1, 5):
                finger = FINGERS[idx]
                base = landmarks.get(0)
                d1 = self.square_distance(landmarks.get(finger[0]), base)
                d2 = self.square_distance(landmarks.get(finger[2]), base)
                d3 = self.square_distance(landmarks.get(finger[3]), base)
                if d3 > d1 and d3 > d2:
                    status[idx] = 1

        if status == [0, 1, 0, 0, 0]: # Index finger is UP
            action = "move"
        elif status == [0, 1, 1, 0, 0]: # Index and Middle finger are UP
            action = "move_faster"
        elif status == [0, 1, 0, 0, 1] or status == [0, 1, 1, 0, 1]: # Index and Pinky finger are UP
            action = "click"
        elif status == [0, 1, 1, 1, 1]:
            action = "drag"
        else:
            action = None

        return action, status

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