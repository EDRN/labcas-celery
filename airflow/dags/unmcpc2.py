# Airflow DAG for UNMCPC image registration
# using the KubernetesPodOperator

from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount

AIRFLOW_DATA_DIR = "/efs-ecs/docker/labcas/airflow/"
INPUT_DIR = "/efs-ecs/docker/labcas/airflow/20201202T004851/input"
OUTPUT_DIR = "/efs-ecs/docker/labcas/airflow/20201202T004851/output2"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2020-12-21',
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'catchup': False,
    'schedule_interval': None
    #'retry_delay': timedelta(minutes=5)
}

dag = DAG('kubernetes_pod_operator_test', default_args=default_args)

input_volume = Volume(
    name="inputdata",
    configs={"hostPath": {"path":INPUT_DIR, "type":"Directory"}}
)

input_volume_mount = VolumeMount(
    "inputdata",
    mount_path="/usr/src/app/input",
    sub_path=None,
    read_only=True
)

output_volume = Volume(
    name="outputdata",
    configs={"hostPath": {"path":OUTPUT_DIR, "type":"Directory"}}
)

output_volume_mount = VolumeMount(
    "outputdata",
    mount_path="/usr/src/app/output",
    sub_path=None,
    read_only=False
)


passing = KubernetesPodOperator(namespace='default',
                          image="edrn/reg_mult",
                          #cmds=["python","-c"],
                          #arguments=["print('hello world')"],
                          #labels={"foo": "bar"},
                          name="regmulti",
                          task_id="regmulti-task",
                          in_cluster=False,
                          do_xcom_push=False,
                          get_logs=True,
                          startup_timeout_seconds=300,
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


