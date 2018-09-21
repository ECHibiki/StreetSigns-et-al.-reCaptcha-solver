'''
Templated from: https://github.com/MicrocontrollersAndMore/TensorFlow_Tut_1_Installation_and_First_Progs/blob/master/mnist_deep.py
'''

import numpy as np
import tensorflow as tf
import sys
sys.path.insert(0, 'includes/')
import visualizations


def cnnModel(training_data, channels, classes, dimension_x, dimension_y):
    """
    Convolution -> Relu -> Pool
    Aux dropout
    Convolution -> Relu -> Pool
    Aux dropout
    Fully connected -> Relu
                                            Main Dropout
                                            Fully connected -> Relu
    Main Dropout
    Aproximations

    
     
     Testing shows that the following does not work well for multi labled CNNs. 0.97 yields best results
     https://stats.stackexchange.com/questions/240305/where-should-i-place-dropout-layers-in-a-neural-network
     
     Alterations for underfitting issues
     https://stackoverflow.com/questions/37268974/high-bias-convolutional-neural-network-not-improving-with-more-layers-filters
      """
    # Reshape to use within a convolutional neural net.
    # Last dimension is for "features" - there is only one here, since images are
    # 1 for greyscale, 3 for an RGB image, 4 for RGBgrey, etc.
    with tf.name_scope('reshape'):
        x_image = tf.reshape(training_data, [-1, dimension_x, dimension_y, channels])

    # First convolutional layer - maps n Depth image to 32 feature maps.
    with tf.name_scope('conv1'):
        W_conv1 = weight_variable([5, 5, channels, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    # Pooling layer - downsamples by 2X.
    with tf.name_scope('pool1'):
        h_pool1 = max_pool_5x5(h_conv1)
        # visualizations.modelSummary(W_conv1, b_conv1, h_conv1, h_pool1)

    # lesser dropout 1    - At a small ammount as research suggests
    convolution_keep_prob = tf.placeholder(tf.float32)
    with tf.name_scope('aux-dropout01'):
        c1_drop = tf.nn.dropout(h_pool1, convolution_keep_prob)
        
    # Second convolutional layer -- maps 32 feature maps to 64.
    with tf.name_scope('conv2'):
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(c1_drop, W_conv2) + b_conv2)

    # Second pooling layer.
    with tf.name_scope('pool2'):
        h_pool2 = max_pool_2x2(h_conv2)
        # visualizations.modelSummary(W_conv2, b_conv2, h_conv2, h_pool2)
            
    # lesser dropout 2
    with tf.name_scope('aux-dropout02'):
        c2_drop = tf.nn.dropout(h_pool2, convolution_keep_prob)

    # third convolutional layer -- maps 64 feature maps to 64.
    with tf.name_scope('conv3'):
        W_conv3 = weight_variable([5, 5, 64, 64])
        b_conv3 = bias_variable([64])
        h_conv3 = tf.nn.relu(conv2d(c2_drop, W_conv3) + b_conv3)

    # third pooling layer.
    with tf.name_scope('pool3'):
        h_pool3 = max_pool_2x2(h_conv3)                    
      
    
    # lesser dropout 3
    with tf.name_scope('aux-dropout02'):
        c3_drop = tf.nn.dropout(h_pool3, convolution_keep_prob)               
            
    # Fully connected layer 1 -- after 2 round of downsampling, our 28x28 image
    # is down to 5x5x256 feature maps -- maps this to 1024 features.
    with tf.name_scope('fc1'):
        W_fc1 = weight_variable([int(dimension_x / 20) * int(dimension_y /20) * 64, 1024])
        print(np.shape(h_pool1))
        print(np.shape(h_pool2))
        print(np.shape(h_pool3))
        b_fc1 = bias_variable([1024])

        h_pool2_flat = tf.reshape(c3_drop, [-1, int(dimension_x / 20) * int(dimension_y /20) * 64])
        # h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        h_fc1 = (tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        # visualizations.modelSummary(W_fc1, b_fc1, h_fc1, h_pool2_flat)
        
    # Dropout - controls the complexity of the model, prevents co-adaptation of
    # features.
    with tf.name_scope('main-dropout1'):
        base_keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, base_keep_prob)    
    
    # Map the 1024 features to n classes, one for each digit
    with tf.name_scope('fc3'):
        W_fc2 = weight_variable([1024, classes])
        b_fc2 = bias_variable([classes])

        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
        # visualizations.modelSummary(W_fc2, b_fc2, y_conv, 0)
    return y_conv, base_keep_prob, convolution_keep_prob

def conv2d(x, W):
    """conv2d returns a 2d convolution layer with full stride."""
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    """max_pool_2x2 downsamples a feature map by 2X."""
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')
def max_pool_5x5(x):
    """max_pool_5x5 downsamples a feature map by 5X."""
    return tf.nn.max_pool(x, ksize=[1, 5, 5, 1],
                          strides=[1, 5, 5, 1], padding='SAME')

def weight_variable(shape):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)
