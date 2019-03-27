#!/bin/sh
# Script to execute Smart3seq alignment
set -e

echo "Executing Smart3seq alignment"
cd /usr/local/3SEQtools
align_smart-3seq.sh /data/smart3seq/genome/hg38/star/dbsnp147_gencode25-68 /data/smart3seq/data/*fastq.gz
