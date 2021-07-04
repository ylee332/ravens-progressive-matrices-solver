from BinaryImage import BinaryImage


def find_index_of_most_similar_pixels(image_to_check: BinaryImage, possible_images_to_match: list,
                                      thresh=0.93):
    highest_similarity_score = 0.0
    index_of_highest_similarity = -1
    for index, element in enumerate(possible_images_to_match):
        similarity_score = image_to_check.get_similarity_score(element)
        if similarity_score < thresh:
            continue
        if similarity_score > highest_similarity_score:
            index_of_highest_similarity = index + 1
            highest_similarity_score = similarity_score
    return index_of_highest_similarity


def find_indexes_of_images_with_same_objects_number(target_number_of_objects: int,
                                                    possible_images_to_match: list) -> list:
    indexes_of_images_with_same_objects_number = []
    for index, element in enumerate(possible_images_to_match):
        number_of_objects = element.count_not_nested_objects()
        if number_of_objects == target_number_of_objects:
            indexes_of_images_with_same_objects_number.append(index)
    return indexes_of_images_with_same_objects_number
