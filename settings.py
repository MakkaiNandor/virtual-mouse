import yaml
import json
from utils import FINGERS

default_settings = {
    'camera': 0,
    'hands': 1,
    'face': False,
    'face_method': 'eigen',
    'main_hand': 'Right',
    'navigation': {
        'move': ['01000'],
        'faster_move': ['01100'],
        'left_click': ['11000'],
        'right_click': ['01001'],
        'double_left_click': ['11100'],
        'drag_and_drop': ['01111'],
        'scroll': ['01110']
    },
    'mouse_sensitivity': 3.5
}

try:
    with open('settings.yaml', 'r') as f:
        settings = {**default_settings, **yaml.safe_load(f)}
except yaml.YAMLError as exc:
    settings = default_settings

# print(json.dumps(settings, indent=4))

def getSettings():
    try:
        with open('settings.yaml', 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        return {}

def saveSettings(data=None):
    if data is None:
        data = settings
    with open('settings.yaml', 'w') as f:
        yaml.dump(data, f)

def getMainHand():
    main_hand = 0
    
    if settings['hands'] == 2:
        if settings['main_hand'] == 'Left':
            main_hand = 0
        elif settings['main_hand'] == 'Right':
            main_hand = 1
    
    return main_hand

def getReferencePoints():
    main_hand = getMainHand()

    ref_points = {}

    for method_name, method_gestures in settings['navigation'].items():
        gesture = method_gestures[main_hand]
        first_finger_up = gesture.find('1')
        ref_points[method_name] = FINGERS[first_finger_up][-1]

    return ref_points