#!/bin/bash
set -ex

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export INPUT_DIR=$1
export OUTPUT_DIR=$2
export EXECUTION_DATE=$3
echo "THIS_DIR=$THIS_DIR"
echo "INPUT_DIR=$INPUT_DIR"
echo "OUTPUT_DIR=$OUTPUT_DIR"
echo "EXECUTION_DATE=$EXECUTION_DATE"

# location of kubectl
envsubst < ${THIS_DIR}/k8s_job.yml > /tmp/k8s_job_2020.yml
kubectl create -f /tmp/k8s_job_2020.yml
