from utils.imageUtils import goruntuOku, goruntuGoster
from utils.drawUtils import kutuCiz
from utils.boxUtils import iouHesapla
from utils.boxUtils import nmsUygula
from detectionPipeline import nmsUygulaWrapper, detectionCiz
from detectionPipeline import yoloDetectionUret
from utils.annotationUtils import yoloToPixelBox, yoloAnnotationOku
from utils.annotationUtils import labelPathBul

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

# if image is not None:
#     detections = yoloDetectionUret(image)

#     nmsOncesi = detectionCiz(image.copy(), detections)
#     goruntuGoster(nmsOncesi, "NMS oncesi")

#     temizDetections = nmsUygulaWrapper(detections)

#     nmsSonrasi = detectionCiz(image.copy(), temizDetections)
#     goruntuGoster(nmsSonrasi, "NMS sonrasi")

    # yolo tabanlı computer vision modellerini kullanmak için
    # pip install ultralytics


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


classNames = {
    0: "araba",
    1: "insan"
}

imagePath = "datasets/images/indir.jpg"
labelPath = labelPathBul(imagePath)

image = goruntuOku(imagePath)

if image is not None:
    imageHeight, imageWidth = image.shape[:2]

    annotations = yoloAnnotationOku(labelPath)

    for classId, xCenter, yCenter, width, height in annotations:
        x, y, w, h = yoloToPixelBox(
            xCenter,
            yCenter,
            width,
            height,
            imageWidth,
            imageHeight
        )

        label = classNames.get(classId, "bilinmeyen")
        image = kutuCiz(image, x, y, w, h, label, 1.00)

    goruntuGoster(image)