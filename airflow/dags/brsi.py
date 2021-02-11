# Airflow DAG for BRSI Machine Learning
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

input_dir = "/efs-ecs/docker/labcas/Combined_Imaging_and_Blood_Biomarkers_for_Breast_Cancer_Diagnosis"
output_dir = "/efs-ecs/docker/labcas/Combined_Imaging_and_Blood_Biomarkers_for_Breast_Cancer_Diagnosis_Output"

# general DAG setup
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

aws_profile = Variable.get("aws_profile", default_var="default")
logging.info("Using aws_profile=%s" % aws_profile)

# This macro is not interpreted until the operator is instantiated,
# and it must be part of a templated field
#exec_date = "{{ ts_nodash }}"
#exec_date = "{{ params.exec_date }}"
exec_date = datetime.now().strftime("%Y%m%dT%H%M%S")
logging.info("exec_date="+exec_date)

# DAG run parameters
image_path = "{{ params.image_path }}"

# DAG default arguments
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

dag = DAG('brsi', default_args=default_args)

input_volume = Volume(
    name="inputdata",
    configs={"hostPath": {"path":input_dir, "type":"Directory"}}
)

input_volume_mount = VolumeMount(
    "inputdata",
    mount_path="/data/BRSI",
    sub_path=None,
    read_only=True
)

output_volume = Volume(
    name="outputdata",
    configs={"hostPath": {"path":output_dir, "type":"Directory"}}
)

output_volume_mount = VolumeMount(
    "outputdata",
    mount_path="/usr/local/src/PenRad_Single_View_Detection_Demo/Test_output/single_view/0.3",
    sub_path=None,
    read_only=False
)

# Runs the Docker container into the K8s cluster
# Note: these are the templated_fields for KubernetesPodOperator: 
# template_fields = ('cmds', 'arguments', 'env_vars', 'config_file')
kpot = KubernetesPodOperator(
                          namespace='default',
                          #image="edrn/tensorflow-brsi",
                          image="300153749881.dkr.ecr.us-west-2.amazonaws.com/tensorflow-brsi",
                          #cmds=["python","-c"],
                          arguments=[f"{image_path}"],
                          labels={
                             "exec_date": exec_date,
                             "app": "labcas-brsi-ml"
                          },
                          name="tensorflow-brsi",
                          task_id="tensorflow-brsi-task",
                          in_cluster=False,
                          do_xcom_push=False,
                          get_logs=True,
                          startup_timeout_seconds=300,
                          resources={
                             'request_memory': '10Gi',
                             'request_cpu': 1,
                             'limit_memory': '10Gi',
                             'limit_cpu': 1
                          },
                          #env_vars={
                          #  "FOO": "bar"
                          #},
                          #image_pull_secrets="service-user-for-pull",
                          volumes=[input_volume, output_volume],
                          volume_mounts=[input_volume_mount, output_volume_mount],
                          dag=dag
                          )

# to be used by DebugExecutor
if __name__ == '__main__':
  dag.clear(reset_dag_runs=True)
  dag.run()


