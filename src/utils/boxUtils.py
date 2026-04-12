def iouHesapla(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # kutuların sağ-alt köşeleri
    box1X2 = x1 + w1
    box1Y2 = y1 + h1
    box2X2 = x2 + w2
    box2Y2 = y2 + h2

    # kesişim dikdörtgeni
    kesisimX1 = max(x1, x2)
    kesisimY1 = max(y1, y2)
    kesisimX2 = min(box1X2, box2X2)
    kesisimY2 = min(box1Y2, box2Y2)

    # kesişim genişlik / yükseklik
    kesisimGenislik = max(0, kesisimX2 - kesisimX1)
    kesisimYukseklik = max(0, kesisimY2 - kesisimY1)

    kesisimAlani = kesisimGenislik * kesisimYukseklik

    box1Alani = w1 * h1
    box2Alani = w2 * h2

    birlesimAlani = box1Alani + box2Alani - kesisimAlani

    if birlesimAlani == 0:
        return 0

    return kesisimAlani / birlesimAlani