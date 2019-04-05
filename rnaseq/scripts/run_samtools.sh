#!/bin/bash
# Script to run Samtools to index bam files produced by Tophat

set -e

# specific run to be processed
run=$1
echo "Executing Samtools for run: $run"

cd $RNASEQ_DATA_DIR/$run/tophat_out
samtools index accepted_hits.bam
