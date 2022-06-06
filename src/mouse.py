import pyautogui as gui
import threading

gui.FAILSAFE = False

class VirtualMouse:
    def moveBy(self, x, y):
        c_x, c_y = gui.position()
        if gui.onScreen(c_x + x, c_y + y):
            threading.Thread(target=gui.move, args=(x, y), daemon=True).start()

    def click(self):
        threading.Thread(target=gui.click, daemon=True).start()

    def dragStart(self):
        threading.Thread(target=gui.mouseDown(), daemon=True).start()

    def dragStop(self):
        threading.Thread(target=gui.mouseUp(), daemon=True).start()