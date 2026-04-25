import cv2
from detectionPipeline import yoloDetectionUret, detectionCiz 
import time
# video kaynağı oluşturuyor burası VideoCapture 0 yazınca da pc kamerasını açıyor
# kamera objesi oluşturduk cap ile
def kameraIleRealTimeDetection():
    cap = cv2.VideoCapture(0)

    #  kamera açıldı mı kontrol ediliyor
    if not cap.isOpened():
        print("Kamera acilmadi")

        exit()
    oncekiZaman = time.time()

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
        detections = yoloDetectionUret(frame)
        # sonra o frame çizim yapıyoruz
        frame = detectionCiz(frame, detections)
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