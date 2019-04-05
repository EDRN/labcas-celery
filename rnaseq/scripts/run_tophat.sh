#!/bin/bash
# Script to run tophat on some test data

set -e

# specific run to be processed
run=$1
echo "Executing Tophat for run: $run"

# Test data must be already downloaded to the directory $RNASEQ_DATA_DIR/test_data
DATA_DIR=$RNASEQ_DATA_DIR/test_data

# working directory
RUN_DIR=$RNASEQ_DATA_DIR/output/$run
mkdir -p $RUN_DIR
cd $RUN_DIR

# tophat requires Python 2.7
source activate py27

# execute tophat
tophat -r 20 $DATA_DIR/test_ref $DATA_DIR/reads_1.fq $DATA_DIR/reads_2.fq
