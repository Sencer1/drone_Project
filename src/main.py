from utils.imageUtils import goruntuOku, goruntuGoster, goruntuKaydet
from utils.drawUtils import kutuCiz
from utils.boxUtils import iouHesapla
from utils.boxUtils import nmsUygula
from detectionPipeline import nmsUygulaWrapper, detectionCiz
from detectionPipeline import yoloDetectionUret
from utils.annotationUtils import yoloToPixelBox, yoloAnnotationOku
from utils.annotationUtils import labelPathBul
from utils.annotationUtils import imageDosyalariGetir
import os
from realTimeDetection import kameraIleRealTimeDetection
from videoDetection import videoIleDetection


# ---------------------------------------------------------------------------------------------
# image = goruntuOku("deneme1-1.jpg")

# if image is not None:
#     # x = 100
#     # y = 100
#     # w = 200
#     # h = 150
    
#     # image = kutuCiz(image, x, y, w, h, "kara delik")
    
#     detections = [
#         (10, 10, 20, 15, "Arac", 0.92),
#         (35, 12, 12, 18, "Insan", 0.81),
#         (50, 30, 18, 12, "Arac", 0.76)
#     ]
#     for x, y, w, h, label, confidence in detections:
#         image = kutuCiz(image, x, y, w, h, label, confidence)

#     goruntuGoster(image)

    
# ---------------------------------------------------------------------------------------------
# box1 = (100, 100, 200, 150)
# box2 = (110, 110, 195, 145)

# iou = iouHesapla(box1, box2)

# print("IoU:", iou)

# # # nms non max suppression
# # bunla üst üste gelen aynı kutuları ayırt ediyoruz 
# # # aynı objeyi farklı kutular göstermiyor
# # iou intersection over union bunu hesaplayıp aynı mı ayrı kutular mı ona bakıcaz

# detections = [
#     (100, 100, 200, 150, "Arac", 0.92),
#     (110, 110, 195, 145, "Arac", 0.88),
#     (350, 120, 120, 180, "Insan", 0.81),
#     (500, 300, 180, 120, "Arac", 0.76)
# ]

# sonuc = nmsUygula(detections, iouThreshold=0.5)

# print("NMS sonrasi:")
# for detection in sonuc:
#     print(detection)

# ---------------------------------------------------------------------------------------------
# if image is not None:
#     detections = [
#         (100, 100, 200, 150, "Arac", 0.92),
#         (110, 110, 195, 145, "Arac", 0.88),
#         (350, 120, 120, 180, "Insan", 0.81),
#         (500, 300, 180, 120, "Arac", 0.76)
#     ]

#     nmsOncesiImage = image.copy()

#     for x, y, w, h, label, confidence in detections:
#         nmsOncesiImage = kutuCiz(nmsOncesiImage, x, y, w, h, label, confidence)


#     goruntuGoster(nmsOncesiImage, "NMS Oncesi")

#     secilenDetections = nmsUygula(detections, iouThreshold=0.5)

#     nmsSonrasıImage = image.copy()

#     for x, y, w, h, label, confidence in secilenDetections:
#         nmsSonrasıImage = kutuCiz(nmsSonrasıImage, x, y, w, h, label, confidence)

#     goruntuGoster(nmsSonrasıImage, "NMS Sonrasi")  


# burası daha temiz hali 
# ---------------------------------------------------------------------------------------------
# if image is not None:
#     detections = yoloDetectionUret(image)

#     nmsOncesi = detectionCiz(image.copy(), detections)
#     goruntuGoster(nmsOncesi, "NMS oncesi")

#     temizDetections = nmsUygulaWrapper(detections)

#     nmsSonrasi = detectionCiz(image.copy(), temizDetections)
#     goruntuGoster(nmsSonrasi, "NMS sonrasi")

    # yolo tabanlı computer vision modellerini kullanmak için
    # pip install ultralytics

# ---------------------------------------------------------------------------------------------
#  yolo ya çevirmeyi test ediyoruz burda

