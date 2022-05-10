import cv2
import time
import pyautogui
from handtracker import HandTracker

FPS_POSITION = (10, 50)
FPS_FONT = cv2.FONT_HERSHEY_PLAIN
FPS_FONT_SCALE = 2
FPS_COLOR = (255, 0, 0)
FPS_FONT_THICKNESS = 2

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def main():
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
            hand_pos = hand_tracker.position[0]
            status = hand_tracker.detect_fingers(hand_pos)
            print(status)

            # mouse actions depending hand gestures
            if status == [0, 1, 0, 0, 0]:
                # move the mouse
                pointer = hand_pos[8]
                center = (pointer['x'], pointer['y'])
                cv2.circle(img, center, 10, (0, 255, 0), -1)
            elif status == [0, 1, 1, 0, 0]:
                # pointer1 = hand_pos[8]
                # pointer2 = hand_pos[12]
                # center1 = (pointer1['x'], pointer1['y'])
                # center2 = (pointer2['x'], pointer2['y'])
                # cv2.circle(img, center1, 10, (0, 255, 0), -1)
                # cv2.circle(img, center2, 10, (0, 255, 0), -1)
                # d = hand_tracker.distance(pointer1, pointer2)
                # print(d)
                pass
    
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        text = "FPS: %s" % str(int(fps))

        img = cv2.flip(img, 1)

        cv2.putText(img, text, FPS_POSITION, FPS_FONT, FPS_FONT_SCALE, FPS_COLOR, FPS_FONT_THICKNESS)

        cv2.imshow("Virtual Mouse", img)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()