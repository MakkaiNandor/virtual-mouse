import cv2
import time
import utils
from handtracker import HandTracker
from mouse import VirtualMouse
from handgesture import HandGestureDetector, FINGERS

def main():
    hand_tracker = HandTracker(max_hands=1)
    v_mouse = VirtualMouse()
    gesture_detector = HandGestureDetector()

    cap = cv2.VideoCapture(0)

    p_landmarks = None
    landmarks = None

    clicked = False
    dragged = False

    while cap.isOpened():
        success, img = cap.read()

        if not success:
            continue

        hand_tracker.find_hands(img)

        landmarks = hand_tracker.get_landmarks(0)

        if p_landmarks is None:
            p_landmarks = landmarks
            continue

        mouse_action, fingers_status = gesture_detector.detect(landmarks)

        for i in range(1, 5):
            if fingers_status[i] == 1:
                cv2.circle(img, (landmarks[FINGERS[i][-1]]['x'], landmarks[FINGERS[i][-1]]['y']), 7, (0, 255, 0), -1)

        if not mouse_action == "click" and clicked:
            clicked = False

        if not mouse_action == "drag" and dragged:
            dragged = False
            v_mouse.dragStop()

        if mouse_action == "click" and not clicked:
            clicked = True
            v_mouse.click()
        elif mouse_action == "drag" and not dragged:
            dragged = True
            v_mouse.dragStart()

        if mouse_action in ["move", "move_faster", "drag"] and 8 in p_landmarks and 8 in landmarks:
            velocity = 5 if mouse_action == "move_faster" else 2
            offset_x = (p_landmarks[8]['x'] - landmarks[8]['x']) * velocity
            offset_y = - (p_landmarks[8]['y'] - landmarks[8]['y']) * velocity
            v_mouse.moveBy(offset_x, offset_y)

        p_landmarks = landmarks

        img = cv2.flip(img, 1)

        utils.put_text(img, mouse_action)

        cv2.imshow("Virtual Mouse", img)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()