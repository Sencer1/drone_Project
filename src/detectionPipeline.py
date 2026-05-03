from utils.drawUtils import kutuCiz
from utils.boxUtils import nmsUygula
from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/visdroneYolov8n50-2/weights/best.pt")

def yoloDetectionUret(image, confidenceThreshold=0.5, allowedLabels=None):
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
            if conf < confidenceThreshold:
                continue

            label = model.names[cls]

            if allowedLabels is not None and label not in allowedLabels:
                continue

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



def sinifSayilariniCiz(frame, detections, baslangicY=120):
    sinifSayilari = {}

    for detection in detections:
        label = detection[4]

        if label not in sinifSayilari:
            sinifSayilari[label] = 0

        sinifSayilari[label] += 1

    yKonum = baslangicY

    for label, sayi in sinifSayilari.items():
        cv2.putText(
            frame,
            f"{label}: {sayi}",
            (20, yKonum),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        yKonum += 30

    return frame

# Tracking için bu kısım

def merkezNoktasiHesapla(detection):
    x, y, w, h = detection[:4]
    # // aşağıya yuvarlayarak böl
    merkezX = x + w // 2
    merkezY = y + h // 2

    return merkezX, merkezY


def merkezNoktalariniCiz(frame, detections):
    for detection in detections:
        merkezX, merkezY = merkezNoktasiHesapla(detection)

        # görüntü üzerine daire çiziyor yar 
        cv2.circle(frame, (merkezX, merkezY), 4, (0, 0, 255), -1)

    return frame

def trackedObjectsCiz(frame, trackedObjects):
    # .items() dic içindeki hem anahtaralrı döner hem de value ları
    for objectId, data in trackedObjects.items():
        centerX, centerY, detection = data
        x, y, w, h, label, confidence = detection

        cv2.putText(
            frame,
            f"ID{objectId}",
            (x, y - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,0,255),
            2
        )
        # -1 değerri daireyi doldurur 
        cv2.circle(frame, (centerX, centerY), 4, (0, 0, 255), -1)

    return frame