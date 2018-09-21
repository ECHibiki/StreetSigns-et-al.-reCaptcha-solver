import numpy as np
import os
import time
import pickle
import random
import numpy as np
from scipy import misc
from skimage import feature
from skimage import transform
import tensorflow as tf
import requests
from PIL import Image
from io import BytesIO
import copy
from skimage.io import imsave, imread
from threading import *

resize = int(input('Resize int: '))

train_paths = os.listdir('data/train')
valid_paths = os.listdir('data/valid')
test_paths = os.listdir('data/test')

threads = []

def resize_fn(folder, path, image_path):
    image_pixels = misc.imread("data/" + folder + "/" + path + "/" + image_path)
    image_pixels = transform.resize(image_pixels, (resize,resize,))
    imsave("data/" + folder + "/" + path + "/" + image_path, image_pixels)
    print("data/" + folder + "/" + path + "/" + image_path)

for path in train_paths:
    image_folder = os.listdir('data/train/' + path)
    for image_path in image_folder:
        thread = Thread(target=resize_fn,args=('train',path,image_path,))
        thread.start()
        threads.append(thread)

for thread in threads:
    thread.join()

threads = []

for path in valid_paths:
    image_folder = os.listdir('data/valid/' + path)
    for image_path in image_folder:
        thread = Thread(target=resize_fn,args=('valid',path,image_path,))
        thread.start()
        threads.append(thread)

for thread in threads:
    thread.join()

threads = []

for path in test_paths:
    image_folder = os.listdir('data/test/' + path)
    for image_path in image_folder:
        thread = Thread(target=resize_fn,args=('test',path,image_path,))
        thread.start()
        threads.append(thread)

for thread in threads:
    thread.join()

threads = []