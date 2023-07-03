import pyautogui
import threading
from mouse.utils import *

class MouseControl():
    def __init__(self, hands, navigation, main_hand, ref_points, mouse_sensitivity):
        self._hands = hands
        self._navigation = navigation
        self._main_hand = main_hand
        self._ref_points = ref_points
        self._mouse_sensitivity = mouse_sensitivity
        self._landmarks = None
        self._prev_pos = None
        self._curr_pos = None
        self._prev_method = None
        
    def checkStates(self, method):
        if self._prev_method == 'drag_and_drop' and not method == 'drag_and_drop':
            self.runAsync(pyautogui.mouseUp)

    def execute(self, landmarker_result, gestures):
        self._landmarks = landmarker_result.hand_landmarks

        if not len(gestures) == self._hands:
            # not enough hands are detected
            return False, None

        if self._hands == 2:
            # order the detected gestures -> [Left, Right]
            if not list(gestures.keys()).index('Left') == 0:
                self._landmarks = [self._landmarks[1], self._landmarks[0]]
            gestures = [gestures['Left'], gestures['Right']]
        else:
            gestures = list(gestures.values())

        active_method = None
        for method_name, method_gestures in self._navigation.items():
            if len(method_gestures) == len(gestures):
                status = []
                for i in range(len(gestures)):
                    status.append(method_gestures[i] == gestures[i])
                if all(status):
                    active_method = method_name
                    break

        self.checkStates(active_method)
        
        if active_method is None:
            self._prev_pos = None
            self._curr_pos = None
        else:
            print('Action:', active_method)
            getattr(self, active_method)()

        self._prev_method = active_method

        return active_method

    def move(self):
        self._curr_pos = self._landmarks[self._main_hand][self._ref_points['move']]
        if self._prev_pos is not None:
            diff_x = self._curr_pos.x - self._prev_pos.x
            if abs(diff_x) > MOUSE_MOVE_TRESHOLD:
                diff_x *= self._mouse_sensitivity

            diff_y = self._curr_pos.y - self._prev_pos.y
            if abs(diff_y) > MOUSE_MOVE_TRESHOLD:
                diff_y *= self._mouse_sensitivity

            self.runAsync(pyautogui.move, (diff_x, diff_y))

        self._prev_pos = self._curr_pos
        self._curr_pos = None

    def faster_move(self):
        self._curr_pos = self._landmarks[self._main_hand][self._ref_points['move']]
        if self._prev_pos is not None:
            diff_x = self._curr_pos.x - self._prev_pos.x
            if abs(diff_x) > MOUSE_MOVE_TRESHOLD:
                diff_x *= self._mouse_sensitivity * 2

            diff_y = self._curr_pos.y - self._prev_pos.y
            if abs(diff_y) > MOUSE_MOVE_TRESHOLD:
                diff_y *= self._mouse_sensitivity * 2

            self.runAsync(pyautogui.move, (diff_x, diff_y))

        self._prev_pos = self._curr_pos
        self._curr_pos = None

    def left_click(self):
        if self._prev_method == 'left_click':
            self.move()
        else:
            self.runAsync(pyautogui.click)

    def right_click(self):
        if self._prev_method == 'right_click':
            self.move()
        else:
            self.runAsync(pyautogui.click, button='right')

    def double_left_click(self):
        if self._prev_method == 'double_left_click':
            self.move()
        else:
            self.runAsync(pyautogui.doubleClick)

    def drag_and_drop(self):
        if not self._prev_method == 'drag_and_drop':
            self.runAsync(pyautogui.mouseDown)
        self.move()

    def scroll(self):
        self._curr_pos = self._landmarks[self._main_hand][self._ref_points['scroll']]
        if self._prev_pos is not None:
            diff_x = self._prev_pos.x - self._curr_pos.x
            if abs(diff_x) > MOUSE_MOVE_TRESHOLD:
                # diff_x = 0
                diff_x *= SCROLL_SENSITIVITY

            diff_y = self._prev_pos.y - self._curr_pos.y
            if abs(diff_y) > MOUSE_MOVE_TRESHOLD:
                # diff_y = 0
                diff_y *= SCROLL_SENSITIVITY

            if diff_x > diff_y:
                self.runAsync(pyautogui.hscroll, diff_x)
            else:
                self.runAsync(pyautogui.vscroll, diff_y)

        self._prev_pos = self._curr_pos
        self._curr_pos = None

    def runAsync(self, func, *args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()