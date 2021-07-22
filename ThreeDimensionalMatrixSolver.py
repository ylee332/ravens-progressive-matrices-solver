from BinaryImage import BinaryImage
from BinaryImageUtils import find_index_of_most_similar_pixels, find_indexes_of_images_with_same_objects_number
from ImageAnalyzer import ImageAnalyzer


class ThreeDimensionalMatrixSolver:

    def __init__(self, problem):
        self.problem = problem
        self.analyzer = ImageAnalyzer()

    def solve(self):
        # if self.problem.name != "Challenge Problem E-12":
        #     return -1
        figures = self.problem.figures

        image_a = BinaryImage(name='A', image_file_path=figures['A'].visualFilename)
        image_b = BinaryImage(name='B', image_file_path=figures['B'].visualFilename)
        image_c = BinaryImage(name='C', image_file_path=figures['C'].visualFilename)
        image_d = BinaryImage(name='D', image_file_path=figures['D'].visualFilename)
        image_e = BinaryImage(name='E', image_file_path=figures['E'].visualFilename)
        image_f = BinaryImage(name='F', image_file_path=figures['F'].visualFilename)
        image_g = BinaryImage(name='G', image_file_path=figures['G'].visualFilename)
        image_h = BinaryImage(name='H', image_file_path=figures['H'].visualFilename)
        image1 = BinaryImage(name='1', image_file_path=figures['1'].visualFilename)
        image2 = BinaryImage(name='2', image_file_path=figures['2'].visualFilename)
        image3 = BinaryImage(name='3', image_file_path=figures['3'].visualFilename)
        image4 = BinaryImage(name='4', image_file_path=figures['4'].visualFilename)
        image5 = BinaryImage(name='5', image_file_path=figures['5'].visualFilename)
        image6 = BinaryImage(name='6', image_file_path=figures['6'].visualFilename)
        image7 = BinaryImage(name='7', image_file_path=figures['7'].visualFilename)
        image8 = BinaryImage(name='8', image_file_path=figures['8'].visualFilename)

        possible_solutions_images = [image1, image2, image3, image4, image5, image6, image7, image8]

        image_a_shape = self.analyzer.analyze(image_a)
        image_b_shape = self.analyzer.analyze(image_b)
        image_c_shape = self.analyzer.analyze(image_c)
        number_of_black_pixels_in_image_a = image_a.get_number_of_black_pixels()
        number_of_black_pixels_in_image_b = image_b.get_number_of_black_pixels()
        number_of_black_pixels_in_image_c = image_c.get_number_of_black_pixels()

        if image_a_shape == image_b_shape == image_c_shape and \
                number_of_black_pixels_in_image_a == number_of_black_pixels_in_image_b == number_of_black_pixels_in_image_c:
            image_h_shape = self.analyzer.analyze(image_h)
            number_of_pixels_in_image_h = image_h.get_number_of_black_pixels()
            for index, element in enumerate(possible_solutions_images):
                if image_h_shape == self.analyzer.analyze(
                        element) and number_of_pixels_in_image_h == element.get_number_of_black_pixels():
                    return index + 1

        if image_a == image_b or image_a == image_c:
            image_i = image_h
            for index, element in enumerate(possible_solutions_images):
                if image_i == element:
                    return index + 1
            image_i = image_g
            for index, element in enumerate(possible_solutions_images):
                if image_i == element:
                    return index + 1
        elif image_a == image_d or image_a == image_g:
            image_i = image_c
            for index, element in enumerate(possible_solutions_images):
                if image_i == element:
                    return index + 1
            image_i = image_f
            for index, element in enumerate(possible_solutions_images):
                if image_i == element:
                    return index + 1

        image_a_with_b = image_a + image_b
        number_of_black_pixels_in_image_ab = image_a_with_b.get_number_of_black_pixels()
        if abs(number_of_black_pixels_in_image_ab - number_of_black_pixels_in_image_c) < 80 and \
                self.analyzer.analyze(image_a_with_b) == self.analyzer.analyze(image_c):
            image_i = image_g + image_h
            number_of_pixels_in_image_i = image_i.get_number_of_black_pixels()
            for index, element in enumerate(possible_solutions_images):
                a = element.get_number_of_black_pixels()
                if abs(number_of_pixels_in_image_i - a) < 80:
                    return index + 1

        number_of_objects_in_image_a = image_a.count_not_nested_objects()
        number_of_objects_in_image_b = image_b.count_not_nested_objects()
        number_of_objects_in_image_c = image_c.count_not_nested_objects()
        if number_of_objects_in_image_b - number_of_objects_in_image_a == number_of_objects_in_image_c - number_of_objects_in_image_b:
            number_of_objects_in_image_g = image_g.count_not_nested_objects()
            number_of_objects_in_image_h = image_h.count_not_nested_objects()
            number_of_objects_in_third_row_delta = number_of_objects_in_image_h - number_of_objects_in_image_g

            if number_of_objects_in_third_row_delta >= 1 or number_of_objects_in_third_row_delta < 0:
                number_of_objects_in_possible_solution = number_of_objects_in_image_h + number_of_objects_in_third_row_delta
                indexes_of_images_with_same_objects_number = find_indexes_of_images_with_same_objects_number(
                    number_of_objects_in_possible_solution,
                    possible_solutions_images)
                if len(indexes_of_images_with_same_objects_number) > 0:
                    min_x_black_in_image_g, max_x_black_in_image_g = image_g.get_min_max_x_coordinates()
                    min_y_black_in_image_g, max_y_black_in_image_g = image_g.get_min_max_y_coordinates()

                    for index in indexes_of_images_with_same_objects_number:
                        element = possible_solutions_images[index]
                        min_x, max_x = element.get_min_max_x_coordinates()
                        min_y, max_y = element.get_min_max_y_coordinates()

                        x_ok = (2 >= abs(min_x - min_x_black_in_image_g) >= 0 and (2 >= abs(
                            max_x - max_x_black_in_image_g) >= 0))
                        y_ok = (2 >= abs(min_y - min_y_black_in_image_g) >= 0 and (2 >= abs(
                            max_y - max_y_black_in_image_g) >= 0))
                        if x_ok or y_ok:
                            return index + 1
                    return indexes_of_images_with_same_objects_number[0] + 1

        image_a_vertical_mirror = image_a.get_vertical_mirror()
        if image_a_vertical_mirror.get_similarity_score(image_g) > 0.98:
            image_c_vertical_mirror = image_c.get_vertical_mirror()
            index = find_index_of_most_similar_pixels(image_c_vertical_mirror, possible_solutions_images)
            if index != -1:
                return index

        image_a_horizontal_mirror = image_a.get_horizontal_mirror()
        if image_a_horizontal_mirror.get_similarity_score(image_c) > 0.98:
            image_g_horizontal_mirror = image_g.get_horizontal_mirror()
            index = find_index_of_most_similar_pixels(image_g_horizontal_mirror, possible_solutions_images)
            if index != -1:
                return index

        number_of_black_pixels_in_row = number_of_black_pixels_in_image_a + number_of_black_pixels_in_image_b + number_of_black_pixels_in_image_c

        number_of_black_pixels_in_image_g = image_g.get_number_of_black_pixels()
        number_of_black_pixels_in_image_h = image_h.get_number_of_black_pixels()
        target_number_of_pixels_in_image_i = number_of_black_pixels_in_row - number_of_black_pixels_in_image_g - number_of_black_pixels_in_image_h

        # adding black pixels
        sum_of_number_of_black_pixels_in_ab = image_a.get_number_of_black_pixels() + image_b.get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_ab - number_of_black_pixels_in_image_c) < 80:
            for index, element in enumerate(possible_solutions_images):
                target_black_pixels = number_of_black_pixels_in_image_g + number_of_black_pixels_in_image_h
                if abs(element.get_number_of_black_pixels() - target_black_pixels) < 80:
                    return index + 1

        sum_of_number_of_black_pixels_in_bc = image_b.get_number_of_black_pixels() + image_c.get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_bc - number_of_black_pixels_in_image_a) < 80:
            for index, element in enumerate(possible_solutions_images):
                target_black_pixels = number_of_black_pixels_in_image_g - number_of_black_pixels_in_image_h

                if abs(element.get_number_of_black_pixels() - target_black_pixels) < 80:
                    return index + 1

        sum_of_number_of_black_pixels_in_ac = image_a.get_number_of_black_pixels() + image_c.get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_ac - number_of_black_pixels_in_image_b) < 80:
            for index, element in enumerate(possible_solutions_images):
                target_black_pixels = number_of_black_pixels_in_image_h - number_of_black_pixels_in_image_g
                if abs(element.get_number_of_black_pixels() - target_black_pixels) < 80:
                    return index + 1

        # adding images

        sum_of_number_of_black_pixels_in_ab2 = (image_a + image_b).get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_ab2 - number_of_black_pixels_in_image_c) < 30:
            gh_plus = (image_h - image_g)
            index = find_index_of_most_similar_pixels(gh_plus, possible_solutions_images)
            if index != -1:
                return index

        sum_of_number_of_black_pixels_in_bc2 = (image_b + image_c).get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_bc2 - number_of_black_pixels_in_image_a) < 30:
            gh_minus = (image_h - image_g)
            index = find_index_of_most_similar_pixels(gh_minus, possible_solutions_images)
            if index != -1:
                return index

        sum_of_number_of_black_pixels_in_ac2 = (image_a + image_c).get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_ac2 - number_of_black_pixels_in_image_b) < 30:
            hg_minus = (image_h - image_g)
            index = find_index_of_most_similar_pixels(hg_minus, possible_solutions_images)
            if index != -1:
                return index

        diff1 = number_of_black_pixels_in_image_b - number_of_black_pixels_in_image_a
        diff2 = number_of_black_pixels_in_image_c - number_of_black_pixels_in_image_b
        if abs(diff1 - diff2) < 50:
            target_black_pixels = number_of_black_pixels_in_image_h + diff2
            for index, element in enumerate(possible_solutions_images):
                if abs(element.get_number_of_black_pixels() - target_black_pixels) < 80:
                    return index + 1

        # diff1 = number_of_black_pixels_in_image_a - number_of_black_pixels_in_image_b
        # diff2 = number_of_black_pixels_in_image_b - number_of_black_pixels_in_image_c
        # if abs(diff1 - diff2) < 50:
        #     target_black_pixels = number_of_black_pixels_in_image_h - diff2
        #     for index, element in enumerate(possible_solutions_images):
        #         if abs(element.get_number_of_black_pixels() - target_black_pixels) < 80:
        #             return index + 1

        # xor
        sum_of_number_of_black_pixels_in_xor_ab2 = (image_a.xor_operation(image_b)).get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_xor_ab2 - number_of_black_pixels_in_image_c) < 250:
            hg_xor = image_h.xor_operation(image_g)
            index = find_index_of_most_similar_pixels(hg_xor, possible_solutions_images)
            if index != -1:
                return index

        # and
        sum_of_number_of_black_pixels_in_and_ab2 = (image_a.and_operation(image_b)).get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_and_ab2 - number_of_black_pixels_in_image_c) < 250:
            hg_and = image_h.and_operation(image_g)
            index = find_index_of_most_similar_pixels(hg_and, possible_solutions_images)
            if index != -1:
                return index

        # or
        sum_of_number_of_black_pixels_in_or_ab2 = (image_a.or_operation(image_b)).get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_or_ab2 - number_of_black_pixels_in_image_c) < 250:
            hg_or = image_h.or_operation(image_g)
            index = find_index_of_most_similar_pixels(hg_or, possible_solutions_images)
            if index != -1:
                return index

        # not
        sum_of_number_of_black_pixels_in_not_ab2 = (image_a.not_operation(image_b)).get_number_of_black_pixels()
        if abs(sum_of_number_of_black_pixels_in_not_ab2 - number_of_black_pixels_in_image_c) < 250:
            hg_not = image_h.not_operation(image_g)
            index = find_index_of_most_similar_pixels(hg_not, possible_solutions_images)
            if index != -1:
                return index

        for index, element in enumerate(possible_solutions_images):
            if abs(target_number_of_pixels_in_image_i - element.get_number_of_black_pixels()) < 100:
                return index + 1

        return -1
