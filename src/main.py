from utils.imageUtils import goruntuOku, goruntuGoster
from utils.drawUtils import kutuCiz
from utils.boxUtils import iouHesapla

image = goruntuOku("indir.jpg")

if image is not None:
    # x = 100
    # y = 100
    # w = 200
    # h = 150
    
    # image = kutuCiz(image, x, y, w, h, "kara delik")
    
    detections = [
        (10, 10, 20, 15, "Arac", 0.92),
        (35, 12, 12, 18, "Insan", 0.81),
        (50, 30, 18, 12, "Arac", 0.76)
    ]
    for x, y, w, h, label, confidence in detections:
        image = kutuCiz(image, x, y, w, h, label, confidence)

    goruntuGoster(image)

    

box1 = (100, 100, 200, 150)
box2 = (110, 110, 195, 145)

iou = iouHesapla(box1, box2)

print("IoU:", iou)

# # nms non max suppression
# bunla üst üste gelen aynı kutuları ayırt ediyoruz 
# # aynı objeyi farklı kutular göstermiyor
# iou intersection over union bunu hesaplayıp aynı mı ayrı kutular mı ona bakıcaz

