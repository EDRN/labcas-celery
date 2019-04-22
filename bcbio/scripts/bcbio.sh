#!/bin/sh
# script to run bcbio 'cancer-dream-syn3' workflow
set -e

cd /efs-ecs/docker/bcbio/projects/cancer-dream-syn3/work
bcbio_nextgen.py ../config/cancer-dream-syn3.yaml -n 8
