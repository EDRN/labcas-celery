#!/bin/bash
# Script that submits a Kubernetes batch job to execute the image alignment
# The Kubernetes YAML file is parsed to replace the INPUT_DATA, OUTPUT_DATA placeholders
# with values from the environment
envsubst < ${AIRFLOW_HOME}/dags/k8s_job.yml > /tmp/k8s_job_2020.yml
kubectl create -f /tmp/k8s_job_2020.yml
