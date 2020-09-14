from airflow import DAG
from airflow.operators import BashOperator, PythonOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta
import boto3
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# instantiate S3 client
session = boto3.session.Session(profile_name='saml-pub')
s3 = session.resource('s3')

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 9, 14),
    'email': ['luca.cinquini@jpl.nasa.gov'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('UNMC_Image_Alignment', default_args=default_args)

# helper functions to download/upload data from/to S3
def download_from_S3(bucket=None, key=None, filepath=None):
    s3.Bucket(bucket).download_file(key, filepath)

def upload_file_to_S3(filename, key, bucket_name):
    s3.Bucket(bucket_name).upload_file(filename, key)



t1 = BashOperator(
    task_id='scale_nodes_up',
    bash_command='echo "Scale EKS nodes up"',
    dag=dag)

t2 = PythonOperator(
    task_id='download_data_from_s3',
    python_callable=download_from_S3,
    op_kwargs={
        'filepath': '/Users/cinquini/tmp/SAN_VM_SNAPSHOT.xls',
        'key': 'archive/Analysis_of_pancreatic_cancer_biomarkers_in_PLCO_set/Analysis_of_pancreatic_cancer_biomarkers_in_PLCO_set/SAN_VM_SNAPSHOT.xls',
        'bucket': 'edrn-labcas',
    },
    dag=dag)

# Note: on OSX must export TMPDIR to a path that Docker can mount (NOT /var/folders/tk...)
t3 = DockerOperator(
                task_id='helloworld_from_docker',
                image='centos:7',
                start_date = datetime.now(),
                api_version='auto',
                auto_remove=True,
                tty=True,
                environment={
                        'HELLO_HOME': "/hello",
                },
                volumes=['/Users/cinquini/tmp:/tmp'],
                command="bash -c 'for i in {1..10}; do echo hi; sleep 2; done'",
                docker_url='unix://var/run/docker.sock',
                network_mode='bridge'
        )


t4 = BashOperator(
    task_id='monitor_eks_job',
    bash_command='echo "Monitor batch job on EKS"',
    dag=dag)

t5 = BashOperator(
    task_id='upload_data_to_s3',
    bash_command='echo "Upload output data to S3"',
    dag=dag)

t6 = BashOperator(
    task_id='scale_nodes_down',
    bash_command='echo "Scale EKS nodes down"',
    dag=dag)

t7 = BashOperator(
    task_id='send_email',
    bash_command='echo "Send email"',
    dag=dag)

t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7
