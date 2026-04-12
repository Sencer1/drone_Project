import cv2

def kutuCiz(image, x, y, w, h, label="Object", confidence=None):
    # dikdörtgen çizimi

    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if confidence is not None:
        yazi = f"{label} {confidence:.2f}"
    else:
        yazi = label

    cv2.putText(
        image,
        yazi,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    return image