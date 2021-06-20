import numpy as np
from PIL import Image, ImageOps
import cv2
from matplotlib import pyplot as plot


def get_pixels_from_pil_image(image):
    black_and_white_image = image.convert('L')
    black_and_white_pixels = np.asarray(black_and_white_image).astype(np.int)
    return black_and_white_pixels


class BinaryImage:
    def __init__(self, image_file_path=None, pixels=None):
        if image_file_path and pixels:
            raise Exception("Both image_file_path and pixels passed to constructor")

        if image_file_path is not None:
            self.pixels = cv2.cvtColor(cv2.imread(image_file_path), cv2.COLOR_BGR2GRAY)
            self.pixels = cv2.threshold(self.pixels, 127, 255, cv2.THRESH_BINARY)[1]
            self.pixels = (255 - self.pixels)
            self.pixels = self.pixels/255
            self.pil_image = Image.fromarray(self.pixels)

        if pixels is not None:
            self.pil_image = Image.fromarray(pixels)
            self.pixels = pixels

        pixels_x, pixels_y = self.pixels.shape
        self.number_of_pixels = pixels_x * pixels_y

    def get_horizontal_mirror(self):
        return BinaryImage(pixels=get_pixels_from_pil_image(ImageOps.mirror(self.pil_image)))

    def get_vertical_mirror(self):
        return BinaryImage(pixels=get_pixels_from_pil_image(ImageOps.flip(self.pil_image)))

    def get_similarity_score(self, other):
        equality_matrix = np.equal(self.pixels, other.pixels).astype(int)
        return np.mean(equality_matrix)

    def show(self):
        pixels = (self.pixels * 255).astype(np.uint8)
        tmp_image = Image.fromarray(pixels)
        tmp_image.show()

    def save_to_file(self, file_path):
        self.pil_image.save(file_path)

    def get_black_and_white_ratio(self):
        number_of_white_pixels = np.count_nonzero(self.pixels)
        number_of_black_pixels = self.number_of_pixels - number_of_white_pixels
        return number_of_black_pixels / float(self.number_of_pixels)

    def get_contours(self):
        contours, hierarchy = cv2.findContours(self.pixels, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contours

    def show_image_with_contours(self):
        contours = self.get_contours()
        image = cv2.drawContours(self.pixels, contours, -1, (255, 0, 0), 2)
        plot.imshow(image)
        plot.show()

    def __eq__(self, other):
        return np.array_equal(self.pixels, other.pixels)

    def __sub__(self, other):
        x = np.subtract(self.pixels, other.pixels)
        return BinaryImage(pixels=np.abs(x))
