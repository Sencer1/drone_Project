import cv2
from detectionPipeline import yoloDetectionUret, detectionCiz
import time

def videoIleDetection(videoYolu):

    cap = cv2.VideoCapture(videoYolu)

    if not cap.isOpened():
        print("video alınamdı")
        exit()
    # o anki zamanaı aldık burda
    oncekiZaman = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("video bitti veya frame okunamadı")
            break

        detections = yoloDetectionUret(frame)
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

        cv2.imshow("Video detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()