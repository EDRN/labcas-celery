#!/bin/bash
# Script to run htseq_count on the output produced by Tophat

set -e

# specific run to be processed
run=$1
echo "Executing Htseq-count for run: $run"

GTF=$RNASEQ_DATA_DIR/gencode.vM20.annotation.gtf
cd $RNASEQ_DATA_DIR/$run/tophat_out
htseq-count -r pos -f bam -m intersection-strict accepted_hits.bam $GTF > htseq_count.txt
