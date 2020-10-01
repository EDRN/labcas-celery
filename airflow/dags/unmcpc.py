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
LOCAL_DIR = "/efs-ecs/docker/labcas/unmcpc/"

input_bucket = "{{ params.input }}"
output_bucket = "{{ params.output }}"

# execution date from task parameters or dag configuration
exec_date = "{{ params.exec_date }}"
# execution date as YYYY-MM-DD
# xdate = "{{ ds }}"
# execution date in ISO format
#exec_date = "{{ ts }}"
input_dir = LOCAL_DIR + exec_date + "/input_data"
output_dir = LOCAL_DIR + exec_date + "/output_data"

# Following are defaults which can be overridden later on
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
    'execution_timeout': timedelta(minutes=60),
    #'schedule_interval': '@once'
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
t2 = BashOperator(
    task_id='submit_k8s_job',
    # IMPORTANT: must have space after the .sh!
    bash_command="{{ var.value.k8s_home }}/submit_k8s_job.sh %s %s %s " % (input_dir, output_dir, exec_date),
    dag=dag)

def monitor_k8s_job(exec_date):
    '''Function to monitor a Kubernets job with a specific
       value of the exec_date label.'''

    v1 = client.BatchV1Api()
    while True:
       jobs = v1.list_namespaced_job(namespace='default', watch=False, label_selector='exec_date=%s' % exec_date)
       if jobs.items:
          for job in jobs.items:
             npa = job.status.active
             npf = job.status.failed
             nps = job.status.succeeded
             logging.info("Number of pods active, failed, succeded: %s, %s, %s" % (npa, npf, nps))
             if nps and int(nps)==1:
                logging.info("Pod succeeded, returning")
                return 
             elif npf and int(npf)==1:
                raise AirflowFailException("Job failed!")
             elif npa and int(npa)==1:
                logging.info("Waiting for pod to stop running...")
                time.sleep(10)
             else:
                raise AirflowFailException("Cannot monitor jobs reliably, exiting!")
       else:
           raise AirflowFailException("Cannot find any job matching label: exec_date=%s" % exec_date)
    

t3 = PythonOperator(
        task_id='monitor_k8s_job',
        python_callable=monitor_k8s_job,
        op_kwargs={'exec_date': exec_date},
        dag=dag)

# Uploads data from local disk to S3
t4 = BashOperator(
       task_id='upload_data_to_s3',
       bash_command=("aws s3 sync %s %s --profile {{ var.value.aws_profile }} " % (
                     output_dir, output_bucket)),
       dag=dag
      )

t0 >> t1 >> t2 >> t3 >> t4 

