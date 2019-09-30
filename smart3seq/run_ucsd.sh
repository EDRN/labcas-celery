#!/bin/bash
# Runs a Smart-3Seq pipeline for a specific set of samples

CONFIG_FILE=/usr/local/edrn/src/labcas-celery/smart3seq/config-ucsd.yaml
PROJECT_DIR=/efs/docker/labcas/mcl/archive/Smart-3Seq/UCSD

docker run -itd -v $CONFIG_FILE:/usr/local/SMART-3SEQ-smk/code/config.yaml\
                -v /efs/docker/labcas/smart3seq/star_ref:/star_ref\
                -v $PROJECT_DIR:/project\
                edrn/labcas-smart3seq:latest sh -c "source activate smart-3seq && snakemake --snakefile pipeline.smk --configfile config.yaml -j 4"
