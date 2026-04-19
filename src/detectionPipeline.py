from utils.drawUtils import kutuCiz
from utils.boxUtils import nmsUygula

def sahteDetectionUret():
    return [
        (100, 100, 200, 150, "Arac", 0.92),
        (110, 110, 195, 145, "Arac", 0.88),
        (350, 120, 120, 180, "Insan", 0.81),
        (500, 300, 180, 120, "Arac", 0.76)
    ]


def nmsUygulaWrapper(detections):
    return nmsUygula(detections, iouThreshold=0.5)

def detectionCiz(image, detections):
    for x, y, w, h, label, confidence in detections:
        image = kutuCiz(image, x, y, w, h, label, confidence)

    return image