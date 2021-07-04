import cv2
from ShapeDetector import ShapeDetector
from BinaryImage import BinaryImage


class ImageAnalyzer:
    def __init__(self):
        self.shape_detector = ShapeDetector()

    def analyze(self, image: BinaryImage):
        all_contours = image.get_all_contours()
        pixels_copy = image.pixels
        for contours in all_contours:
            moments = cv2.moments(contours)
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
            shape_name = self.shape_detector.detect(contours)
            cv2.drawContours(pixels_copy, [contours], -1, (0, 255, 0), 2)
            cv2.putText(pixels_copy, shape_name, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)

            cv2.imshow("Image", pixels_copy)
            cv2.waitKey(0)
