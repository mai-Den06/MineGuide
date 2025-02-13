import logging

from ultralytics import YOLO

from config.setting import MODEL_PATH

logging.getLogger('ultralytics').setLevel(logging.WARNING)

model = YOLO(MODEL_PATH)

def pred(image):
    results = model(image, save=False)
    return results[0]
