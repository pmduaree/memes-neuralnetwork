import os
import scipy
import numpy as np

path_to_resources = '../resources/'

delimiter = '###'


def is_image(image_path):
    extension = image_path.split('.')[-1]
    return extension == 'jpg' or extension == 'png' or extension == 'jpeg'


def load_image(path_to_images, is_meme, index, number_of_images_to_download,
               is_reverse=False, size=100, color_channel="RGB"):
    X, Y = [], []
    list_of_images = os.listdir(path_to_images)
    images_saved = 0
    index_reverse = -1 if is_reverse else 1
    while images_saved < number_of_images_to_download:
        image_name = list_of_images[index_reverse * index]
        image_path = path_to_images + image_name
        if is_image(image_name):
            # Load the image file
            try:
                img = scipy.ndimage.imread(image_path, mode=color_channel)
                img = scipy.misc.imresize(img, (size, size), interp="bicubic").astype(np.float32, casting='unsafe')
                if color_channel == 'L':
                    img = img.reshape((size, size, 1))
                X.append(img)
                y = [0, 1] if is_meme else [1, 0]
                Y.append(y)
                images_saved += 1
            except:
                pass

        index += 1
    return X, Y, images_saved


def load_memes(number_of_images, size, color_channel):
    number_of_test_images = 0.1 * number_of_images  # 10% number of images

    print 'loading data (' + str(number_of_images) + ')'
    # train data
    # memes
    print 'train memes'
    path_to_images = path_to_resources + 'memes/'
    X_train, Y_train, index_memes = load_image(path_to_images, True, 0, number_of_images, size=size,
                                               color_channel=color_channel)

    # nonmemes
    print 'train non_memes'
    path_to_images = path_to_resources + 'non_memes/'
    X, Y, index_non_memes = load_image(path_to_images, False, 0, number_of_images, size=size,
                                       color_channel=color_channel)
    X_train += X
    Y_train += Y

    # test data
    # memes
    print 'test memes'
    path_to_images = path_to_resources + 'memes/'
    X_test, Y_test, _ = load_image(path_to_images, True, index_memes, number_of_test_images, size=size,
                                   color_channel=color_channel)

    # nonmemes
    print 'test non memes'
    path_to_images = path_to_resources + 'non_memes/'
    X, Y, _ = load_image(path_to_images, False, index_non_memes, number_of_test_images, size=size,
                         color_channel=color_channel)
    X_test += X
    Y_test += Y

    print 'finished loading ' + str(2 * (number_of_images + number_of_test_images)) + ' images'
    return X_train, Y_train, X_test, Y_test


def load_validation_memes(number_of_images=2000, size=100, color_channel='RGB'):
    # validation data
    # memes
    print 'validation memes'
    path_to_images = path_to_resources + 'memes/'
    X_validation, Y_validation, index_memes = load_image(path_to_images, True, 0, number_of_images, True, size=size,
                                                         color_channel=color_channel)

    # non memes
    print 'validation non_memes'
    path_to_images = path_to_resources + 'non_memes/'
    X, Y, index_non_memes = load_image(path_to_images, False, 0, number_of_images, True, size=size,
                                       color_channel=color_channel)
    X_validation += X
    Y_validation += Y
    return X_validation, Y_validation
