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

train_data = [[],[]]
train_data_paths = [[],[]]
valid_data = [[],[]]
test_data = [[],[]]
color_setting = 0
class_number = 0
np.random.seed(int(time.time()))

def interpretNumberToClass(num):
    if num is 0:
        return 'fire hydrant'
    elif num is 1:
        return 'bicycle'
    elif num is 2:
        return 'boats'
    elif num is 3:
        return 'bridges'
    elif num is 4:
        return 'bus'
    elif num is 5:
        return 'cars'
    elif num is 6:
        return 'crosswalk'
    elif num is 7:
        return 'motorcycles'
    elif num is 8:
        return 'mountains'
    elif num is 9:
        return 'roads'
    elif num is 10:
        return 'statues'
    elif num is 11:
        return 'taxis'
    elif num is 12:
        return 'traffic lights'
    elif num is 13:
        return 'palm trees'
    else:
        print('X ' + num + ' X')
        return None

def interpretNameToClass(name):
    if name == 'a fire hydrant':
        return 0
    elif name == 'bicycles':
        return 1
    elif name == 'boats':
        return 2
    elif name == 'bridges':
        return 3
    elif name == 'bus':
        return 4
    elif name == 'cars':
        return 5
    elif name == 'crosswalks' or name == 'pedestrian crossing':
        return 6
    elif name == 'motorcycles':
        return 7
    elif name == 'mountains or hills':
        return 8
    elif name == 'roads':
        return 9
    elif name == 'statues':
        return 10
    elif name == 'taxis':
        return 11
    elif name == 'traffic lights':
        return 12
    elif name == 'palm trees':
        return 13
    else:
        print('X ' + name + ' X')
        return -1

def resize_fn(image_pixels, resize):
    return transform.resize(image_pixels, (resize,resize,))
        
def split9x9(url):
    image = ''
    retry_max = 10
    count = 0
    sleep_rate = 5
    while count < retry_max:
        try:
            image = requests.get(url)
            break
        except Exception:
            print('req retry')
            time.sleep(sleep_rate)
            count = count + 1
    if count == retry_max: 
        print(f'req fail X {retry_max} at {sleep_rate} req/sec')
        return None, False
    nine_by_one = Image.open(BytesIO(image.content))
    three_by_three = []
    for image_y in range(3):
        for image_x in range(3):
            crop = nine_by_one.crop((image_x * 100, image_y * 100, image_x * 100 + 100, image_y * 100 + 100))
            crop.save("tmp/img" + str(image_x) + str(image_y) + ".jpg")
            three_by_three.append("tmp/img" + str(image_x) + str(image_y) + ".jpg")
    return three_by_three, True

def loadImage_Greyscale(path):
    rtn_arr = (np.zeros(shape=(1, 1, 100*100)))
    # Grey
    image_pixels = misc.imread(path, "L")
    image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_grey, op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0    
    rtn_arr[0][0] = np.reshape(np.asarray(image_pixels_grey), [10000])
    return rtn_arr

