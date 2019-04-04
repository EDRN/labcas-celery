#!/bin/sh
# Script to execute Smart3seq read counting
set -e

run=$1
echo "Executing Smart3seq read counting for run: $run"

cd ${SMART3SEQ_DATA_DIR}/output/${run}
Rscript /usr/local/3SEQtools/make_expression_table.R --no-rlog ./hg38/gencode.v25.annotation.gtf ${SMART3SEQ_DATA_DIR}/output/${run}/*bam