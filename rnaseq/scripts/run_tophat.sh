#!/bin/bash
# Script to run tophat on some test data

set -e

# Test data must be already downloaded to the directory $RNASEQ_DATA_DIR/test_data
cd $RNASEQ_DATA_DIR/test_data

# tophat requires Python 2.7
source activate py27

# execute tophat
tophat -r 20 test_ref reads_1.fq reads_2.fq
