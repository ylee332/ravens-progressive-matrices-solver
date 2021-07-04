import numpy as np
from PIL import Image, ImageOps
import cv2


def get_pixels_from_pil_image(image):
    black_and_white_image = image.convert('L')
    black_and_white_pixels = np.asarray(black_and_white_image).astype(np.uint8)
    return black_and_white_pixels


class BinaryImage:
    def __init__(self, name, image_file_path=None, pixels=None):
        if image_file_path and pixels:
            raise Exception("Both image_file_path and pixels passed to constructor")

        if image_file_path is not None:
            # TODO: delete original image
            self.original_image = cv2.imread(image_file_path)
            self.pixels = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.pixels = cv2.threshold(self.pixels, 127, 255, cv2.THRESH_BINARY)[1]
            self.pixels = (255 - self.pixels)

        if pixels is not None:
            self.pixels = pixels

        self.pil_image = Image.fromarray(np.asarray(self.pixels).astype(np.uint8))
        pixels_x, pixels_y = self.pixels.shape
        self.number_of_pixels = pixels_x * pixels_y
        self.name = name

    def get_horizontal_mirror(self):
        return BinaryImage(name=f"{self.name} horizontal mirror",
                           pixels=get_pixels_from_pil_image(ImageOps.mirror(self.pil_image)))

    def get_vertical_mirror(self):
        return BinaryImage(name=f"{self.name} vertical mirror",
                           pixels=get_pixels_from_pil_image(ImageOps.flip(self.pil_image)))

    def get_rotation(self):
        return BinaryImage(name=f"{self.name} rotated by 270 degrees",
                           pixels=get_pixels_from_pil_image(Image.Image.rotate(self.pil_image, 270)))

    def get_similarity_score(self, other):
        equality_matrix = np.equal(self.pixels, other.pixels).astype(int)
        return np.mean(equality_matrix)

    def show(self):
        image = Image.fromarray(self.pixels)
        image.show()

    def save_to_file(self, file_path):
        self.pil_image.save(file_path)

    def get_black_and_white_ratio(self):
        number_of_white_pixels = np.count_nonzero(self.pixels)
        number_of_black_pixels = self.number_of_pixels - number_of_white_pixels
        return number_of_black_pixels / float(self.number_of_pixels)

    def get_all_contours(self):
        contours, hierarchy = cv2.findContours(image=self.pixels, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        return contours

    def get_outer_contours_filled(self):
        all_contours = self.get_all_contours()
        outer_contours = max(all_contours, key=cv2.contourArea)
        filled = np.zeros(self.pixels.shape, dtype="uint8")
        cv2.drawContours(filled, [outer_contours], -1, 255, -1)
        return BinaryImage(name=f"{self.name} with filled outer contours", pixels=filled)

    def show_image_with_contours(self):
        outer_contours = self.get_all_contours()
        image_copy = self.original_image
        cv2.drawContours(image=image_copy, contours=outer_contours, contourIdx=-1, color=(0, 0, 255), thickness=1,
                         lineType=cv2.LINE_AA)
        cv2.imshow('None approximation', image_copy)
        cv2.waitKey(0)

    def count_not_nested_objects(self):
        all_contours = self.get_all_contours()
        return len(all_contours)

    def get_black_pixels(self):
        width, height = self.pixels.shape
        black_pixels = []
        for col in range(width):
            for row in range(height):
                pixel = self.pixels[col, row]
                if pixel == 255:
                    black_pixels.append((col, row))
        return black_pixels

    def get_min_max_x_coordinates(self):
        black_pixels = self.get_black_pixels()
        min_x = 200
        max_x = -1

        for x, _ in black_pixels:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x

        return min_x, max_x

    def get_min_max_y_coordinates(self):
        black_pixels = self.get_black_pixels()
        min_y = 200
        max_y = -1

        for _, y in black_pixels:
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        return min_y, max_y

    def __eq__(self, other):
        return np.array_equal(self.pixels, other.pixels)

    def __sub__(self, other):
        return BinaryImage(name=f"{self.name} - {other.name}", pixels=cv2.absdiff(self.pixels, other.pixels))
