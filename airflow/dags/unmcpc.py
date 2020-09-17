from airflow import DAG
from airflow.operators import BashOperator, PythonOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta
import logging
import sys
from airflow.models import Variable

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

aws_profile = Variable.get("saml_profile", default_var="default")
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

t2 = BashOperator(
    task_id='download_data_from_s3',
    bash_command=('aws s3 sync'
                  ' {{ dag_run.conf["input"] }}'
                  ' /tmp/UNMCPC/Liver/UNMCPC.Liver86rf3504/'
                  ' --profile {{ var.value.saml_profile }}'),
    dag=dag)

