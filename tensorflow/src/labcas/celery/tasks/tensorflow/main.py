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

from labcas.celery.tasks.tensorflow.task import tensorflow_task
import argparse
    
# command line invocation program
if __name__ == '__main__':

    '''
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Tensorflow demo program")
    parser.add_argument('--num_images', type=int, help="Number of images", default=1000)
    parser.add_argument('--data_dir', type=str, help="Input data directory", default='/tmp/tensorflow/mnist/input_data')
    parser.add_argument('--output_file', type=str, help="Output file path", default='output.txt')
    
    args_dict = vars(parser.parse_args())

    tensorflow_task.delay(num_images=args_dict['num_images'],
                          data_dir=args_dict['data_dir'],
                          output_file=args_dict['output_file'])
    '''
    
    # submit N tasks asynchronously
    for i in range(100):
        tensorflow_task.delay(num_images=100, output_file="/tmp/output_%s.txt" % i)