import cv2
import mediapipe as mp
import time
import pyautogui

FPS_POSITION = (10, 70)
FPS_FONT = cv2.FONT_HERSHEY_PLAIN
FPS_FONT_SCALE = 3
FPS_COLOR = (255, 0, 255)
FPS_FONT_THICKNESS = 3

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

p_time = 0
c_time = 0

with mp_hands.Hands() as hands:
    while cap.isOpened():
        success, img = cap.read()

        if not success:
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        text = str(int(fps))
        # text = str(SCREEN_WIDTH) + ":" + str(SCREEN_HEIGHT)

        img = cv2.flip(img, 1)

        cv2.putText(img, text, FPS_POSITION, FPS_FONT, FPS_FONT_SCALE, FPS_COLOR, FPS_FONT_THICKNESS)

        cv2.imshow("Virtual Mouse", img)

        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()
