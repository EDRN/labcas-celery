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

dag = DAG("unmcpc", 
          schedule_interval="@once",
          default_args=default_args)

# {{ ts }}: execution data in ISO format

t1 = BashOperator(
    task_id='download_data_from_s3',
    bash_command=('aws s3 sync'
                  ' {{ dag_run.conf["input"] }}'
                  ' /efs-ecs/docker/labcas/unmcpc/input_data/2020'
                  ' --profile {{ var.value.aws_profile }}'),
    dag=dag)

t2 = BashOperator(
    task_id='submit_k8s_job',
    environment={
                 "INPUT_DATA": "{{ params.input }}",
                 "OUTPUT_DATA": "{{ params.output }}" 
                },
    # IMPORTANT: must have space after the .sh!
    # bash_command='{{ dag_run.conf["dags_folder"] }}/submit_k8s_job.sh ',
    bash_command='{{ var.value.k8s_home }}/submit_k8s_job.sh ',
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

t3 = BashOperator(
       task_id='upload_data_to_s3',
       bash_command=('aws s3 sync'
                     ' /efs-ecs/docker/labcas/unmcpc/output_data/2020'
                     #' {{ dag_run.conf["output"] }}'
                     ' {{ params.output }}'
                     ' --profile {{ var.value.aws_profile }}'),
    dag=dag)

t1 >> t2 >> t3

