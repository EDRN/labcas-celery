#!/bin/bash
# Script to download the data used by this workflow,
# if not existing already.

set -e

RNASEQ_DATA_DIR=${RNASEQ_DATA_DIR:-/tmp}
echo "Using RNASEQ_DATA_DIR=$RNASEQ_DATA_DIR"
mkdir -p $RNASEQ_DATA_DIR
cd $RNASEQ_DATA_DIR

# download test data
TEST_DATA=test_data.tar.gz 
if [ -f $TEST_DATA ]; then
   echo "File $TEST_DATA already exists"
else
   echo "File $TEST_DATA does not exist, downloading"
   curl -O https://ccb.jhu.edu/software/tophat/downloads/test_data.tar.gz
   tar xvfz test_data.tar.gz
fi

# download reference genome
GTF=gencode.vM20.annotation.gtf
if [ -f $GTF ]; then
   echo "File $GTF already exists"
else
   echo "File $GTF does not exist, downloading"
   curl -O ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M20/gencode.vM20.annotation.gtf.gz
   gunzip gencode.vM20.annotation.gtf.gz
fi
