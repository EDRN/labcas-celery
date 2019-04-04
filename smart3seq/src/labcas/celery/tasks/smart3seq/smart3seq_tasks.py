"""
Smart3seq workflow
"""
import argparse
import sys
from labcas.celery.worker import app
from celery import chain
from labcas.celery.tasks.system_tasks import echo, exec_script
import time

SCRIPT_DATA_DOWLOAD = "/usr/local/bin/run_data_download.sh"

SCRIPT_SMART3SEQ_ALIGNMENT = "/usr/local/bin/smart3seq_alignment.sh"
SCRIPT_SMART3SEQ_COUNTING = "/usr/local/bin/smart3seq_counting.sh"

WORKFLOW = "smart3seq"



def smart3seq_workflow(run):
    
    print("Executing Smart3seq workflow")
    
    s3 = exec_script.signature((SCRIPT_SMART3SEQ_ALIGNMENT, run,),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    s4 = exec_script.signature((SCRIPT_SMART3SEQ_COUNTING, run,),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    
    async_result = chain(s3 | s4).apply_async()

    return async_result
    

# command line invocation program
if __name__ == '__main__':
    
    # submit N tasks asynchronously
    from labcas.celery.tasks.smart3seq.smart3seq_tasks import smart3seq_workflow
    
    # FIXME: test run
    # run = "11553"
    # submit N jobs
    for run in range(10):
        smart3seq_workflow(str(run))
        time.sleep(5)
    
