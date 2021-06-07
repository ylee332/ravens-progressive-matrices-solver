import numpy as np
from PIL import Image, ImageOps


def get_pixels(image):
    black_and_white_image = image.convert('1')
    black_and_white_pixels = np.asarray(black_and_white_image).astype(np.int)
    return 1 - black_and_white_pixels


def get_absolute_difference_between_pixels(pixels_a, pixels_b):
    return np.abs(pixels_b - pixels_a)


def get_similarity_percentages(pixels_a, pixels_b):
    equality_matrix = np.equal(pixels_a, pixels_b).astype(int)
    return np.mean(equality_matrix)


def find_index_of_most_similar_pixels(pixels_to_check, possible_pixels_to_match: list, thresh=0.93):
    highest_similarity_percentage = 0.0
    index_of_highest_similarity = -1
    for index, element in enumerate(possible_pixels_to_match):
        similarity_percentage = get_similarity_percentages(pixels_to_check, element)
        if similarity_percentage < thresh:
            continue
        if similarity_percentage > highest_similarity_percentage:
            index_of_highest_similarity = index + 1
            highest_similarity_percentage = similarity_percentage
    return index_of_highest_similarity


def show_pixels(pixels):
    pixels = (pixels * 255).astype(np.uint8)
    image = Image.fromarray(pixels)
    image.show()


def save_pixels_to_file(pixels, file_path):
    pixels = (pixels * 255).astype(np.uint8)
    image = Image.fromarray(pixels)
    image.save(file_path)


class TwoDimensionalMatrixSolver:

    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        # if self.problem.name != "Basic Problem B-09":
        #     return -1
        figures = self.problem.figures

        image_a = Image.open(figures['A'].visualFilename)
        image_b = Image.open(figures['B'].visualFilename)
        image_c = Image.open(figures['C'].visualFilename)
        image1 = Image.open(figures['1'].visualFilename)
        image2 = Image.open(figures['2'].visualFilename)
        image3 = Image.open(figures['3'].visualFilename)
        image4 = Image.open(figures['4'].visualFilename)
        image5 = Image.open(figures['5'].visualFilename)
        image6 = Image.open(figures['6'].visualFilename)

        pixels_a = get_pixels(image_a)
        pixels_b = get_pixels(image_b)
        pixels_c = get_pixels(image_c)

        pixels1 = get_pixels(image1)
        pixels2 = get_pixels(image2)
        pixels3 = get_pixels(image3)
        pixels4 = get_pixels(image4)
        pixels5 = get_pixels(image5)
        pixels6 = get_pixels(image6)

        possible_solution_pixels = [pixels1, pixels2, pixels3, pixels4, pixels5, pixels6]

        if np.array_equal(pixels_a, pixels_b):
            pixels_d = pixels_c
            for index, element in enumerate(possible_solution_pixels):
                if np.array_equal(pixels_d, element):
                    return index + 1
        elif np.array_equal(pixels_a, pixels_c):
            pixels_d = pixels_b
            for index, element in enumerate(possible_solution_pixels):
                if np.array_equal(pixels_d, element):
                    return index + 1
        else:
            pixels_a_horizontal_mirror = get_pixels(ImageOps.mirror(image_a))
            if get_similarity_percentages(pixels_a_horizontal_mirror, pixels_b) > 0.98:
                pixels_c_horizontal_mirror = get_pixels(ImageOps.mirror(image_c))
                index = find_index_of_most_similar_pixels(pixels_c_horizontal_mirror, possible_solution_pixels)
                if index != -1:
                    return index

            if get_similarity_percentages(pixels_a_horizontal_mirror, pixels_c) > 0.97:
                pixels_b_horizontal_mirror = get_pixels(ImageOps.mirror(image_b))
                index = find_index_of_most_similar_pixels(pixels_b_horizontal_mirror, possible_solution_pixels)
                if index != -1:
                    return index

            pixels_a_vertical_mirror = get_pixels(ImageOps.flip(image_a))

            if get_similarity_percentages(pixels_a_vertical_mirror, pixels_b) > 0.98:
                pixels_c_vertical_mirror = get_pixels(ImageOps.flip(image_c))
                index = find_index_of_most_similar_pixels(pixels_c_vertical_mirror, possible_solution_pixels)
                if index != -1:
                    return index

            if get_similarity_percentages(pixels_a_vertical_mirror, pixels_c) > 0.98:
                pixels_b_vertical_mirror = get_pixels(ImageOps.flip(image_b))
                index = find_index_of_most_similar_pixels(pixels_b_vertical_mirror, possible_solution_pixels)
                if index != -1:
                    return index

            transform_ab = get_absolute_difference_between_pixels(pixels_a, pixels_b)
            transform_ac = get_absolute_difference_between_pixels(pixels_a, pixels_c)

            pixels_d1 = get_absolute_difference_between_pixels(transform_ab, pixels_c)
            pixels_d2 = get_absolute_difference_between_pixels(transform_ac, pixels_b)

            for index, element in enumerate(possible_solution_pixels):
                if np.array_equal(pixels_d1, element) or np.array_equal(
                        pixels_d2, element):
                    return index + 1

            index = find_index_of_most_similar_pixels(pixels_d1, possible_solution_pixels)
            if index != -1:
                # save_pixels_to_file(pixels_d1, r"C:\Users\micha\Desktop\rpm\ravens-progressive-matrix-solver\d1.png")
                return index

            index = find_index_of_most_similar_pixels(pixels_d2, possible_solution_pixels)
            if index != -1:
                return index
        return -1