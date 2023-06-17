import cv2
import os

PATHS = {
    'basedir': 'face',
    'images': os.path.join('face', 'images'),
    'models': os.path.join('face', 'models'),
    'cascade_file': cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
}

METHODS = {
    'eigen': {
        'treshold': 3000,
        'function': cv2.face.EigenFaceRecognizer_create,
        'file': 'model_eigen.xml'
    },
    'lbph': {
        'treshold': 85,
        'function': cv2.face.LBPHFaceRecognizer_create,
        'file': 'model_lbph.xml'
    }
    # 'fisher': {
    #     'treshold': 300,
    #     'function': cv2.face.FisherFaceRecognizer_create,
    #     'file': 'model_fisher.xml'
    # }
}

FACE_SIZE = (100, 100)
RESIZE_FACTOR = 4
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5
MIN_SIZE = (30, 30)
LINE_STROKE = 3
FONT_FAMILY = cv2.FONT_HERSHEY_PLAIN
FONT_SIZE = 2
FONT_WEIGHT = 2
DEFAULT_COLOR = (255, 0, 0)
SUCCESS_COLOR = (0, 255, 0)
FAILURE_COLOR = (0, 0, 255)
TRAIN_NR_FACES = 100
TRAIN_IMG_FREQ = 5

def createDirIfNotExists(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def deleteDirContent(dir_path):
    if os.path.isdir(dir_path):
        for fn in os.listdir(dir_path):
            path = os.path.join(dir_path, fn)
            try:
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                pass

def deleteTrainingImages():
    deleteDirContent(PATHS['images'])

def deleteTrainedModels():
    deleteDirContent(PATHS['models'])

def deleteTrainedModelByMethod(method):
    if method in METHODS:
        path = os.path.join(PATHS['models'], METHODS[method]['file'])
        if os.path.isfile(path):
            os.unlink(path)