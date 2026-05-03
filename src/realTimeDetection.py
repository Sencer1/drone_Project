import cv2
from detectionPipeline import yoloDetectionUret, detectionCiz, sinifSayilariniCiz, merkezNoktalariniCiz, trackedObjectsCiz
import time
from centroidTracker import CentroidTracker
# video kaynağı oluşturuyor burası VideoCapture 0 yazınca da pc kamerasını açıyor
# kamera objesi oluşturduk cap ile
def kameraIleRealTimeDetection():
    cap = cv2.VideoCapture(0)

    #  kamera açıldı mı kontrol ediliyor
    if not cap.isOpened():
        print("Kamera acilmadi")

        exit()
    oncekiZaman = time.time()

    tracker = CentroidTracker(maxDistance=80, maxMissingFrame=10)


    while True:
        # kamera objesi okunuyor burda
        # ret frame başarıyla alındı mı onu tutuyor boolean 
        #  frame görüntüsnün kendisi
        ret, frame = cap.read()
        #  frame alınamadı false oluyor
        if not ret:
            print("Frame okunamadi")
            break
        # frame ile modele veriyoruz kutuları alıyoruz
        allowedLabels = ["person", "car", "bus", "truck", "bicycle"]
        detections = yoloDetectionUret(frame, confidenceThreshold=0.5, allowedLabels=allowedLabels)

        # buraya da centroid tracker koyuyoruz

        trackedObjects = tracker.update(detections)
        # print(trackedObjects)

        # sonra o frame çizim yapıyoruz
        frame = detectionCiz(frame, detections)
        frame = trackedObjectsCiz(frame, trackedObjects)
        frame = sinifSayilariniCiz(frame, detections, baslangicY=120)

        # burda merkezleri çiziyoruz
        frame = merkezNoktalariniCiz(frame, detections)
        
        # # toplam nesne sayısnı ekrana basıyoruz
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

        #  bu da ekranda göstermek için
        cv2.imshow("Real time drone detection", frame)
        # 1ms ile klavyeden giriş bekliyor waitkey
        #  ord karakterin ascii kodunu veriyor
        # aldığı kalvyeden keey  in son 8 bitini alıyor 0xFF ile sonra da kıyas yapıyorsun
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    # burası kamerayı serbest bırakır
    cap.release()
    # bu da tüm pencereleri kapatıyor
    cv2.destroyAllWindows()