#!/bin/sh
# Script to download the initial Tensorflow data 
# to the directory $TENSORFLOW_DATA
#

set -ex

if [ ! "$TENSORFLOW_DATA" ]; then
    echo "TENSORFLOW_DATA is NOT set"
    exit
else
    echo "Using TENSORFLOW_DATA=$TENSORFLOW_DATA"
fi

mkdir -p $TENSORFLOW_DATA
cd $TENSORFLOW_DATA

for file in "t10k-labels-idx1-ubyte.gz" "t10k-images-idx3-ubyte.gz" "train-labels-idx1-ubyte.gz" "train-images-idx3-ubyte.gz"
do
	if [ ! -f ${file} ]; then
		echo "Downlaoding ${file}"
		wget "http://yann.lecun.com/exdb/mnist/${file}"
fi
done