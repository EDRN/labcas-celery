#!/bin/sh
# Script to download the initial Tensorflow data 
# to the directory $TENSORFLOW_DATA
#
if [ ! "$TENSORFLOW_DATA" ]; then
    echo "TENSORFLOW_DATA is NOT set"
    exit
else
    echo "Using TENSORFLOW_DATA=$TENSORFLOW_DATA"
fi

mkdir -p $TENSORFLOW_DATA
cd $TENSORFLOW_DATA
wget "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"
wget "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"
wget "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"
wget "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
