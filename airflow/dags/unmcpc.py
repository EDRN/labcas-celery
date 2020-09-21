from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta
import logging
import sys
from airflow.models import Variable

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

aws_profile = Variable.get("aws_profile", default_var="default")
logging.info("Using aws_profile=%s" % aws_profile)

LOCAL_DIR = "/efs-ecs/docker/labcas/unmcpc"
input_dir = LOCAL_DIR + "/input_data/{{ params.execution_date }}"
output_dir = LOCAL_DIR + "/output_data/{{ params.execution_date }}" 
execution_date = "{{ params.execution_date }}"

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 9, 14),
    'email': ['luca.cinquini@jpl.nasa.gov'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

# execution date as YYYY-MM-DD
date = "{{ ds }}"
# execution date in ISO format
# date = "{{ ts }}"

dag = DAG("unmcpc", 
          schedule_interval="@once",
          default_args=default_args)

# Downloads data from S3 to local disk
# Uses S3 input folder from dag run configuration
t1 = BashOperator(
    task_id='download_data_from_s3',
    bash_command=("aws s3 sync {{ params.input }} %s "
                  "--profile {{ var.value.aws_profile }}" % input_dir),
    dag=dag)

# Executes the bash script to submit a Kubernetes batch job
# The script uses the input and output folders retrieved from the environment
t2 = BashOperator(
    task_id='submit_k8s_job',
    #environment={
    #     "INPUT_DATA": "/efs-ecs/docker/labcas/unmcpc/input_data/{{ params.execution_date }}",
    #     "OUTPUT_DATA": "/efs-ecs/docker/labcas/unmcpc/output_data/{{ params.execution_date }}",
    #     "EXECUTION_DATE": "{{ params.execution_date }}" 
    #},
    # IMPORTANT: must have space after the .sh!
    #bash_command='{{ var.value.k8s_home }}/submit_k8s_job.sh ',
    bash_command="{{ var.value.k8s_home }}/submit_k8s_job.sh %s %s %s " % (input_dir, output_dir, execution_date),
    dag=dag)

'''
t2_ = DockerOperator(
                task_id='helloworld_from_docker',
                image='centos:7',
                api_version='auto',
                auto_remove=True,
                tty=True,
                environment={
                        'HELLO_HOME': "/hello",
                },
                volumes=['/efs-ecs/docker/labcas/unmcpc/input_data/2020/:/input_data/2020',
                         '/efs-ecs/docker/labcas/unmcpc/output_data/:/output_data'],
                #command="bash -c 'for i in {1..5}; do echo hi; sleep 2; done'",
                command='cp -R /input_data/2020 /output_data/.',
                docker_url='unix://var/run/docker.sock',
                network_mode='bridge',
                default_args=default_args,
                dag=dag
        )
'''

# Uploads data from local disk to S3
# Uses S3 output folder from dag run configuration
t3 = BashOperator(
       task_id='upload_data_to_s3',
       bash_command=('aws s3 sync'
                     ' /efs-ecs/docker/labcas/unmcpc/output_data/2020'
                     #' {{ dag_run.conf["output"] }}'
                     ' {{ params.output }}'
                     ' --profile {{ var.value.aws_profile }}')
      )

t1 >> t2 

