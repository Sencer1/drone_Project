import cv2


def goruntuOku(dosyaYolu):
    image = cv2.imread(dosyaYolu)

    if image is None:
        print("Goruntu yuklenmedi")
        return None
    
    return image



def goruntuGoster(image, pencereAdi="Goruntu"):
    cv2.imshow(pencereAdi, image)
    #  ekrana pencere açar ve resmi koyar
    cv2.waitKey(0)
    #  klavyeden input bekler 0 sonsuz demek
    #  tuşa basana kadar pencere açık
    cv2.destroyAllWindows()
    #  opencv nin açtığı tüm pencereleri kapatır 