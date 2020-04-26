from PIL import Image, ImageDraw
from sys import stderr
from numpy.random import randint


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

            converted_tuple = [float(param) for param in line_split]  # convert coords to float, place in list
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
            current_box[dimension + 2] = current_box[3 - dimension]  # get the number for the opposite dimension

        else:  # positive debt, grow negative as needed
            current_box[dimension] -= growth_needed + positive_growth_debt
            current_box[dimension + 2] = current_box[3 - dimension]

        return current_box
    else:
        ret_list = [-1, -1, -1, -1]
        ret_list[dimension] = image_dimensions[dimension] - current_box[dimension]  # store amount more pixels required
        return ret_list


def main():
    images_directory = 'CUB_200_2011/images/'

    id_list = build_id_list('CUB_200_2011/images.txt')
    boxes = read_bounding_boxes('CUB_200_2011/bounding_boxes.txt')

    # test_image_name = '072.Pomarine_Jaeger/Pomarine_Jaeger_0029_61365.jpg'
    # test_image_name = '110.Geococcyx/Geococcyx_0099_104134.jpg'
    # test_image_name = '156.White_eyed_Vireo/White_Eyed_Vireo_0018_159450.jpg'
    # test_image_name = '190.Red_cockaded_Woodpecker/Red_Cockaded_Woodpecker_0025_794710.jpg'
    test_image_name = '157.Yellow_throated_Vireo/Yellow_Throated_Vireo_0025_795009.jpg'

    i = id_list.index(test_image_name)

    # First image in the first category
    test_image_path = images_directory + test_image_name

    num_birds = int(input('Please enter the number of birds you would like to see: '))
    # try 5 random images to resize the box of
    for i in randint(0, high=len(id_list), size=num_birds):
        image_name = id_list[i]
        current_box = boxes[i]

        with Image.open(images_directory + image_name) as current_image:
            print('Current image:', image_name)
            print('Current image dimensions:', current_image.size)
            print('Current bounding box:', current_box)
            # current_image = draw_bounding(current_image, current_box, 'red')
            # current_image.show()

            new_bounding_box = resize_bounding(current_image.size, current_box)

            # error checking:
            (new_width, new_height) = new_bounding_box[2:]


            print('New bounding box:', new_bounding_box)
            print('New bounding box (cart):', convert_cartesian(new_bounding_box))

            if new_bounding_box[0] == -1:
               print('Height of new bounding box for bird {} short by {}px.'.format(i, new_bounding_box[1]),
                     file=stderr)
            elif new_bounding_box[1] == -1:
                print('Width of new bounding box for bird {} short by {}px.'.format(i, new_bounding_box[0]),
                      file=stderr)
            else:
                print('Bounding box for bird id {} successfully resized!'.format(i))
                image_with_resized_box = crop_by_box(current_image, new_bounding_box)
                image_with_resized_box.show()

    # going to try drawing the bounding box
    # bounded_image = draw_bounding(test_image, boxes[0])

    # attempt to crop image
    # cropped_image = crop_by_box(test_image, boxes[0])
    # cropped_image.show()


if __name__ == '__main__':
    main()
