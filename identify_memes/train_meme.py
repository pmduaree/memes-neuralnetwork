# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
from load_images import load_memes

# Import tflearn and some helpers
import tflearn
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation


def train_meme(number_of_images, size, channel_color):
    file_name = '../resources/data/' + str(size) + 'x' + str(size) + '_' + str(channel_color) + '_memes_' + str(
        number_of_images)

    X, Y, X_test, Y_test = load_memes(number_of_images, size, channel_color)

    # Shuffle the data
    X, Y = shuffle(X, Y)

    # Make sure the data is normalized
    img_prep = ImagePreprocessing()
    img_prep.add_featurewise_zero_center()
    img_prep.add_featurewise_stdnorm()

    # Create extra synthetic training data by flipping, rotating and blurring the
    # images on our data set.
    img_aug = ImageAugmentation()
    img_aug.add_random_flip_leftright()
    img_aug.add_random_rotation(max_angle=25.)
    img_aug.add_random_blur(sigma_max=3.)

    # Define our network architecture:
    number_of_channels = 3 if channel_color == "RGB" else 1
    network = input_data(shape=[None, size, size, number_of_channels],
                         data_preprocessing=img_prep,
                         data_augmentation=img_aug)

    # Step 1: Convolution
    network = conv_2d(network, 32, 3, activation='relu')

    # Step 2: Max pooling
    network = max_pool_2d(network, 2)

    # Step 3: Convolution again
    network = conv_2d(network, 64, 3, activation='relu')

    # Step 4: Convolution yet again
    network = conv_2d(network, 64, 3, activation='relu')

    # Step 5: Max pooling again
    network = max_pool_2d(network, 2)

    # Step 6: Fully-connected 512 node neural network
    network = fully_connected(network, 512, activation='relu')

    # Step 7: Dropout - throw away some data randomly during training to prevent over-fitting
    network = dropout(network, 0.5)

    # Step 8: Fully-connected neural network with two outputs (0=isn't a meme, 1=is a meme)
    # to make the final prediction
    network = fully_connected(network, 2, activation='softmax')

    # Tell tflearn how we want to train the network
    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=0.001)

    # Wrap the network in a model object
    model = tflearn.DNN(network, tensorboard_verbose=0)

    # Train it! We'll do 100 training passes and monitor it as it goes.
    model.fit(X, Y, n_epoch=100, shuffle=True, validation_set=(X_test, Y_test),
              show_metric=True, batch_size=100,
              snapshot_epoch=True,
              run_id=file_name)

    model.save(file_name + '.tfl')

    # print(str(datetime.now()))


def main():
    # load the test data
    train_meme(1000, 100, "RGB")
    # train_meme(number_of_images, 25, "RGB") done
    # train_meme(number_of_images, 75, "RGB") done
    # train_meme(number_of_images, 100, "L") done
    # train_meme(number_of_images, 200, "RGB") maybe not


if __name__ == "__main__":
    main()
