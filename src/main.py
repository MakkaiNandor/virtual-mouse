import cv2
import time
import pyautogui
from handTracker import HandTracker

FPS_POSITION = (10, 70)
FPS_FONT = cv2.FONT_HERSHEY_PLAIN
FPS_FONT_SCALE = 3
FPS_COLOR = (255, 0, 255)
FPS_FONT_THICKNESS = 3

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

hand_tracker = HandTracker(max_hands=1)

cap = cv2.VideoCapture(0)

p_time = 0
c_time = 0

while cap.isOpened():
    success, img = cap.read()

    if not success:
        continue

    img = hand_tracker.find_hands(img)

    if len(hand_tracker.position) > 0:
        pos = hand_tracker.position[0]

    # c_time = time.time()
    # fps = 1 / (c_time - p_time)
    # p_time = c_time

    # text = str(int(fps))
    # text = str(SCREEN_WIDTH) + ":" + str(SCREEN_HEIGHT)

    img = cv2.flip(img, 1)

    # cv2.putText(img, text, FPS_POSITION, FPS_FONT, FPS_FONT_SCALE, FPS_COLOR, FPS_FONT_THICKNESS)

    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()