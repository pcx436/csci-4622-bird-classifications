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
def read_bounding_boxes(filename):
    boxes = list()
    with open(filename, 'r') as boxes_file:
        for line in boxes_file:
            line_split = line.strip().split(' ')[1:]  # remove the index at the beginning of the line

            converted_tuple = tuple([float(param) for param in line_split])  # convert coords to float, place in tuple
            boxes.append(converted_tuple)

    return boxes


# convert bounding box system to cartesian coordinate system
def convert_cartesian(current_box):
    left = current_box[0]
    upper = current_box[1]
    right = current_box[0] + current_box[2]
    lower = current_box[1] + current_box[3]

    return left, upper, right, lower


def draw_bounding(image, box):
    draw = ImageDraw.Draw(image)
    draw.rectangle(convert_cartesian(box), outline='white')

    return image


# crop an image to its bounding box
def crop_by_box(image, current_box):
    crop_box = convert_cartesian(current_box)
    cropped_image = image.crop(crop_box)
    return cropped_image


def main():
    images_directory = 'CUB_200_2011/images/'

    id_list = build_id_list('CUB_200_2011/images.txt')
    boxes = read_bounding_boxes('CUB_200_2011/bounding_boxes.txt')

    # First image in the first category
    test_image_path = images_directory + id_list[0]

    test_image = Image.open(test_image_path)

    print('Test image dimensions: {}px width, {}px height'.format(test_image.width, test_image.height))
    print('Test image bounding box:', boxes[0])
    print('Bounding box dimensions: {}px width, {}px height'.format(boxes[0][2], boxes[0][3]))

    # resizing dimensions of bounding box as necessary
    current_box = boxes[0]
    cartesian_box = convert_cartesian(current_box)
    image_dimensions = test_image.size
    (box_width, box_height) = current_box[2:]

    if box_width != box_height:
        # box dimensions must change
        growth = abs(box_width - box_height) / 2.0
        dimension = 0 if box_width < box_height else 1

        # calculate the amount of px needed to grow in either direction
        negative_growth = cartesian_box[dimension] - growth
        negative_growth_debt = abs(negative_growth) if negative_growth < 0 else 0

        positive_growth = (cartesian_box[dimension + 2] + growth) - image_dimensions[dimension]
        positive_growth_debt = abs(positive_growth) if positive_growth > 0 else 0


    # going to try drawing the bounding box
    # bounded_image = draw_bounding(test_image, boxes[0])

    # attempt to crop image
    # cropped_image = crop_by_box(test_image, boxes[0])
    # cropped_image.show()


if __name__ == '__main__':
    main()
