from PIL import Image, ImageDraw


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


def draw_bounding(image, box):
    start_cord = tuple(box[0:2])
    end_cord = (start_cord[0] + box[2], start_cord[1] + box[3])

    draw = ImageDraw.Draw(image)
    draw.rectangle([start_cord, end_cord], outline='white')

    return image


# convert bounding box system to cartesian coordinate system
def convert_cartesian(current_box):
    left = current_box[0]
    upper = current_box[1]
    right = current_box[0] + current_box[2]
    lower = current_box[1] + current_box[3]

    return left, upper, right, lower


def main():
    images_directory = 'CUB_200_2011/images/'

    id_list = build_id_list('CUB_200_2011/images.txt')
    boxes = bounding_boxes('CUB_200_2011/bounding_boxes.txt')

    # First image in the first category
    test_image_path = images_directory + id_list[0]

    test_image = Image.open(test_image_path)

    print('Test image dimensions:', test_image.size)
    print('Test image bounding box:', boxes[0])

    # going to try drawing the bounding box
    # bounded_image = draw_bounding(test_image, boxes[0])



if __name__ == '__main__':
    main()
