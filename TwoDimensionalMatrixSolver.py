from BinaryImage import BinaryImage
from BinaryImageUtils import find_index_of_most_similar_pixels


class TwoDimensionalMatrixSolver:

    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        figures = self.problem.figures

        image_a = BinaryImage(name='A', image_file_path=figures['A'].visualFilename)
        image_b = BinaryImage(name='B', image_file_path=figures['B'].visualFilename)
        image_c = BinaryImage(name='C', image_file_path=figures['C'].visualFilename)
        image1 = BinaryImage(name='1', image_file_path=figures['1'].visualFilename)
        image2 = BinaryImage(name='2', image_file_path=figures['2'].visualFilename)
        image3 = BinaryImage(name='3', image_file_path=figures['3'].visualFilename)
        image4 = BinaryImage(name='4', image_file_path=figures['4'].visualFilename)
        image5 = BinaryImage(name='5', image_file_path=figures['5'].visualFilename)
        image6 = BinaryImage(name='6', image_file_path=figures['6'].visualFilename)

        possible_solutions_images = [image1, image2, image3, image4, image5, image6]

        if image_a == image_b:
            image_d = image_c
            for index, element in enumerate(possible_solutions_images):
                if image_d == element:
                    return index + 1
        elif image_a == image_c:
            image_d = image_b
            for index, element in enumerate(possible_solutions_images):
                if image_d == element:
                    return index + 1

        image_a_horizontal_mirror = image_a.get_horizontal_mirror()
        if image_a_horizontal_mirror.get_similarity_score(image_b) > 0.98:
            image_c_horizontal_mirror = image_c.get_horizontal_mirror()
            index = find_index_of_most_similar_pixels(image_c_horizontal_mirror, possible_solutions_images)
            if index != -1:
                return index

        if image_a_horizontal_mirror.get_similarity_score(image_c) > 0.97:
            image_b_horizontal_mirror = image_b.get_horizontal_mirror()
            index = find_index_of_most_similar_pixels(image_b_horizontal_mirror, possible_solutions_images)
            if index != -1:
                return index

        image_a_vertical_mirror = image_a.get_vertical_mirror()

        if image_a_vertical_mirror.get_similarity_score(image_b) > 0.98:
            image_c_vertical_mirror = image_c.get_vertical_mirror()
            index = find_index_of_most_similar_pixels(image_c_vertical_mirror, possible_solutions_images)
            if index != -1:
                return index

        if image_a_vertical_mirror.get_similarity_score(image_c) > 0.98:
            image_b_vertical_mirror = image_b.get_vertical_mirror()
            index = find_index_of_most_similar_pixels(image_b_vertical_mirror, possible_solutions_images)
            if index != -1:
                return index

        image_a_with_filled_outer_contours = image_a.get_outer_contours_filled()

        if image_a_with_filled_outer_contours.get_similarity_score(image_b) > 0.95:
            image_c_with_filled_outer_contours = image_c.get_outer_contours_filled()
            index = find_index_of_most_similar_pixels(image_c_with_filled_outer_contours, possible_solutions_images)
            if index != -1:
                return index

        image_a_rotated_by_270_degrees = image_a.get_rotation()
        if image_a_rotated_by_270_degrees.get_similarity_score(image_b) > 0.96:
            image_c_rotated_by_270_degrees = image_c.get_rotation()
            index = find_index_of_most_similar_pixels(image_c_rotated_by_270_degrees, possible_solutions_images)
            if index != -1:
                return index

        transform_ab = image_b - image_a
        transform_ac = image_c - image_a

        image_d1 = image_c - transform_ab
        image_d2 = image_b - transform_ac

        for index, element in enumerate(possible_solutions_images):
            if image_d1 == element or image_d2 == element:
                return index + 1

        index = find_index_of_most_similar_pixels(image_d1, possible_solutions_images)
        if index != -1:
            return index

        index = find_index_of_most_similar_pixels(image_d2, possible_solutions_images)
        if index != -1:
            return index
        return -1
