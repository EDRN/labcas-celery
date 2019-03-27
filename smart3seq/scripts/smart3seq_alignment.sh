#!/bin/sh
# Script to execute Smart3seq alignment
set -e

# specific run to be processed
run=$1
echo "Executing Smart3seq alignment for run: $run"

cd ${SMART3SEQ_DATA_DIR}/data/${run}
align_smart-3seq.sh ${SMART3SEQ_DATA_DIR}/genome/hg38/star/dbsnp147_gencode25-68 ${SMART3SEQ_DATA_DIR}/data/${run}/*fastq.gz
