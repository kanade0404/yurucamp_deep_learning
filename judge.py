#!/usr/bin/env python

import glob
import os
import sys
import numpy as np
import tensorflow as tf
import cv2

path=os.getcwd()+'/analysis/'
file_list=os.listdir(path)

i = 0
label_name = []

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('label','label.txt','File name of label')

f = open(FLAGS.label,'r')
for line in f:
  line = line.rstrip()
  l = line.rstrip()
  label_name.append(l)
  i = i + 1

NUM_CLASSES = i
IMAGE_SIZE = 56
IMAGE_PIXELS = IMAGE_SIZE*IMAGE_SIZE*3

def inference(images_placeholder, keep_prob):

    def weight_variable(shape):
      initial = tf.truncated_normal(shape, stddev=0.1)
      return tf.Variable(initial)

    def bias_variable(shape):
      initial = tf.constant(0.1, shape=shape)
      return tf.Variable(initial)

    def conv2d(x, W):
      return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(x):
      return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                            strides=[1, 2, 2, 1], padding='SAME')

    x_image = tf.reshape(images_placeholder, [-1, 56, 56, 3])

    with tf.name_scope('conv1') as scope:
        W_conv1 = weight_variable([3, 3, 3, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    with tf.name_scope('pool1') as scope:
        h_pool1 = max_pool_2x2(h_conv1)

    with tf.name_scope('conv2') as scope:
        W_conv2 = weight_variable([3, 3, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    with tf.name_scope('pool2') as scope:
        h_pool2 = max_pool_2x2(h_conv2)

    with tf.name_scope('conv3') as scope:
        W_conv3 = weight_variable([3, 3, 64, 128])
        b_conv3 = bias_variable([128])
        h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)

    with tf.name_scope('pool3') as scope:
        h_pool3 = max_pool_2x2(h_conv3)

    with tf.name_scope('fc1') as scope:
        W_fc1 = weight_variable([7*7*128, 1024])
        b_fc1 = bias_variable([1024])
        h_pool3_flat = tf.reshape(h_pool3, [-1, 7*7*128])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool3_flat, W_fc1) + b_fc1)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('fc2') as scope:
        W_fc2 = weight_variable([1024, NUM_CLASSES])
        b_fc2 = bias_variable([NUM_CLASSES])

    with tf.name_scope('softmax') as scope:
        y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    return y_conv

if __name__ == '__main__':
    test_image = []
    test_filenm = []

    for file in file_list:
        test_filenm.append(file)

        img = cv2.imread('./analysis/' + file )
        img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
        test_image.append(img.flatten().astype(np.float32)/255.0)

    test_image = np.asarray(test_image)

    images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
    labels_placeholder = tf.placeholder("float", shape=(None, NUM_CLASSES))
    keep_prob = tf.placeholder("float")

    logits = inference(images_placeholder, keep_prob)
    sess = tf.InteractiveSession()

    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, "./model.ckpt")

    for i in range(len(test_image)):
        accr = logits.eval(feed_dict={
            images_placeholder: [test_image[i]],
            keep_prob: 1.0 })[0]
        pred = np.argmax(logits.eval(feed_dict={
            images_placeholder: [test_image[i]],
            keep_prob: 1.0 })[0])

        pred_label = label_name[pred]
#        print (pred,accr)
        print (test_filenm[i],' , ',pred_label)
