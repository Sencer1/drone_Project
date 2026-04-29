import cv2
from detectionPipeline import yoloDetectionUret, detectionCiz, sinifSayilariniCiz, merkezNoktalariniCiz
import time
from centroidTracker import CentroidTracker


def videoIleDetection(videoYolu):

    cap = cv2.VideoCapture(videoYolu)

    if not cap.isOpened():
        print("video alınamdı")
        exit()
    # o anki zamanı aldık burda
    oncekiZaman = time.time()

    tracker = CentroidTracker()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("video bitti veya frame okunamadı")
            break
        # burası izin verdiklerimizin sadece gözükmesi detect edilmesi için
        allowedLabels = ["person", "car", "bus", "truck", "bicycle"]
        detections = yoloDetectionUret(frame, confidenceThreshold=0.5, allowedLabels=allowedLabels)

        # buraya da centroid tracker koyuyoruz

        trackedObjects = tracker.update(detections)
        print(trackedObjects)
        frame = detectionCiz(frame, detections)
        frame = sinifSayilariniCiz(frame, detections, baslangicY=120)
        
        # burası merkez çizme
        frame = merkezNoktalariniCiz(frame, detections) 

        # # labellara göre sayı ekleme
        # sinifSayilari = {}
        # for detection in detections:
        #     label = detection[4]

        #     if label not in sinifSayilari:
        #         sinifSayilari[label] = 0
            
        #     sinifSayilari[label] += 1

        # toplam nesne sayısnı ekrana basıyoruz
        # nesneSayisi = len(detections)

        # cv2.putText(
        #     frame,
        #     f"Nesne sayisi: {nesneSayisi}",
        #     (20, 80),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     1,
        #     (0, 255, 0),
        #     2
        # )

        simdikiZaman = time.time()
        fps = 1 / (simdikiZaman - oncekiZaman)
        oncekiZaman = simdikiZaman

        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # yKonum = 120

        # for label, sayi in sinifSayilari.items():
        #     cv2.putText(
        #         frame,
        #         f"{label}: {sayi}",
        #         (20, yKonum),
        #         cv2.FONT_HERSHEY_SIMPLEX,
        #         0.8,
        #         (0, 255, 0),
        #         2
        #     )
        #     yKonum += 30

        cv2.imshow("Video detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()