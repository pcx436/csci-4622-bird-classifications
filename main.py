from PIL import Image, ImageDraw
from warnings import warn
import argparse


# NOTE: All of the ids are 1 indexed in the 'images.txt' file, keep this in mind
def build_id_list(filename):
    id_list = list()

    with open(filename, 'r') as library_file:
        for line in library_file:
            line_split = line.strip().split(' ')
            # add the name of the file to the list
            id_list.append(line_split[1])  

    return id_list


# reads in the bounding boxes
def read_bounding_boxes(filename):
    boxes = list()
    with open(filename, 'r') as boxes_file:
        for line in boxes_file:
            # remove the index at the beginning of the line
            line_split = line.strip().split(' ')[1:]  
            # convert coords to float, place in list
            converted_tuple = [float(param) for param in line_split]  
            boxes.append(converted_tuple)

    return boxes


# convert bounding box system to cartesian coordinate system
def convert_cartesian(current_box):
    left = current_box[0]
    upper = current_box[1]
    right = current_box[0] + current_box[2]
    lower = current_box[1] + current_box[3]

    return left, upper, right, lower


def draw_bounding(image, box, color='white'):
    draw = ImageDraw.Draw(image)
    draw.rectangle(convert_cartesian(box), outline=color)

    return image


# crop an image to its bounding box
def crop_by_box(image, current_box):
    crop_box = convert_cartesian(current_box)
    cropped_image = image.crop(crop_box)
    return cropped_image


def resize_bounding(image_dimensions, current_box):
    # resizing dimensions of bounding box as necessary
    (box_width, box_height) = current_box[2:]

    # box dimensions must change
    dimension = 0 if box_width < box_height else 1
    difference = abs(box_width - box_height)

    free_space = image_dimensions[dimension] - current_box[dimension + 2]

    if difference <= free_space:  # needed box growth can fit in image
        growth_needed = difference / 2

        # calculate the amount of px needed to grow in either direction
        negative_growth = current_box[dimension] - growth_needed
        negative_growth_debt = abs(negative_growth) if negative_growth < 0 else 0

        current_positive = current_box[dimension] + current_box[dimension + 2]
        positive_growth = (current_positive + growth_needed) - image_dimensions[dimension]
        positive_growth_debt = abs(positive_growth) if positive_growth > 0 else 0

        if negative_growth_debt == 0 and positive_growth_debt == 0:  # no debt, can grow freely
            current_box[dimension] -= growth_needed
            current_box[dimension + 2] += difference

        elif negative_growth_debt != 0:  # negative debt, grow positive as needed
            current_box[dimension] = 0
            # get the number for the opposite dimension
            current_box[dimension + 2] = current_box[3 - dimension]  

        else:  # positive debt, grow negative as needed
            current_box[dimension] -= growth_needed + positive_growth_debt
            current_box[dimension + 2] = current_box[3 - dimension]

        return current_box
    else:
        ret_list = [-1, -1, -1, -1]
        # store amount more pixels required
        ret_list[dimension] = image_dimensions[dimension] - current_box[dimension]  
        return ret_list


def parse_command_line_args():
    parser = argparse.ArgumentParser(description='Preprocess bird images to '
        'square uniform dimensions.')
    parser.add_argument('-d', '--images_directory', required=True, 
        help='Path to root images directory.')
    parser.add_argument('-i', '--images_file', required=True, help='Path to ' 
        'file with image id and name.')
    parser.add_argument('-b', '--bounding_box_file', required=True, help='Path to' 
        ' file with image id and bounding box info.')
    parser.add_argument('-o', '--output_directory', required=True, help='Path '
        'to directory where you want resulting image information stored.')
    return parser.parse_args()

def main():
    args = parse_command_line_args()
    images_directory = args.images_directory

    id_list = build_id_list(args.images_file)
    boxes = read_bounding_boxes(args.bounding_box_file)

    num_cant_resize = 0
    for i in range(len(id_list)):
        bird_id = id_list[i]
        current_box = boxes[i]

        with Image.open(images_directory + bird_id) as current_image:
            resized_box = resize_bounding(current_image.size, current_box)

            if -1 not in resized_box:
                boxes[i] = resized_box
            else:
                num_cant_resize += 1
                warn('Bounding box of bird {} could not be resized!'.format(i + 1))

    print('Could not resize {} images ({:.2f}%).'.format(num_cant_resize, 
        (num_cant_resize / len(id_list)) * 100))


if __name__ == '__main__':
    main()
