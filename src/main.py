import cv2
import time
import threading
from handtracker import HandTracker
import mouse

TEXT_POSITION = (10, 50)
TEXT_FONT = cv2.FONT_HERSHEY_PLAIN
TEXT_FONT_SCALE = 2
TEXT_COLOR = (255, 0, 0)
TEXT_FONT_THICKNESS = 2

def main():
    hand_tracker = HandTracker(max_hands=1)

    cap = cv2.VideoCapture(0)

    p_time = 0
    c_time = 0

    p_pos_x = None
    p_pos_y = None
    c_pos_x = None
    c_pos_y = None
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
                # move the mouse
                ACTION_NAME = "Move Mouse"
                pointer = hand_pos[8]
                c_pos_x = pointer['x']
                c_pos_y = pointer['y']
                cv2.circle(img, (c_pos_x, c_pos_y), 10, (0, 255, 0), -1)
                if not p_pos_x is None and not p_pos_y is None:
                    offset_x = p_pos_x - c_pos_x
                    offset_y = c_pos_y - p_pos_y
                    t = threading.Thread(target=mouse.mouseMove, args=(offset_x, offset_y), daemon=True)
                    t.start()
                p_pos_x = c_pos_x
                p_pos_y = c_pos_y
            elif status == [0, 1, 1, 0, 0]:
                # move the mouse faster
                ACTION_NAME = "Move Mouse Faster"
                pointer = hand_pos[8]
                c_pos_x = pointer['x']
                c_pos_y = pointer['y']
                cv2.circle(img, (c_pos_x, c_pos_y), 10, (0, 255, 0), -1)
                if not p_pos_x is None and not p_pos_y is None:
                    offset_x = (p_pos_x - c_pos_x) * 5
                    offset_y = (c_pos_y - p_pos_y) * 5
                    t = threading.Thread(target=mouse.mouseMove, args=(offset_x, offset_y), daemon=True)
                    t.start()
                p_pos_x = c_pos_x
                p_pos_y = c_pos_y
                pass
            else:
                ACTION_NAME = "Nothing"
                p_pos_x = None
                p_pos_y = None
                c_pos_x = None
                c_pos_y = None
    
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        # text = "FPS: %s" % str(int(fps))
        text = ACTION_NAME

        img = cv2.flip(img, 1)

        cv2.putText(img, text, TEXT_POSITION, TEXT_FONT, TEXT_FONT_SCALE, TEXT_COLOR, TEXT_FONT_THICKNESS)

        cv2.imshow("Virtual Mouse", img)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()