'''
Airflow DAG to execute the UNMCPC image alignment inside a K8s cluster

TODO: use sub-directories of the form data//{{ ts_nodash}} to allow multiple concurrent jobs
The problem is that the K8s volume paths cannot be templated, so we must pass some configuration to 
coregistration pod.
'''

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from kubernetes.client import models as k8s

AIRFLOW_SHARED_DIR = "/efs-ecs/docker/labcas/airflow"
S3_ROOT_URL = "s3://edrn-labcas/sftp_data/UNMCPC"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'start_date': datetime.utcnow(),
    'start_date': '2021-06-22',
    #start_date=days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'catchup': False,
    'schedule_interval': None,
    #'retry_delay': timedelta(minutes=5)
}

# volume to mount the AWS credentials inside the K8s pods
# Note: the host path is relative to the cloud host,
# NOT the docker containers where the Airflow webserver or scheduler run.
aws_creds_volume = k8s.V1Volume(
    name='aws-creds',
    host_path=k8s.V1HostPathVolumeSource(
        path="%s/.aws" % AIRFLOW_SHARED_DIR,
        type="Directory"
    )
)
aws_creds_volume_mount = k8s.V1VolumeMount(
    name='aws-creds', mount_path='/root/.aws', sub_path=None, read_only=True
)

# volume that holds input and output data in sub-directories
data_volume = k8s.V1Volume(
    name='data',
    host_path=k8s.V1HostPathVolumeSource(
        path="%s/data" % AIRFLOW_SHARED_DIR,
        type="Directory"
    )
)
data_volume_mount = k8s.V1VolumeMount(
    name='data', mount_path='/usr/src/app', sub_path=None, read_only=False
)

# FIXME: mount input/output volumes separately
input_volume = k8s.V1Volume(
    name='input',
    host_path=k8s.V1HostPathVolumeSource(
        path="%s/data/input" % AIRFLOW_SHARED_DIR,
        type="Directory"
    )
)
input_volume_mount = k8s.V1VolumeMount(
    name='input', mount_path='/usr/src/app/input', sub_path=None, read_only=False
)
output_volume = k8s.V1Volume(
    name='output',
    host_path=k8s.V1HostPathVolumeSource(
        path="%s/data/output" % AIRFLOW_SHARED_DIR,
        type="Directory"
    )
)
output_volume_mount = k8s.V1VolumeMount(
    name='output', mount_path='/usr/src/app/output', sub_path=None, read_only=False
)

dag = DAG(
    'unmcpc_with_k8s', default_args=default_args)

# FIXME: this task is needed when data directory is NOT job specific
cleanup_task = KubernetesPodOperator(
    namespace='default',
    image="ubuntu:16.04",
    cmds=["bash", "-cx"],
    arguments=["rm -rf /usr/src/app/input/* /usr/src/app/output/*"],
    volumes=[data_volume],
    volume_mounts=[data_volume_mount],
    task_id="cleanup_task",
    name="cleanup_pod",
    in_cluster=False,
    do_xcom_push=False,
    get_logs=True,
    startup_timeout_seconds=60,
    dag=dag
)


setup_task = KubernetesPodOperator(
    namespace='default',
    image="ubuntu:16.04",
    cmds=["bash", "-cx"],
    # FIXME
    #arguments=["mkdir -p /usr/src/app/{{ ts_nodash }}/input /usr/src/app/{{ ts_nodash }}/output"],
    arguments=["mkdir -p /usr/src/app/input /usr/src/app/output"],
    volumes=[data_volume],
    volume_mounts=[data_volume_mount],
    task_id="setup_task",
    name="setup_pod",
    in_cluster=False,
    do_xcom_push=False,
    get_logs=True,
    startup_timeout_seconds=60,
    dag=dag
)
 
download_task = KubernetesPodOperator(
    namespace='default',
    image="amazon/aws-cli",
    # cmds=[""],
    arguments=["s3", "sync", "%s/{{dag_run.conf['DATASET']}}/Input" % S3_ROOT_URL, 
               # FIXME
               # "/usr/src/app/{{ ts_nodash }}/input"],
               "/usr/src/app/input"],
    volumes=[aws_creds_volume, data_volume],
    volume_mounts=[aws_creds_volume_mount, data_volume_mount],
    env_vars={'AWS_DEFAULT_PROFILE': 'saml-pub'},
    task_id="download_task",
    name="download_pod",
    in_cluster=False,
    do_xcom_push=False,
    get_logs=True,
    startup_timeout_seconds=60,
    dag=dag
)

coregistration_task = KubernetesPodOperator(
    namespace='default',
    image="edrn/reg_mult",
    volumes=[input_volume, output_volume],
    volume_mounts=[input_volume_mount, output_volume_mount],
    task_id="coregistration_task",
    name="coregistration_pod",
    in_cluster=False,
    do_xcom_push=False,
    get_logs=True,
    startup_timeout_seconds=300,
    dag=dag
)

upload_task = KubernetesPodOperator(
    namespace='default',
    image="amazon/aws-cli",
    # cmds=[""],
    arguments=["s3", "sync", 
               # FIXME
               # "/usr/src/app/{{ ts_nodash }}/output/", 
               "/usr/src/app/output/", 
               "%s/{{dag_run.conf['DATASET']}}/Output/" % S3_ROOT_URL],
    volumes=[aws_creds_volume, data_volume],
    volume_mounts=[aws_creds_volume_mount, data_volume_mount],
    env_vars={'AWS_DEFAULT_PROFILE': 'saml-pub'},
    task_id="upload_task",
    name="upload_pod",
    in_cluster=False,
    do_xcom_push=False,
    get_logs=True,
    startup_timeout_seconds=60,
    dag=dag
)


cleanup_task >> setup_task >> download_task >> coregistration_task >> upload_task


# to be used by DebugExecutor
if __name__ == '__main__':
  # dag.clear(reset_dag_runs=True)
  dag.clear()
  dag.run()




