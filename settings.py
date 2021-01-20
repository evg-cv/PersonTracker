import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(CUR_DIR, 'utils', 'model')
CAFFEMODEL_PATH = os.path.join(MODEL_DIR, 'SSD_MobileNet.caffemodel')
PROTOTXT_PATH = os.path.join(MODEL_DIR, 'SSD_MobileNet_prototxt.txt')
YOLO_WEIGHT_PATH = os.path.join(MODEL_DIR, 'yolov3-tiny.weights')
YOLO_CONFIG_PATH = os.path.join(MODEL_DIR, 'yolov3-tiny.cfg')
YOLO_COCO_PATH = os.path.join(MODEL_DIR, 'coco.names')
PB_MODEL_PATH = os.path.join(MODEL_DIR, 'frcnn_inception_v2.pb')
PB_TEXT_PATH = os.path.join(MODEL_DIR, 'frcnn_inception_v2_graph.pbtxt')

DETECT_CONFIDENCE = 0.5
PERSON_TRACK_CYCLE = 20
MARGIN = 0
TRACK_QUALITY = 2
OVERLAP_THRESH = 0.7
UNDETECTED_THRESH = 5

GPU = True

SAFE_DISTANCE = 200
FOCUS_LENGTH = 615
