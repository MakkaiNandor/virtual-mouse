import pyautogui as gui

gui.FAILSAFE = False

class VirtualMouse:
    def __init__(self):
        pass

class Mouse:
    def moveBy(self, x, y):
        c_x, c_y = gui.position()
        if gui.onScreen(c_x + x, c_y + y):
            gui.move(x, y)