import cv2


class ShapeDetector:

    def detect(self, contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        if len(approx) == 3:
            return "triangle"
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if 0.95 <= ar <= 1.05:
                return "square"
            else:
                return "rectangle"
        elif len(approx) == 5:
            return "pentagon"
        else:
            return "circle"
