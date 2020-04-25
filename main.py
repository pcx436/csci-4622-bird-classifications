from PIL import Image


def main():
    images_directory = 'CUB_200_2011/images/'

    # First image in the first category
    test_image_path = images_directory + '001.Black_footed_Albatross/Black_Footed_Albatross_0001_796111.jpg'

    test_image = Image.open(test_image_path)

    print('Test image dimensions:', test_image.size)


if __name__ == '__main__':
    main()