def loadImage_RGB_Greyscale_Canny(path):
    rtn_arr = (np.zeros(shape=(1, 5, 100*100)))
    # rgb
    image_pixels = misc.imread(path)
    image_pixels_rgb = np.reshape(image_pixels, [-1,3]) # 1 for grey/canny, 3 for RGB
    for pixel in np.nditer(image_pixels_rgb.astype(np.float32), op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for index, pixel_group in enumerate(image_pixels_rgb):
        rtn_arr[0][0][index] = pixel_group[0]
        rtn_arr[0][1][index] = pixel_group[1]
        rtn_arr[0][2][index] = pixel_group[2]
    # Grey
    image_pixels = misc.imread(path, "L")
    image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_grey.astype(np.float32), op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0    
    rtn_arr[0][3] = np.reshape(np.asarray(image_pixels_grey), [10000])
    #canny    
    edge_pixels = feature.canny(image_pixels, sigma=3)
    edge_pixels = np.reshape(edge_pixels.astype(np.float32), [-1,1]) 
    # for pixel in np.nditer(edge_pixels, op_flags=['readwrite']):
        # pixel[...] = float(pixel) / 255.0
    rtn_arr[0][4] = np.reshape(np.asarray(edge_pixels), [10000])
    return rtn_arr

def loadImage_RGB(path):
    rtn_arr = (np.zeros(shape=(1, 3, 100*100)))
    # rgb
    image_pixels = misc.imread(path)
    image_pixels_rgb = np.reshape(image_pixels, [-1,3]) # 1 for grey/canny, 3 for RGB
    for pixel in np.nditer(image_pixels_rgb.astype(np.float32), op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for index, pixel_group in enumerate(image_pixels_rgb):
        rtn_arr[0][0][index] = pixel_group[0]
        rtn_arr[0][1][index] = pixel_group[1]
        rtn_arr[0][2][index] = pixel_group[2]
    return rtn_arr
    
def loadImage_RGB_Greyscale_Canny(path):
    rtn_arr = (np.zeros(shape=(1, 4, 100*100)))
    # rgb
    image_pixels = misc.imread(path)
    image_pixels_rgb = np.reshape(image_pixels, [-1,3]) # 1 for grey/canny, 3 for RGB
    for pixel in np.nditer(image_pixels_rgb.astype(np.float32), op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for index, pixel_group in enumerate(image_pixels_rgb):
        rtn_arr[0][0][index] = pixel_group[0]
        rtn_arr[0][1][index] = pixel_group[1]
        rtn_arr[0][2][index] = pixel_group[2]
    # Grey
    image_pixels = misc.imread(path, "L")
    image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_grey.astype(np.float32), op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0    
    rtn_arr[0][3] = np.reshape(np.asarray(image_pixels_grey), [10000])
    return rtn_arr

def loadAllToMemory_RGB_Greyscale_Canny(class_size):
    global color_setting
    color_setting = 5
    loadDirToMemory_RGB_GreyScale_Canny('data/train', train_data, class_size)
    loadDirToMemory_RGB_GreyScale_Canny('data/valid', valid_data, class_size)
    loadDirToMemory_RGB_GreyScale_Canny('data/test', test_data, class_size)
    
def loadPartialToMemory_RGB_Greyscale_Canny(class_size):
    global color_setting
    color_setting = 5
    loadDirPaths('data/train', train_data_paths, class_size)
    loadDirToMemory_RGB_GreyScale_Canny('data/valid', valid_data, class_size)
    loadDirToMemory_RGB_GreyScale_Canny('data/test', test_data, class_size)

def loadPartialToMemory_RGB_Greyscale(class_size):
    global color_setting
    color_setting = 4
    loadDirPaths('data/train', train_data_paths, class_size)
    loadDirToMemory_RGB_GreyScale('data/valid', valid_data, class_size)
    loadDirToMemory_RGB_GreyScale('data/test', test_data, class_size)
    
def loadPartialToMemory_RGB(class_size):
    global color_setting
    color_setting = 3
    loadDirPaths('data/train', train_data_paths, class_size)
    loadDirToMemory_RGB('data/valid', valid_data, class_size)
    loadDirToMemory_RGB('data/test', test_data, class_size)

def loadPartialToMemory_Greyscale(class_size):
    global color_setting
    color_setting = 0
    loadDirPaths('data/train', train_data_paths, class_size)
    loadDirToMemory_Greyscale('data/valid', valid_data, class_size)
    loadDirToMemory_Greyscale('data/test', test_data, class_size)
    
def loadPartialToMemory_Canny(class_size):
    global color_setting
    color_setting = 1
    loadDirPaths('data/train', train_data_paths, class_size)
    loadDirToMemory_Canny('data/valid', valid_data, class_size)
    loadDirToMemory_Canny('data/test', test_data, class_size)

def loadDirToMemory_RGB_GreyScale_Canny(path, path_arr, class_size):
    path_directory = os.listdir(path)
    label_length = len(path_directory)
    file_count = 0
    print(str(path_directory))
    for index, directory in enumerate(path_directory):
        files = os.listdir(path + '/' + directory)
        directory_list = directory.split("-");
        one_hot = np.zeros(class_size)
        for dir in directory_list:
            index = interpretNameToClass(dir)
            if index < 0:
                continue
            one_hot[index] = 1.0
        print(one_hot)
        print(directory_list)
        for image in files:
            path_arr[0].append([[],[],[],[],[]])
            # RGB
            image_pixels_rgb = misc.imread(path + '/' + directory + '/' + image)
            image_pixels_rgb = np.reshape(image_pixels_rgb.astype(np.float32), [-1,3]) # 1 for grey, 3 for RGB
            for pixel in np.nditer(image_pixels_rgb, op_flags=['readwrite']):
                pixel[...] = float(pixel) / 255.0
            for pixel_group in image_pixels_rgb:
                path_arr[0][file_count][0].append(pixel_group[0])
                path_arr[0][file_count][1].append(pixel_group[1])
                path_arr[0][file_count][2].append(pixel_group[2])
            # Grey
            image_pixels = misc.imread(path + '/' + directory + '/' + image, "L")
            image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
            for pixel in np.nditer(image_pixels_grey, op_flags=['readwrite']):
                pixel[...] = float(pixel) / 255.0
            for pixel_group in image_pixels_grey:        
                path_arr[0][file_count][3].append(pixel_group[0])
        #Canny
            edge_pixels = feature.canny(image_pixels, sigma=3)
            edge_pixels = np.reshape(edge_pixels.astype(np.float32), [-1,1]) 
            # for pixel in np.nditer(edge_pixels, op_flags=['readwrite']):
                # pixel[...] = float(pixel) / 255.0
            for pixel_group in edge_pixels:
                path_arr[0][file_count][4].append(pixel_group[0])
            path_arr[1].append(one_hot)
            file_count = file_count + 1
        global class_number
        class_number = class_size

def loadDirToMemory_RGB_GreyScale(path, path_arr, class_size):
    path_directory = os.listdir(path)
    label_length = len(path_directory)
    file_count = 0
    print(str(path_directory))
    for index, directory in enumerate(path_directory):
        files = os.listdir(path + '/' + directory)
        directory_list = directory.split("-");
        one_hot = np.zeros(class_size)
        for dir in directory_list:
            index = interpretNameToClass(dir)
            if index < 0:
                continue
            one_hot[index] = 1.0
        print(one_hot)
        print(directory_list)
        for image in files:
            path_arr[0].append([[],[],[],[]])
            # RGB
            image_pixels_rgb = misc.imread(path + '/' + directory + '/' + image)
            image_pixels_rgb = np.reshape(image_pixels_rgb.astype(np.float32), [-1,3]) # 1 for grey, 3 for RGB
            for pixel in np.nditer(image_pixels_rgb, op_flags=['readwrite']):
                pixel[...] = float(pixel) / 255.0
            for pixel_group in image_pixels_rgb:
                path_arr[0][file_count][0].append(pixel_group[0])
                path_arr[0][file_count][1].append(pixel_group[1])
                path_arr[0][file_count][2].append(pixel_group[2])
            # Grey
            image_pixels = misc.imread(path + '/' + directory + '/' + image, "L")
            image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
            for pixel in np.nditer(image_pixels_grey, op_flags=['readwrite']):
                pixel[...] = float(pixel) / 255.0
            for pixel_group in image_pixels_grey:        
                path_arr[0][file_count][3].append(pixel_group[0])
            path_arr[1].append(one_hot)
            file_count = file_count + 1
        global class_number
        class_number = class_size

def loadDirToMemory_RGB(path, path_arr, class_size):
    path_directory = os.listdir(path)
    label_length = len(path_directory)
    file_count = 0
    print(str(path_directory))
    for index, directory in enumerate(path_directory):
        files = os.listdir(path + '/' + directory)
        directory_list = directory.split("-");
        one_hot = np.zeros(class_size)
        for dir in directory_list:
            index = interpretNameToClass(dir)
            if index < 0:
                continue
            one_hot[index] = 1.0
        print(one_hot)
        print(directory_list)
        for image in files:
            path_arr[0].append([[],[],[]])
            # RGB
            image_pixels_rgb = misc.imread(path + '/' + directory + '/' + image)
            image_pixels_rgb = np.reshape(image_pixels_rgb.astype(np.float32), [-1,3]) # 1 for grey, 3 for RGB
            for pixel in np.nditer(image_pixels_rgb, op_flags=['readwrite']):
                pixel[...] = float(pixel) / 255.0
            for pixel_group in image_pixels_rgb:
                path_arr[0][file_count][0].append(pixel_group[0])
                path_arr[0][file_count][1].append(pixel_group[1])
                path_arr[0][file_count][2].append(pixel_group[2])
            path_arr[1].append(one_hot)
            file_count = file_count + 1
        global class_number
        class_number = class_size
        
def loadDirToMemory_Greyscale(path, path_arr, class_size):
    path_directory = os.listdir(path)
    label_length = len(path_directory)
    file_count = 0
    print(str(path_directory))
    for index, directory in enumerate(path_directory):
        files = os.listdir(path + '/' + directory)
        directory_list = directory.split("-");
        one_hot = np.zeros(class_size)
        for dir in directory_list:
            index = interpretNameToClass(dir)
            if index < 0:
                continue
            one_hot[index] = 1.0
        print(one_hot)
        print(directory_list)
        for image in files:
            path_arr[0].append([[]])       
            # Grey
            image_pixels = misc.imread(path + '/' + directory + '/' + image, "L")
            image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
            for pixel in np.nditer(image_pixels_grey, op_flags=['readwrite']):
                pixel[...] = float(pixel) / 255.0
            for pixel_group in image_pixels_grey:        
                path_arr[0][file_count][0].append(pixel_group[0])
            path_arr[1].append(one_hot)
            file_count = file_count + 1
        global class_number
        class_number = class_size
        
def loadDirToMemory_Canny(path, path_arr, class_size):
    path_directory = os.listdir(path)
    label_length = len(path_directory)
    file_count = 0
    print(str(path_directory))
    for index, directory in enumerate(path_directory):
        files = os.listdir(path + '/' + directory)
        directory_list = directory.split("-");
        one_hot = np.zeros(class_size)
        for dir in directory_list:
            index = interpretNameToClass(dir)
            if index < 0:
                continue
            one_hot[index] = 1.0
        print(one_hot)
        print(directory_list)
        for image in files:
            path_arr[0].append([[]])
        #Canny
            edge_pixels = feature.canny(image_pixels, sigma=3)
            edge_pixels = np.reshape(edge_pixels.astype(np.float32), [-1,1]) 
            # for pixel in np.nditer(edge_pixels, op_flags=['readwrite']):
                # pixel[...] = float(pixel) / 255.0
            for pixel_group in edge_pixels:
                path_arr[0][file_count][0].append(pixel_group[0])
            path_arr[1].append(one_hot)
            file_count = file_count + 1
        global class_number
        class_number = class_size
        
        
def loadDirPaths(path, path_arr, class_size):
    path_directory = os.listdir(path)
    label_length = len(path_directory)
    file_count = 0
    print(str(path_directory))
    for index, directory in enumerate(path_directory):
        files = os.listdir(path + '/' + directory)
        directory_list = directory.split("-");
        one_hot = np.zeros(class_size)
        for dir in directory_list:
            index = interpretNameToClass(dir)
            if index < 0:
                continue
            one_hot[index] = 1.0
        print(one_hot)
        print(directory_list)
        for image in files:
            path_arr[0].append(path + '/' + directory + '/' + image)
            path_arr[1].append(one_hot)
            file_count = file_count + 1
        global class_number
        class_number = class_size

def LoadPathToTrain_RGB_GreyScale_Canny(path, one_hot):
    train_data[0].append([[],[],[],[],[]])
    train_data[1].append(one_hot)
    # RGB
    image_pixels_rgb = misc.imread(path)
    image_pixels_rgb = np.reshape(image_pixels_rgb.astype(np.float32), [-1,3]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_rgb, op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for pixel_group in image_pixels_rgb:
        train_data[0][len(train_data[0]) - 1][0].append(pixel_group[0])
        train_data[0][len(train_data[0]) - 1][1].append(pixel_group[1])
        train_data[0][len(train_data[0]) - 1][2].append(pixel_group[2])
    # Grey
    image_pixels = misc.imread(path, "L")
    image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_grey, op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for pixel_group in image_pixels_grey:        
        train_data[0][len(train_data[0]) - 1][3].append(pixel_group[0])
#Canny
    edge_pixels = feature.canny(image_pixels, sigma=3)
    edge_pixels = np.reshape(edge_pixels.astype(np.float32), [-1,1]) 
    # for pixel in np.nditer(edge_pixels, op_flags=['readwrite']):
        # pixel[...] = float(pixel) / 255.0
    for pixel_group in edge_pixels:
        train_data[0][len(train_data[0]) - 1][4].append(pixel_group[0])

def LoadPathToTrain_RGB_GreyScale(path, one_hot):
    train_data[0].append([[],[],[],[]])
    train_data[1].append(one_hot)
    # RGB
    image_pixels_rgb = misc.imread(path)
    image_pixels_rgb = np.reshape(image_pixels_rgb.astype(np.float32), [-1,3]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_rgb, op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for pixel_group in image_pixels_rgb:
        train_data[0][len(train_data[0]) - 1][0].append(pixel_group[0])
        train_data[0][len(train_data[0]) - 1][1].append(pixel_group[1])
        train_data[0][len(train_data[0]) - 1][2].append(pixel_group[2])
    # Grey
    image_pixels = misc.imread(path, "L")
    image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_grey, op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for pixel_group in image_pixels_grey:        
        train_data[0][len(train_data[0]) - 1][3].append(pixel_group[0])
        
def LoadPathToTrain_RGB(path, one_hot):
    train_data[0].append([[],[],[]])
    train_data[1].append(one_hot)
    # RGB
    image_pixels_rgb = misc.imread(path)
    image_pixels_rgb = np.reshape(image_pixels_rgb.astype(np.float32), [-1,3]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_rgb, op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for pixel_group in image_pixels_rgb:
        train_data[0][len(train_data[0]) - 1][0].append(pixel_group[0])
        train_data[0][len(train_data[0]) - 1][1].append(pixel_group[1])
        train_data[0][len(train_data[0]) - 1][2].append(pixel_group[2])

def LoadPathToTrain_GreyScale(path, one_hot):
    train_data[0].append([[]])
    train_data[1].append(one_hot)
    # Grey
    image_pixels = misc.imread(path, "L")
    image_pixels_grey = np.reshape(image_pixels, [-1,1]) # 1 for grey, 3 for RGB
    for pixel in np.nditer(image_pixels_grey, op_flags=['readwrite']):
        pixel[...] = float(pixel) / 255.0
    for pixel_group in image_pixels_grey:        
        train_data[0][len(train_data[0]) - 1][0].append(pixel_group[0])

def LoadPathToTrain_Canny(path, one_hot):
    train_data[0].append([[]])
    train_data[1].append(one_hot)
#Canny
    edge_pixels = feature.canny(image_pixels, sigma=3)
    edge_pixels = np.reshape(edge_pixels.astype(np.float32), [-1,1]) 
    # for pixel in np.nditer(edge_pixels, op_flags=['readwrite']):
        # pixel[...] = float(pixel) / 255.0
    for pixel_group in edge_pixels:
        train_data[0][len(train_data[0]) - 1][0].append(pixel_group[0])        
        
def getSelectionOfSize(n=50, type=''):
    if type is 'train':
        return randomizeBatchArray(n, train_data)
    if type is 'valid':
        return randomizeBatchArray(n, valid_data)
    if type is 'test':
        return randomizeBatchArray(n, test_data)
        
def getSelectionOfSize_TrainDirectory(n=50):
    global train_data
    train_data = [[],[]]
    fillTrainWithRandom(n)
    return randomizeBatchArray(n, train_data)

def fillTrainWithRandom(n):
    global train_data_paths
    paths_copy = copy.deepcopy(train_data_paths)
    for i in range(n):
        index = random.randint(0, len(paths_copy[0])-1)
        path = paths_copy[0][index]
        # print(path)
        # print(len(paths_copy[0]))
        # print(len(train_data_paths[0]))
        one_hot = paths_copy[1][index]
        removal_index = paths_copy[0].index(path) - 1
        # print(removal_index)
        del paths_copy[0][removal_index]
        del paths_copy[1][removal_index]
        
        global color_setting
        if color_setting == 0:
            LoadPathToTrain_GreyScale(path, one_hot)
        elif color_setting == 1:
            LoadPathToTrain_Canny(path, one_hot)
        elif color_setting == 3:
            LoadPathToTrain_RGB(path, one_hot)
        elif color_setting == 4:
            LoadPathToTrain_RGB_GreyScale(path, one_hot)
        elif color_setting == 5:
            LoadPathToTrain_RGB_GreyScale_Canny(path, one_hot)
def randomizeBatchArray(n, base_array):
    global color_setting, class_number
    channels = 0
    if color_setting == 0:
        channels = 1
    elif color_setting == 1:
        channels = 1
    elif color_setting == 3:
        channels = 3
    elif color_setting == 4:
        channels = 4
    elif color_setting == 5:
        channels = 5
    n_max = n
    return_arr = (np.zeros(shape=(n, channels, len(base_array[0][0][0])),
                dtype=np.float32), np.zeros(shape=(n,class_number), dtype=np.uint8))
    random_indices = np.arange(len(base_array[0]))
    np.random.shuffle(random_indices)
    for index in random_indices:
        if n == 1:
            return return_arr
        for color in range(channels):
            return_arr[0][n - 1][color] = np.asarray(base_array[0][index][color])
        return_arr[1][n - 1] = base_array[1][index]
        n = n - 1

def saveToPickle(path):
    #implement saving class number and using it in CNN

    print('Saving dataset...')
    global train_data, valid_data, test_data, color_setting    
    
    print("\tWritting train file...")
    dataset_bin_train = open(path + "train.pickle", 'wb')
    pickle.dump(train_data,dataset_bin_train)
    dataset_bin_train.close()
    train_data = 0
    print("\tTrain Added...")
    
    print("\tWritting valid file...")
    dataset_bin_valid = open(path + "valid.pickle", 'wb')
    pickle.dump(valid_data,dataset_bin_valid)
    dataset_bin_valid.close()
    valid_data = 0
    print("\tValid Added...")
    
    print("\tWritting test file...")
    dataset_bin_test = open(path + "test.pickle", 'wb')
    pickle.dump(test_data,dataset_bin_test)
    dataset_bin_test.close()
    test_data = 0
    print("\tTest Added...")
    
    print("\tWritting color file...")
    dataset_bin_color = open(path + "color.pickle", 'wb')
    pickle.dump(color_setting,dataset_bin_color)
    dataset_bin_color.close()
    color_setting = 0
    print("\tColor Added...")
    
    print("Dataset saved...")
    loadFromPickle(path)

def loadFromPickle(path):
    #implement loading class number and using it in CNN

    print('Loading dataset...')
    global train_data, valid_data, test_data, color_setting
    
    dataset_bin_train = open(path + "train.pickle", 'rb')
    train_data = pickle.load(dataset_bin_train)
    dataset_bin_train.close()
    print("\tTrain Added...")
    
    dataset_bin_valid = open(path + "valid.pickle", 'rb')
    valid_data = pickle.load(dataset_bin_valid)
    dataset_bin_valid.close()
    print("\tValid Added...")
    
    dataset_bin_test = open(path + "test.pickle", 'rb')
    test_data = pickle.load(dataset_bin_test)
    dataset_bin_test.close()
    print("\tTest Added...")
    
    dataset_bin_color = open(path + "color.pickle", 'rb')
    color_setting = pickle.load(dataset_bin_color)
    dataset_bin_color.close()
    print("\tColor set...")
    
    print("\tDataset loaded...")
