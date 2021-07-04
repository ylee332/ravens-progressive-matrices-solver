import cv2


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, contour):
        shape_name = "unidentified"
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        if len(approx) == 3:
            shape_name = "triangle"
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape_name = "square" if 0.95 <= ar <= 1.05 else "rectangle"
        elif len(approx) == 5:
            shape_name = "pentagon"
        else:
            shape_name = "circle"
        return shape_name
