import numpy as np
import tensorflow as tf
import os

saver = None
save_path = None

def reset():
    global saver,save_path
    saver = None
    save_path = None

def modInit(path):
    global saver,save_path
    saver = tf.train.Saver(save_relative_paths=True)
    save_path = path

def saveModel(session):
    global saver, save_path
    saved_location = saver.save(session, save_path)
    print('Session saved to %s' % (saved_location))
	
def saveModelNew(session, new_path):
    global saver, save_path
    saved_location = saver.save(session, new_path)
    print('Session saved to %s' % (saved_location))

def saveModelPath(session, path):
    global saver
    saved_location = saver.save(session, path)
    print('Session saved to %s' % (saved_location))
    
    
def loadModel(session, load_path, file):
    print(load_path + file)
    saver = tf.train.import_meta_graph(load_path + file)
    saver.restore(session, tf.train.latest_checkpoint(load_path))
    print('Session loaded from %s' % (load_path + file))
    
def loadMostRecentModel(session):
    global save_path
    directory = os.listdir(save_path)
    youngest_time = None
    youngest_file = ''
    for file in os.listdir(save_path):
        if file.find('meta') >= 0:
            if youngest_time is None:
                youngest_file = file
                youngest_time = os.path.getmtime(save_path + file)
            if youngest_time > os.path.getmtime(save_path + file):
                youngest_file = file
                youngest_time = os.path.getmtime(save_path + file)
    print (youngest_file)
    saver = tf.train.import_meta_graph(save_path + youngest_file)
    saver.restore(session, tf.train.latest_checkpoint(save_path))
    print('Session loaded from %s' % (save_path + youngest_file))
