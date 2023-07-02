import cv2

# Colors
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_ORANGE = (36, 151, 227)

# Typography
FONT_FAMILY = cv2.FONT_HERSHEY_PLAIN
FONT_SIZE = 2
FONT_THICKNESS = 2
LINE_TYPE = cv2.LINE_AA
MARGIN = 10

# Shapes
LINE_STROKE = 3

# Fingers
FINGERS = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20]
]

def putTextOnImage(image, text, position, color):
    cv2.putText(image, text, position, FONT_FAMILY, FONT_SIZE, color, FONT_THICKNESS, LINE_TYPE)