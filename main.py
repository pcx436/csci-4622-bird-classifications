from PIL import Image
from warnings import warn
import argparse
import numpy as np
from sklearn.model_selection import train_test_split


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
        growth_needed = np.ceil(difference / 2)

        # calculate the amount of px needed to grow in either direction
        negative_growth = current_box[dimension] - growth_needed
        negative_growth_debt = abs(negative_growth) if negative_growth < 0 else 0

        current_positive = current_box[dimension] + current_box[dimension + 2]
        positive_growth = (current_positive + growth_needed) - image_dimensions[dimension]
        positive_growth_debt = abs(positive_growth) if positive_growth > 0 else 0

        if negative_growth_debt == 0 and positive_growth_debt == 0:  # no debt, can grow freely
            current_box[dimension] -= growth_needed
            current_box[dimension + 2] = current_box[3 - dimension]

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
    # TODO: update help parameters to do
    parser = argparse.ArgumentParser(description='Preprocess bird images to square uniform dimensions.')
    parser.add_argument('-d', '--images-directory',
                        help='Path to root images directory. Not used when -o is provided.')
    parser.add_argument('-l', '--image-list', required=True, help='Path to file with image id and name.')
    parser.add_argument('-b', '--bounding-box-file',
                        help='Path to file with image id and bounding box info. Not used when -o is provided.')

    in_or_out = parser.add_mutually_exclusive_group(required=True)
    in_or_out.add_argument('-o', '--output-file',
                           help='Path to file where you want resulting image information stored (npz format).')
    in_or_out.add_argument('-i', '--input-file', help='Path to .npz file containing image data.')
    return parser.parse_args()


def load_images(args):
    id_list = build_id_list(args.image_list)

    image_data = list()
    names_array = list()

    if args.output_file:  # haven't processed images once
        image_objects = list()

        images_directory = args.images_directory
        if images_directory[-1] != '/':
            images_directory += '/'

        boxes = read_bounding_boxes(args.bounding_box_file)

        num_cant_resize = 0
        min_width = -1

        for i in range(len(id_list)):
            bird_id = id_list[i]
            current_box = boxes[i]

            with Image.open(images_directory + bird_id) as current_image:
                # check for non-RGB images (e.g., grayscale, RGBA)
                if current_image.mode != 'RGB':
                    warn('Bird {} not RGB (mode {})'.format(i, current_image.mode))
                    continue

                resized_box = resize_bounding(current_image.size, current_box)

                if -1 not in resized_box:
                    boxes[i] = resized_box
                    cropped_image = crop_by_box(current_image, resized_box)

                    # record minimum width for resizing
                    if cropped_image.width < min_width or min_width == -1:
                        min_width = cropped_image.width

                    # save array data for each image
                    image_objects.append(cropped_image)

                    # save the name of each bird
                    names_array.append(bird_id)
                else:
                    num_cant_resize += 1
                    warn('Bounding box of bird {} could not be resized!'.format(i + 1))

        # resize all images to be the dimensions of the smallest image, translate to array data
        for image_obj in image_objects:
            image_obj.thumbnail((min_width, min_width))
            image_data.append(np.asarray(image_obj))

        print('Number of valid images: {}'.format(len(image_data)))
        print('Could not resize {} images ({:.2f}%).'.format(num_cant_resize,
                                                             (num_cant_resize / len(id_list)) * 100))
        print('Saving image data to {}...'.format(args.output_file))
        np.savez_compressed(args.output_file, image_data=image_data, image_names=names_array)
    else:  # images have been processed already
        loaded_arrays = np.load(args.input_file, allow_pickle=True)
        names_array = loaded_arrays['image_names']  # names will always be last array

        image_data = loaded_arrays['image_data']

    return image_data, names_array


def split_groups(image_array, name_array, percent_train=0.8, percent_test=0.1, seed=None):
    # check desired percentages add to 1.0
    if percent_train < 0 or percent_test < 0:
        raise RuntimeError('Percentage parameters passed to split_groups must be > 0')
    elif percent_test + percent_train > 1.0:
        raise RuntimeError('Percentages passed to split_groups must add to less than 1.0!')

    categories = list()

    for image_data, name in zip(image_array, name_array):
        cat_number = int(name[:3])  # first three characters are the category number

        if cat_number <= len(categories):  # have we seen this category before
            categories[cat_number - 1].append(image_data)
        else:
            categories.append([image_data])

    x_train = list()
    y_train = list()

    x_test = list()
    y_test = list()

    x_valid = list()
    y_valid = list()

    # grab actual data
    for i, data_array in enumerate(categories):
        cat_number = i + 1
        y_labels = [cat_number] * len(data_array)

        sub_X_train, sub_X_test, sub_y_train, sub_y_test = train_test_split(data_array, y_labels,
                                                                            train_size=percent_train, random_state=seed)

        sub_X_test, sub_X_val, sub_y_test, sub_y_val = train_test_split(sub_X_test, sub_y_test,
                                                                        train_size=percent_test,
                                                                        random_state=seed)  # 0.25 x 0.8 = 0.2

        x_train.extend(sub_X_train)
        y_train.extend(sub_y_train)

        x_test.extend(sub_X_test)
        y_test.extend(sub_y_test)

        x_valid.extend(sub_X_val)
        y_valid.extend(sub_y_val)

    return x_train, y_train, x_test, y_test, x_valid, y_valid


def main():
    args = parse_command_line_args()

    (image_array, name_array) = load_images(args)

    split_groups(image_array, name_array)
    x_train, y_train, x_test, y_test, x_valid, y_valid = split_groups(image_array, name_array, seed=12345)

    print(.8 * len(image_array), len(x_train), len(y_train))
    print(.1 * len(image_array), len(x_test), len(y_test))
    print(.1 * len(image_array), len(x_valid), len(y_valid))


if __name__ == '__main__':
    main()
