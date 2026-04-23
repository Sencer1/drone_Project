from utils.drawUtils import kutuCiz
from utils.boxUtils import nmsUygula
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

# def sahteDetectionUret():
#     return [
#         (100, 100, 200, 150, "Arac", 0.92),
#         (110, 110, 195, 145, "Arac", 0.88),
#         (350, 120, 120, 180, "Insan", 0.81),
#         (500, 300, 180, 120, "Arac", 0.76)
#     ]

def yoloDetectionUret(image):
    results = model(image)

    detections = []

    for result in results:
        boxes = result.boxes

        for box in boxes:
            # burası  xyxy kutunun kordinatlarını veriyor liste içindeki listeyi almak için 0 yazdık
            # pytorch tensor ü  pyhton listesi yapar iç yapıları normal listeden farklı
            # daha hızlı işlem yapmak için gpu da çalışması için büyük matrixler için tensor liste nin optimize ediliş hali 
            # daha büyük matris işlemleri için
            x1,y1,x2,y2 = box.xyxy[0].tolist()
            # ne kadar emin box dan onu aldık burda
            conf = float(box.conf[0])
            #  bulnana nesenenin class ını aldık burda 
            cls = int(box.cls[0])
            #  sınıf numarasını isme çevirdik burda da
            label = model.names[cls]

            w = x2 - x1
            h = y2 - y1
            #  burda da tespiti listeye ekledik
            detections.append((int(x1), int(y1), int(w), int(h), label, conf))

    return detections



def nmsUygulaWrapper(detections):
    return nmsUygula(detections, iouThreshold=0.5)

def detectionCiz(image, detections):
    for x, y, w, h, label, confidence in detections:
        image = kutuCiz(image, x, y, w, h, label, confidence)

    return image