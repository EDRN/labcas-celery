#!/bin/bash
# Script to run htseq_count on the output produced by Tophat

GTF=$RNASEQ_DATA_DIR/gencode.vM20.annotation.gtf
cd $RNASEQ_DATA_DIR/test_data/tophat_out
htseq-count -r pos -f bam -m intersection-strict accepted_hits.bam $GTF > htseq_count.txt
