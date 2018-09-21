from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import os
import time
import sys
sys.path.insert(0, 'includes/')
import dataget
import model
import modelstore
import visualizations
import datetime

#static param
channels = 3
classes = 14
dimension_x = 100
dimension_y = 100

retrain = input("1 to retrain: ")
meta = ""
if retrain == "1":
    meta = input("Enter file(no extension): ")
if channels is 5:
    dataget.loadPartialToMemory_RGB_Greyscale_Canny(classes)
    channels = 5
if channels is 4:
    dataget.loadPartialToMemory_RGB_Greyscale(classes)
    channels = 4
if channels is 3:
    dataget.loadPartialToMemory_RGB(classes) 
    channels = 3
if channels is 1:
    dataget.loadPartialToMemory_Canny(classes)
    channels = 1    
if channels is 0:
    dataget.loadPartialToMemory_Greyscale(classes)
    channels = 1
   

save_threashold = 0.35
while True:
    #hyperparam
    iterations = 100000
    loss_steps = 1e-5
    batch_size = 500
    batch_growth = 1
    batch_accel = 1
    batch_cutoff = len(dataget.train_data_paths[0])
    batch_gain_level = 1
    batch_gain_counter = batch_gain_level 
    base_complementary_dropout = 0.75 #lower means more dropout
    convolution_complementary_dropout = 0.9
    cutoff_threashold = loss_steps / 10
    eval_rate = 100
 
    file_name = "models/save"  + str(int(time.time())) + ".mod"
    
    #input("enter to start")
    perf = open('performance.txt', 'a+')
    perf.write('----' + str(datetime.datetime.now()) + '----\n\n')
    perf.write('    Itterations ' + str(iterations)  +'\n')
    perf.write('    color_setting ' + str(dataget.color_setting) + '\n')
    perf.write('    loss_steps ' + str(loss_steps) + '\n')
    perf.write('    base_complementary_dropout ' + str(base_complementary_dropout) + '\n')
    perf.write('    convolution_complementary_dropout ' + str(convolution_complementary_dropout) + '\n')
    perf.write('    eval_rate ' + str(eval_rate) + '\n')
    perf.write('    batch_size ' + str(batch_size) + '\n')
    perf.write('    batch_growth ' + str(batch_growth) + '\n')
    perf.write('    batch_accel ' + str(batch_accel) + '\n')
    perf.write('    train size: ' + str(batch_cutoff) + '\n')
    perf.write('    save_threashold ' + str(save_threashold) + '\n')
    # perf.write('    Canny sigma ' + str(0.5) + '\n')
    
    if retrain != "1":
        perf.write('    File: ' + str(file_name) + '\n')
    else:
        perf.write('    File: ' + str(meta) + '\n')
    perf.write('\n')
    perf.close()

    
    training_data = tf.placeholder(tf.float32,[None,channels, dimension_x * dimension_y], name='train-data')
    training_labels = tf.placeholder(tf.float32,[None, classes], name='train-labels')  #none = dynamic sizing
    training_labels_evaluated,  base_keep_prob, convolution_keep_prob = model.cnnModel(training_data, channels, classes, dimension_x, dimension_y) 

    with tf.name_scope('training'):
        loss_function = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=training_labels,logits=training_labels_evaluated))
        train_function = tf.train.AdamOptimizer(loss_steps).minimize(loss_function)
        
        #https://gist.github.com/sbrodehl/2120a95d57963a289cc23bcfb24bee1b
        # to get the mean accuracy over all labels, prediction_tensor are scaled logits (i.e. with final sigmoid layer)
        correct_prediction = tf.equal(tf.round(tf.nn.sigmoid(training_labels_evaluated)), tf.round(training_labels))
        accuracy2 = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        # to get the mean accuracy where all labels need to be correct
        all_labels_true = tf.reduce_min((tf.cast(correct_prediction, tf.float32)), 1)
        accuracy1 = tf.reduce_mean(all_labels_true)
        
        #confusion mat for multilables?
        #confusion_mat = tf.confusion_matrix(labels=training_labels, predictions=training_labels_evaluated, num_classes=classes)
    
    old_validation_score = 0
    greatest_validation = 0.0
    visualizations.init("graphs/")
    sess = tf.Session()
    
    if retrain == "1":
        modelstore.modInit('models/retrain-' + meta)
        modelstore.loadModel(sess, 'models/',  meta + ".meta")
        print("Retraining...")
        perf = open('performance.txt', 'a')
        perf.write('    Retrain...\n')
        perf.close()
    else:
        modelstore.modInit("models/save"  + str(int(time.time())) + ".mod")
        # visualizations.ioSummary(training_labels, training_labels_evaluated)
        sess.run(tf.global_variables_initializer())
    with sess.as_default():
        train_sum = 0
        for i in range(iterations):
            batch = dataget.getSelectionOfSize_TrainDirectory(batch_size)
            # visualizations.imageSummary(batch, channels);
            if i % eval_rate == 0:
                valid_accuracy, valid_accuracy2 = sess.run([accuracy1, accuracy2], feed_dict={
                    training_data: dataget.valid_data[0], convolution_keep_prob: 1.0,
                    training_labels: dataget.valid_data[1], base_keep_prob: 1.0})
                print('step %d, validation accuracy %g - %g' % (i, valid_accuracy, valid_accuracy2))
                train_sum = train_sum + accuracy1.eval(feed_dict={
                    training_data: batch[0], convolution_keep_prob: convolution_complementary_dropout,
                    training_labels: batch[1], base_keep_prob: base_complementary_dropout})
                print('step %d, train accuracy %g' % (i, train_sum / (eval_rate / 5 + 1)))
                if (valid_accuracy - old_validation_score) < cutoff_threashold:
                    batch_gain_counter = batch_gain_counter - 1
                    perf = open('performance.txt', 'a')
                    perf.write('    itteration ' + str(i) + '\n')
                    perf.write('    batch_size/batch_gain_counter ' + str(batch_size) + '/' + str(batch_gain_counter) + '====\n')
                    perf.write('    validation ' + str(valid_accuracy) + ' - ' + str(valid_accuracy2) + ' ====\n')
                    perf.write('    Training ' + str(train_sum / (eval_rate / 5 + 1)) + ' ====\n')
                    perf.write('    Saturation ' + str(batch_size/batch_cutoff) + '====\n\n')
                    perf.close()
                    if batch_gain_counter <= 0:
                        batch_gain_counter = batch_gain_level
                        if (batch_size + batch_growth) <= batch_cutoff:
                                batch_size = batch_size + batch_growth #https://arxiv.org/abs/1711.00489
                                batch_growth = batch_growth + batch_accel
                old_validation_score = valid_accuracy
                if valid_accuracy > greatest_validation:
                    print('New accuracy record...')
                    batch_gain_counter = batch_gain_level
                    visualizations.log('performance.txt', i, valid_accuracy, valid_accuracy2, train_sum / (eval_rate / 5 + 1))
                    # visualizations.accuracySummary(i, valid_accuracy, train_accuracy)
                    greatest_validation = valid_accuracy
                    if valid_accuracy > save_threashold:
                        save_threashold = greatest_validation
                        modelstore.saveModel(sess)
                train_sum = 0
            if i % 5 == 0:    
                _, accuracy = sess.run([train_function, accuracy1], 
                    feed_dict={training_data: batch[0], convolution_keep_prob: convolution_complementary_dropout,
                    training_labels: batch[1], base_keep_prob: base_complementary_dropout})
                train_sum = train_sum + accuracy
                # visualizations.addSummary(summary, i)
                print(str(i) + " | " + str(train_sum / ((i % eval_rate) / 5 + 1))+ ' -- ' + str(accuracy)) 
            else:
                sess.run([train_function], feed_dict={training_data: batch[0], convolution_keep_prob: convolution_complementary_dropout,
                    training_labels: batch[1], base_keep_prob: base_complementary_dropout})
        
        
        
        valid_accuracy, valid_accuracy2 = sess.run([accuracy1, accuracy2], feed_dict={
                    training_data: dataget.valid_data[0], convolution_keep_prob: 1.0,
                    training_labels: dataget.valid_data[1], base_keep_prob: 1.0})
        print( str(int(time.time())) + ' ending...')
        print('step %d, validation accuracy %g - %g' % (iterations, valid_accuracy, valid_accuracy2))
        print('step %d, train accuracy %g' % (iterations, train_sum / (eval_rate / 5)))
        visualizations.log('performance.txt', iterations, valid_accuracy, valid_accuracy2, '-')
        final_path = "models/save-Final"  + str(int(time.time())) + ".mod"
        modelstore.saveModelNew(sess, final_path)

        
        
    perf = open('performance.txt', 'a')
    perf.write('    File ' + file_name + '====\n\n')
    perf.write('    FileFinal ' + final_path + '====\n\n')
    perf.write('    ====' + str(datetime.datetime.now()) + '====\n\n')
    perf.close()
    
    tf.reset_default_graph()
    
    training_data = None
    training_labels = None
    training_labels_evaluated, base_keep_prob = [None, None]
    loss_function = None
    train_function = None
    
    correct_prediction = None
    accuracy1 = None
    all_labels_true = None
    accuracy2 = None
    modelstore.reset()
    visualizations.reset()
    
    sess.close()
    
    break
    
exit()
#input('enter to finish')
