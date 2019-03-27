#!/bin/sh
# Script to execute Smart3seq read counting
set -e

echo "Executing Smart3seq read counting"
cd /usr/local/3SEQtools
Rscript make_expression_table.R --no-rlog /data/genome/hg38/gencode.v25.annotation.gtf /data/smart3seq/tophat_out/*bam
