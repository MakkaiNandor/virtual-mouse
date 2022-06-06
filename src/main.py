import cv2
import time
import threading
import utils
from handtracker import HandTracker
from mouse import VirtualMouse, Mouse
from handgesture import HandGestureDetector

# actions = ["nothing", "mouse_move", "click"]

def main():
    hand_tracker = HandTracker(max_hands=1)
    mouse = Mouse()
    gesture_detector = HandGestureDetector()

    cap = cv2.VideoCapture(0)

    p_time = 0
    c_time = 0

    p_pos_x = None
    p_pos_y = None
    c_pos_x = None
    c_pos_y = None
    velocity = 2
    smooth = 5
    move_mouse = False
    ACTION_NAME = "Nothing"

    while cap.isOpened():
        success, img = cap.read()

        if not success:
            continue

        img = hand_tracker.find_hands(img)

        if len(hand_tracker.position) > 0:
            hand_pos = hand_tracker.position[0]
            status = hand_tracker.detect_fingers(hand_pos)
            # print(status)

            # mouse actions depending hand gestures
            if status == [0, 1, 0, 0, 0]:
                velocity = 2
                move_mouse = True
                ACTION_NAME = "Move Mouse"
            elif status == [0, 1, 1, 0, 0]:
                velocity = 5
                move_mouse = True
                ACTION_NAME = "Move Mouse Faster"
            else:
                move_mouse = False
                ACTION_NAME = ""
                p_pos_x = None
                p_pos_y = None
                c_pos_x = None
                c_pos_y = None

            if move_mouse:
                pointer = hand_pos[8]
                c_pos_x = pointer['x']
                c_pos_y = pointer['y']
                cv2.circle(img, (c_pos_x, c_pos_y), 10, (0, 255, 0), -1)
                if not p_pos_x is None and not p_pos_y is None:
                    offset_x = (p_pos_x - c_pos_x) * velocity
                    offset_y = - (p_pos_y - c_pos_y) * velocity
                    threading.Thread(target=mouse.moveBy, args=(offset_x, offset_y), daemon=True).start()
                p_pos_x = c_pos_x
                p_pos_y = c_pos_y

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        # text = "FPS: %s" % str(int(fps))
        text = ACTION_NAME

        img = cv2.flip(img, 1)

        utils.put_text(img, text)

        cv2.imshow("Virtual Mouse", img)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()