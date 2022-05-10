import pyautogui as gui

gui.FAILSAFE = False

def mouseMove(x, y):
    c_x, c_y = gui.position()
    if gui.onScreen(c_x + x, c_y + y):
        gui.move(x, y)