# Neural network and memes

This project is all about trying to identify images and if it's a meme or not. This is just of fun. 
  
# How to use

First, you need to install some dependencies first

- [Python](https://www.python.org/downloads/)
- [TensorFlow](https://www.tensorflow.org/install/)
- [Numpy](https://docs.scipy.org/doc/numpy/user/install.html)
- [TFLearn](http://tflearn.org/installation/)

# First step

The first step is to gather all the images. You can find a file named **reddit_get_images.py** in the module download_images. Let it run. It takes a while to download all the images. In average, it takes like 30-40 minutes.

Note: it only works once a day. This is because of how reddit works

# Train the neural network

After we got all the images, we need to have all the dependencies installed. After you have that, run a file named **train_meme.py** in the identify_memes module. It takes a while. 

I have preselected some variables for you. Feel free to play with them as much as you want. 

If you want more precision, then you have to download more images

# Evaluate the network

Finally, if you trained correctly the images, feel free to evaluate what you just trained. In the identify_memes module there is a file named **evauluate_memes.py**. Run it. 

The output is gonna have a lot of values, like true positives, false positives, true negatives and false negatives. Feel free to read this [wikipedia article](https://en.wikipedia.org/wiki/Precision_and_recall) if you want more details.

# Contact

Email: pduarte@nearsoft.com