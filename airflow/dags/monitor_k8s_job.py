from kubernetes import client, config, watch
import logging
import time
import sys

config.load_kube_config()

v1 = client.BatchV1Api()

def monitor_k8s_job(exec_date):
    '''Function to monitor a Kubernets job with a specific
       value of the exec_date label.'''

    v1 = client.BatchV1Api()
    print("Starting to monitor...")
    while True:
       jobs = v1.list_namespaced_job(namespace='default', watch=False, label_selector='exec_date=%s' % exec_date)
       #print("jobs=%s" % jobs)
       if jobs.items:
          for job in jobs.items:
             npa = job.status.active
             npf = job.status.failed
             nps = job.status.succeeded
             print("Number of pods active, failed, succeded: %s, %s, %s" % (npa, npf, nps))
             if nps and int(nps)==1:
                print("Pod succeeded, returning")
                return
             elif npf and int(npf)==1:
                raise AirflowFailException("Job failed!")
             elif npa and int(npa)==1:
                print("Waiting for pod to stop running...")
                time.sleep(10)
             else:
                raise AirflowFailException("Cannot monitor jobs reliably, exiting!")
       else:
           raise AirflowFailException("Cannot find any job matching label: exec_date=%s" % exec_date)

if __name__ == "__main__":

   exec_date = sys.argv[1]
   print("Monitoring for: %s" % exec_date)

   monitor_k8s_job(exec_date)
