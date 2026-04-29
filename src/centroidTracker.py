import math
#  burası merkezleri takip etmek için şu an sadece her frame de detectionlara id veriyor
class CentroidTracker:
    def __init__(self):
        self.nextObjectId = 1
        self.objects = {}


    def update(self, detections):
        updatedObjects = {}

        for detection in detections:
            x, y, w, h = detection[:4]

            centerX = x + w // 2
            centerY = y + h // 2

            objectId = self.nextObjectId
            self.nextObjectId += 1

            updatedObjects[objectId] = (centerX, centerY, detection)

        self.objects = updatedObjects

        return self.objects