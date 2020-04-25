from PIL import Image

def build_id_list(filename):
    id_list = list()

    with open(filename, 'r') as library_file:
        for line in library_file:
            line_split = line.strip().split(' ')

            id_list.append(line_split[1])  # add the name of the file to the list

    return id_list


def main():
    images_directory = 'CUB_200_2011/images/'

    # First image in the first category
    test_image_path = images_directory + '001.Black_footed_Albatross/Black_Footed_Albatross_0001_796111.jpg'

    test_image = Image.open(test_image_path)

    print('Test image dimensions:', test_image.size)


if __name__ == '__main__':
    main()
