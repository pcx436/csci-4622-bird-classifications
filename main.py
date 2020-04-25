from PIL import Image

# NOTE: All of the ids are 1 indexed in the 'images.txt' file, keep this in mind
def build_id_list(filename):
    id_list = list()

    with open(filename, 'r') as library_file:
        for line in library_file:
            line_split = line.strip().split(' ')

            id_list.append(line_split[1])  # add the name of the file to the list

    return id_list


# reads in the bounding boxes
def bounding_boxes(filename):
    boxes = list()
    with open(filename, 'r') as boxes_file:
        for line in boxes_file:
            line_split = line.strip().split(' ')[1:]  # remove the index at the beginning of the line

            converted_tuple = tuple([float(param) for param in line_split])  # convert coords to float, place in tuple
            boxes.append(converted_tuple)

    return boxes


def main():
    images_directory = 'CUB_200_2011/images/'

    id_list = build_id_list('CUB_200_2011/images.txt')
    boxes = bounding_boxes('CUB_200_2011/bounding_boxes.txt')

    # First image in the first category
    test_image_path = images_directory + id_list[0]

    test_image = Image.open(test_image_path)

    print('Test image dimensions:', test_image.size)
    print('Test image bounding box:', boxes[0])


if __name__ == '__main__':
    main()
