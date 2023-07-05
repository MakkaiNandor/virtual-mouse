import os
from utils import *

BASEPATH = 'hands'

PATHS = {
    'model_file': os.path.join(BASEPATH, 'hand_landmarker.task')
}

class Triangle():
    def __init__(self, p1, p2, p3):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3

    def area(self):
        return abs(self._p1.x * (self._p2.y - self._p3.y) + self._p2.x * (self._p3.y - self._p1.y) + self._p3.x * (self._p1.y - self._p2.y)) / 2

    def contains(self, p):
        area_sum = Triangle(self._p1, self._p2, p).area()
        area_sum += Triangle(self._p1, self._p3, p).area()
        area_sum += Triangle(self._p2, self._p3, p).area()
        return area_sum <= self.area()