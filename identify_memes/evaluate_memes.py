# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
from load_images import load_validation_memes

# Import tflearn and some helpers
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import numpy as np


def print_info_from_validation(Y_validate, Y_calculated, file_name):
    true_positives, true_negatives, false_positives, false_negatives = 0, 0, 0, 0
    size = len(Y_calculated)
    for i in range(0, size):
        # in real is a meme
        if Y_validate[i][1] == 1:
            # calculated a meme
            if np.argmax(Y_calculated[i]) == 1:
                true_positives += 1
            # calculated not a meme
            else:
                false_negatives += 1
        # in real is not a meme
        else:
            # calculated not a meme
            if np.argmax(Y_calculated[i]) == 0:
                true_negatives += 1
            else:
                false_positives += 1

    f = open(file_name + '.dat', 'w')
    f.write('True positives: ' + str(true_positives) + '\n')
    f.write('False positives: ' + str(false_positives) + '\n')
    f.write('True negatives: ' + str(true_negatives) + '\n')
    f.write('False negatives: ' + str(false_negatives) + '\n')
    f.write('True positives (%): ' + str(1.0 * true_positives / size) + '\n')
    f.write('False positives (%): ' + str(1.0 * false_positives / size) + '\n')
    f.write('True negatives (%): ' + str(1.0 * true_negatives / size) + '\n')
    f.write('False negatives (%): ' + str(1.0 * false_negatives / size) + '\n')
    f.write('Precision (true positives / all positive guesses ' + str(
        100.0 * true_positives / (true_positives + false_positives)) + '%' + '\n')
    f.write('Recall (true positives / number of memes) ' + str(100.0 * true_positives / (size * 0.5)) + '%' + '\n')
    f.close()

    print('True positives: ' + str(true_positives))
    print('False positives: ' + str(false_positives))
    print('True negatives: ' + str(true_negatives))
    print('False negatives: ' + str(false_negatives))
    print('True positives (%): ' + str(1.0 * true_positives / size))
    print('False positives (%): ' + str(1.0 * false_positives / size))
    print('True negatives (%): ' + str(1.0 * true_negatives / size))
    print('False negatives (%): ' + str(1.0 * false_negatives / size))
    print('Precision (true positives / all positive guesses ' + str(
        100.0 * true_positives / (true_positives + false_positives)) + '%')
    print('Recall (true positives / number of memes) ' + str(100.0 * true_positives / (size * 0.5)) + '%')


def evaluate(size=100, channel_color='RGB', number_of_validation_images=32000, number_of_evaluation_images=3000):
    print('------------------------------')
    img_prep = ImagePreprocessing()
    img_prep.add_featurewise_zero_center()
    img_prep.add_featurewise_stdnorm()

    img_aug = ImageAugmentation()
    img_aug.add_random_flip_leftright()
    img_aug.add_random_rotation(max_angle=25.)
    img_aug.add_random_blur(sigma_max=3.)

    file_name = '../resources/data/' + str(size) + 'x' + str(size) + '_' + str(channel_color) + '_memes_' + str(
        number_of_validation_images)

    # Network architecture:
    number_of_channels = 3 if channel_color == 'RGB' else 1
    network = input_data(shape=[None, size, size, number_of_channels],
                         data_preprocessing=img_prep,
                         data_augmentation=img_aug)

    network = conv_2d(network, 32, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 64, 3, activation='relu')
    network = conv_2d(network, 64, 3, activation='relu')
    network = max_pool_2d(network, 2)
    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.5)
    network = fully_connected(network, 2, activation='softmax')
    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=0.001)

    model = tflearn.DNN(network, tensorboard_verbose=0)
    model.load(file_name + '.tfl')

    X_validate, Y_validate = load_validation_memes(number_of_evaluation_images, size, channel_color)

    print('start predicting')
    Y_calculated = model.predict(X_validate)
    print('finished predicting')
    print_info_from_validation(Y_validate, Y_calculated, file_name)


if __name__ == '__main__':
    evaluate(100, 'RGB', 1000, 200)
