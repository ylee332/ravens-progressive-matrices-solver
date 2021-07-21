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
            return shape_name
