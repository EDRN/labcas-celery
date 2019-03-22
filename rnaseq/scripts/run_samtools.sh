#!/bin/bash
# Script to run Samtools to index bam files produced by Tophat

cd $RNASEQ_DATA_DIR/test_data/tophat_out
samtools index accepted_hits.bam
