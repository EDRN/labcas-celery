# Airflow DAG for UNMCPC image registration
# using the KubernetesPodOperator

from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable
import logging
import sys

AIRFLOW_DATA_DIR = "/efs-ecs/docker/labcas/airflow/"
#INPUT_DIR = "/efs-ecs/docker/labcas/airflow/20201202T004851/input"
#OUTPUT_DIR = "/efs-ecs/docker/labcas/airflow/20201202T004851/output2"

# general DAG setup
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

aws_profile = Variable.get("aws_profile", default_var="default")
logging.info("Using aws_profile=%s" % aws_profile)

exec_date = "{{ ts_nodash }}"
# FIXME
exec_date = "20201223T110652"

# s3://edrn-labcas/sftp_data/UNMCPC/UNMCPC.LIV.3rf77.small.experiment.1/input
input_bucket = "{{ params.input }}"
# s3://edrn-labcas/sftp_data/UNMCPC/UNMCPC.LIV.3rf77.small.experiment.1/output
output_bucket = "{{ params.output }}/%s" % exec_date

input_dir = AIRFLOW_DATA_DIR + ("%s" % exec_date) + "/input"
output_dir = AIRFLOW_DATA_DIR + ("%s" % exec_date) + "/output"


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2020-12-21',
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'catchup': False,
    'execution_timeout': timedelta(minutes=120),
    'schedule_interval': None
    #'retry_delay': timedelta(minutes=5)
}

dag = DAG('kubernetes_pod_operator_test', default_args=default_args)

input_volume = Volume(
    name="inputdata",
    configs={"hostPath": {"path":input_dir, "type":"Directory"}}
)

input_volume_mount = VolumeMount(
    "inputdata",
    mount_path="/usr/src/app/input",
    sub_path=None,
    read_only=True
)

output_volume = Volume(
    name="outputdata",
    configs={"hostPath": {"path":output_dir, "type":"Directory"}}
)

output_volume_mount = VolumeMount(
    "outputdata",
    mount_path="/usr/src/app/output",
    sub_path=None,
    read_only=False
)

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

# Runs the Docker container into the K8s cluster
t2 = KubernetesPodOperator(
                          namespace='default',
                          image="edrn/reg_mult",
                          #cmds=["python","-c"],
                          #arguments=["print('hello world')"],
                          labels={
                             "exec_date": exec_date,
                             "app": "labcas-unmcpc"
                          },
                          name="regmulti",
                          task_id="regmulti-task",
                          in_cluster=False,
                          do_xcom_push=False,
                          get_logs=True,
                          startup_timeout_seconds=300,
                          resources={
                             'request_memory': '60Gi',
                             'request_cpu': 4,
                             'limit_memory': '60Gi',
                             'limit_cpu': 4
                          },
                          #env_vars={
                          #  "FOO": "bar"
                          #},
                          #image_pull_secrets="service-user-for-pull",
                          volumes=[input_volume, output_volume],
                          volume_mounts=[input_volume_mount, output_volume_mount],
                          dag=dag
                          )

# Uploads data from local disk to S3
t3 = BashOperator(
       task_id='upload_data_to_s3',
       bash_command=("aws s3 sync %s %s --profile {{ var.value.aws_profile }} " % (
                     output_dir, output_bucket)),
       dag=dag
      )

# Chain tasks
t0 >> t1 >> t2 >> t3 

# to be used by DebugExecutor
if __name__ == '__main__':
  dag.clear(reset_dag_runs=True)
  dag.run()


