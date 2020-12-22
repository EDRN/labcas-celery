from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta
import logging
import sys
import time
from airflow.models import Variable
from kubernetes import client, config

# general DAG setup
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

aws_profile = Variable.get("aws_profile", default_var="default")
logging.info("Using aws_profile=%s" % aws_profile)

config.load_kube_config()

# execution date as YYYY-MM-DD
# date = "{{ ds }}"
# execution date in ISO format
# date = "{{ ts }}"
AIRFLOW_DATA_DIR = "/efs-ecs/docker/labcas/airflow/"
#AIRFLOW_DATA_DIR = '{{ var.value.AIRFLOW_DATA_DIR }}'

# execution date from task parameters or dag configuration
#exec_date = "{{ params.exec_date }}"
# example: 20180101T000000
exec_date = "{{ ts_nodash }}"

# s3://edrn-labcas/sftp_data/UNMCPC/UNMCPC.LIV.3rf77.small.experiment.1/input
input_bucket = "{{ params.input }}"
# s3://edrn-labcas/sftp_data/UNMCPC/UNMCPC.LIV.3rf77.small.experiment.1/output
output_bucket = "{{ params.output }}/%s" % exec_date

# remove "s3://edrn-labcas/sftp_data/
# TODO: 
# input_dir = AIRFLOW_DATA_DIR + <experiment_name> + "/input"
# outpur_dir = AIRFLOW_DATA_DIR + <experiment_name> + "/output" + exec_date
input_dir = AIRFLOW_DATA_DIR + ("%s" % exec_date) + "/input"
output_dir = AIRFLOW_DATA_DIR + ("%s" % exec_date) + "/output"

# default arguments passed to each task
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2020-10-01',
    'email': ['luca.cinquini@jpl.nasa.gov'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'catchup': False,
    #'retry_delay': timedelta(minutes=1),
    'execution_timeout': timedelta(minutes=120),
    # schedule maually only
    'schedule_interval': None
}

# the DAG
dag = DAG("unmcpc", 
          default_args=default_args)

# Creates input and output local directories
t0 = BashOperator(
    task_id='create_io_dirs',
    bash_command=("mkdir -p %s %s " % (input_dir, output_dir)),
    dag=dag)

# Downloads data from S3 to local disk
t1 = BashOperator(
    task_id='download_data_from_s3',
    bash_command=("aws s3 sync %s %s --profile {{ var.value.aws_profile }}" % (
                  input_bucket, input_dir)),
    dag=dag)

# Executes the bash script to submit a Kubernetes batch job
# Note: must have a blank space at the end of bash_command if it is a script (with arguments)
t2 = BashOperator(
    task_id='submit_k8s_job',
    # IMPORTANT: must have space after the .sh!
    bash_command="{{ var.value.k8s_home }}/submit_k8s_job.sh %s %s %s " % (input_dir, output_dir, exec_date),
    xcom_push=True,
    dag=dag)

# Monitor the K8s job by executing a script that uses the Python Kubernetes client
# Note: the same code executed via a Python operator tends to looses its authorization...
commands = """
source activate airflow
python -u {{ var.value.k8s_home }}/monitor_k8s_job.py %s
""" % exec_date

t3 = BashOperator(
    task_id='monitor_k8s_job',
    # IMPORTANT: must have space after the .sh!
    bash_command=commands,
    xcom_push=True,
    dag=dag)

# Uploads data from local disk to S3
t4 = BashOperator(
       task_id='upload_data_to_s3',
       bash_command=("aws s3 sync %s %s --profile {{ var.value.aws_profile }} " % (
                     output_dir, output_bucket)),
       dag=dag
      )

t0 >> t1 >> t2 >> t3 >> t4 

