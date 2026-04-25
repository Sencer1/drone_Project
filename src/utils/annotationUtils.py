import os
# burdaki maamç daha sonra dönüşümü kullanabilmek için yolo formatını kendi x y w h formatımıza çevirmek
# yolo değerler değil oran tutuluyor kutu merkezi resimin boyutu 0-1 arası değer alıyor
def yoloToPixelBox(xCenter, yCenter, width, height, imageWidth, imageHeight):
    kutuMerkezX = xCenter * imageWidth
    kutuMerkezY = yCenter * imageHeight
    kutuGenisligi = width * imageWidth
    kutuYuksekligi = height * imageHeight

    #  sol üst köşeyi aldık burda 
    x = int(kutuMerkezX -  kutuGenisligi / 2)
    y = int(kutuMerkezY - kutuYuksekligi / 2)
    w = int(kutuGenisligi)
    h = int(kutuYuksekligi)

    return x, y, w, h

#  burası yolo label txt dosyasından okuyup pyhton lsitesine çevirmek için
#  bu dosayda her satır 1 nesen oluyor ama hepsini normalize edilmiş halde
def yoloAnnotationOku(labelPath):
    annotations = []
# dosayyı açtık sadece read işlemi için file objesi olarak
# with ile de işimiz bitince kapattık
    with open(labelPath, "r") as file:
        for line in file:
            # satır sonundaki gereksiz karakterleri siler strip /n gibi
            #  split de boşluklardan böler liste döner
            parcalar = line.strip().split()

            if len(parcalar) != 5:
                continue

            classId = int(parcalar[0])
            xCenter = float(parcalar[1])
            yCenter = float(parcalar[2])
            width = float(parcalar[3])
            height = float(parcalar[4])

            annotations.append((classId, xCenter, yCenter, width, height))

    return annotations
#  burası image e karşılık gelen dosya adını bulmka için

def labelPathBul(imagePath):
    # # tam yolun sadece dosya adını vermek için burası
    # dosyaAdi = os.path.basename(imagePath)
    # # dosya adını iki parçaya bölmek için
    # # _ buraya .jpg atadık ama onu kullanmıcaz
    # kokAd, _ = os.path.splitext(dosyaAdi)
    # # sonra da label yolunu oluşturuyoruz
    # labelPath = os.path.join("dataset", "labels", kokAd + ".txt")

    labelPath = imagePath.replace("images", "labels")
    # stringi sağ baştan başlayarak böler rsplit
    # dasdafa/asfafa/image.jpg yi [apfkapfap/aıfıafmwa/iamge, jpg] şeklinde ayırdı 1 kez
    # [0] ile de ilk kısmı alıp sonuna txt ekledik
    labelPath = labelPath.rsplit(".",1)[0] + ".txt"

    return labelPath




def imageDosyalariGetir(imagesFolder):
    dosyalar = []
    # verilen klasördeki dosya isimlerini döndürür os.listdir
    for dosyaAdi in os.listdir(imagesFolder):
        # string in sonunu kontrol ediyor
        if dosyaAdi.endswith(".jpg") or dosyaAdi.endswith(".png"):
            # dosydakiler ie isimleri birleştiriyor
            tamYol = os.path.join(imagesFolder, dosyaAdi)
            dosyalar.append(tamYol)

    return sorted(dosyalar)