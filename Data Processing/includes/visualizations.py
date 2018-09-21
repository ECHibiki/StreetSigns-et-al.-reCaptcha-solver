import tensorflow as tf
import datetime

train_writer = None
merged_summary = None

def reset():
    global train_writer,merged_summary
    train_writer = None
    merged_summary = None

def log(path, itt, valid_accuracy, valid_accuracy2, train_accuracy):
    perf = open(path, 'a')
    perf.write(f'Itteration: {itt} -- ' + str(datetime.datetime.now()) + '\n')
    perf.write(f'V Accuracy: {valid_accuracy} - {valid_accuracy2} -- ' + str(datetime.datetime.now()) + '\n')
    perf.write(f'T Accuracy: {train_accuracy} -- ' + str(datetime.datetime.now()) + '\n')
    #perf.write(f'T Accuracy: {confusion_mat}\n')
    perf.write('\n')
    perf.close()
    
def addGraph():
    global train_writer
    train_writer.add_graph(tf.get_default_graph())

def addSummary(summary, itt):
    global train_writer
    train_writer.add_summary(summary, itt)

def ioSummary(input_labels, output_labels):
    tf.summary.histogram('input', input_labels)
    tf.summary.histogram('output', output_labels)

def accuracySummary(i, valid_accuracy, train_accuracy):
    tf.summary.histogram('valid_accuracy', valid_accuracy)
    tf.summary.histogram('valid_accuracy', train_accuracy)
    
def modelSummary(weight, bias, relu, pool):
    tf.summary.histogram('weight', weight)
    tf.summary.histogram('bias', bias)
    tf.summary.histogram('activation', relu)
    tf.summary.histogram('pool', pool)
    
def imageSummary(image_batch, channels):
        # print(image_batch)
        # if channels == 1:
            # tf.summary.image('images',tf.reshape(image_batch,max_outputs=channels);
        # elif channels == 3:
            # tf.summary.image('images',image_batch,max_outputs=channels);
        # elif channels == 5:
            # tf.summary.image('images',image_batch,max_outputs=channels);
        pass
    
def init(path):
    global train_writer,merged_summary
    merged_summary = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(path)
    addGraph()