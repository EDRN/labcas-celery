# ==============================================================================
# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
A very simple MNIST classifier.

See extensive documentation at
https://www.tensorflow.org/get_started/mnist/beginners
"""


import argparse
import sys
import time
import os
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

from labcas.celery.worker import app

@app.task
def tensorflow_task(num_images=1000, data_dir='/tmp/tensorflow/mnist/input_data', output_file='output.txt'):

  # Import data
  mnist = input_data.read_data_sets(data_dir, one_hot=True)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 784])
  W = tf.Variable(tf.zeros([784, 10]))
  b = tf.Variable(tf.zeros([10]))
  y = tf.matmul(x, W) + b

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 10])

  # The raw formulation of cross-entropy,
  #
  #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
  #                                 reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
  # outputs of 'y', and then average across the batch.
  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()
  # Train
  for _ in range(num_images):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

  # Test trained model
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  result = sess.run(accuracy, feed_dict={x: mnist.test.images,
                                         y_: mnist.test.labels})
  # Write result to file
  with open(output_file, "w") as file: 
    file.write(str(result))
    
  return str(result)
  
  # command line invocation program
if __name__ == '__main__':

    '''
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Tensorflow demo program")
    parser.add_argument('--num_images', type=int, help="Number of images", default=1000)
    parser.add_argument('--data_dir', type=str, help="Input data directory", default='/tmp/tensorflow/mnist/input_data')
    parser.add_argument('--output_dir', type=str, help="Output directory", default='/tmp')
    
    args_dict = vars(parser.parse_args())

    tensorflow_task.delay(num_images=args_dict['num_images'],
                          data_dir=args_dict['data_dir'],
                          output_file=args_dict['output_file'])
    '''
    
    # retrieve parameters from environment
    num_tasks = os.getenv('NUMBER_OF_TASKS', "10")
    num_images = os.getenv('NUMBER_OF_IMAGES', "100")
    output_dir = os.getenv('OUTPUT_DIR', '/tmp')
    
    # submit N tasks asynchronously
    from labcas.celery.tasks.tensorflow.task import tensorflow_task
    for i in range(int(num_tasks)):
        tensorflow_task.delay(num_images=int(num_images), output_file="%s/output_%s.txt" % (output_dir, i))
        
    # sleep indefinitely to keep program running
    while True:
        print("Sleeping...")
        time.sleep(10)
        