# x, y, w, h = yoloToPixelBox(
#     xCenter=0.5,
#     yCenter=0.4,
#     width=0.2,
#     height=0.1,
#     imageWidth=1000,
#     imageHeight=800
# )

# print(x, y, w, h)
# ---------------------------------------------------------------------------------------------
# className = {
#     0: "arac",
#     1: "insan"
# }

# if image is not None:
#     imageHeight, imageWidth = image.shape[:2]

#     annotations = yoloAnnotationOku("indir.txt")

#     for classId, xCenter, yCenter, width, height in annotations:
#         x, y, w, h = yoloToPixelBox(
#             xCenter,
#             yCenter,
#             width,
#             height,
#             imageWidth,
#             imageHeight
#         )

#         label = className.get(classId, "Bilinmeyen")
#         image = kutuCiz(image, x, y, w, h, label, 1.00)

#     goruntuGoster(image)

# ---------------------------------------------------------------------------------------------
# classNames = {
#     0: "araba",
#     1: "insan"
# }

# imagePaths = imageDosyalariGetir("dataset/images/train")

# for imagePath in imagePaths:
#     labelPath = labelPathBul(imagePath)

#     image = goruntuOku(imagePath)

#     if image is None:
#         continue

#     imageHeight, imageWidth = image.shape[:2]

#     annotations = yoloAnnotationOku(labelPath)

#     for classId, xCenter, yCenter, width, height in annotations:
#         x, y, w, h = yoloToPixelBox(
#             xCenter,
#             yCenter,
#             width,
#             height,
#             imageWidth,
#             imageHeight
#         )

#         label = classNames.get(classId, "Bilinmeyen")
#         image = kutuCiz(image, x, y, w, h, label, 1.00)

#     goruntuGoster(image, imagePath)

# ---------------------------------------------------------------------------------------------
    # yolo detect train model=yolov8n.pt data=data.yaml epochs=5 bunla direkt eğitime başlıyoruz
    # clı command line interface i var ultralytics / yolo framework için


# şimdi eğitilmiş modeli denicem

# image = goruntuOku("dataset/images/val/0000001_05499_d_0000010.jpg")

# if image is not None:
#     detections = yoloDetectionUret(image)

#     image = detectionCiz(image, detections)

#     goruntuGoster(image, "Fine-tuned YOLO Detection")

# ---------------------------------------------------------------------------------------------
# şimdi burda birden fazla val içinde kontolr edicez sonra da bunları output içine kaydedicez

# imagePaths = imageDosyalariGetir("dataset/images/val")

# for imagePath in imagePaths[:10]:
#     image = goruntuOku(imagePath)

#     if image is None:
#         continue

#     detections = yoloDetectionUret(image)
#     image = detectionCiz(image, detections)

#     goruntuGoster(image)

# ---------------------------------------------------------------------------------------------
# output a kaydetme kısmı burası

# outputFolder = "outputs"
# # exist_ok=True klasor varsa hata verme devam
# os.makedirs(outputFolder, exist_ok=True)

# imagePaths = imageDosyalariGetir("dataset/images/val")

# for imagePath in imagePaths[40:50]:
#     image = goruntuOku(imagePath)

#     if image is None:
#         continue

#     detections = yoloDetectionUret(image)
#     image = detectionCiz(image, detections)
#     # burası en sağdaki adı alır resim.jpg gibi
#     fileName = os.path.basename(imagePath)
#     savePath = os.path.join(outputFolder, fileName)

#     goruntuKaydet(image, savePath)

# print("Tahmin sonuclari outputs klasorune kaydedildi.")

# ---------------------------------------------------------------------------------------------
#  burda real time kamera ile gözlem yapıyoruz

# kameraIleRealTimeDetection()

#  tekrar train için
#  yolo detect train model=runs/detect/visdroneYolov8n50/weights/best.pt data=data.yaml epochs=30 imgsz=640 batch=8 name=visdroneYolov8n50-2
# ---------------------------------------------------------------------------------------------
#  burda da video ile detection deniyoruz


videoIleDetection("video.mp4")