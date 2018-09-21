import numpy as np
import os
import time
import pickle
import random
import numpy as np
from scipy import misc
from skimage import feature
import tensorflow as tf
import requests
from PIL import Image
from io import BytesIO
import copy

from skimage.io import imsave, imread
while True:
    path = input('set path: ')
    sigma_= float(input('sigma: '))
    low_threshold_ = float(input('low_threshold: '))
    high_threshold_ = float(input('high_threshold: '))
    # Grey
    image_pixels = misc.imread('data\\valid\\bus-cars-roads-traffic lights\\' + path, "L")
    edge_pixels = feature.canny(image_pixels, sigma=sigma_, low_threshold=0, high_threshold =0.10).astype(int)
    for pixel in np.nditer(edge_pixels, op_flags=['readwrite']):
        pixel[...] = int(pixel) * 255.0
    image = edge_pixels
    imsave('tests/' + path, image)
    rb_image = imread('tests/' + path)
    print("original image")
    print(image)
    print("read back image")
    print(rb_image)