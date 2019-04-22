"""
Bcbio workflow
"""
import argparse
import sys
from labcas.celery.worker import app
from celery import chain
from labcas.celery.tasks.system_tasks import echo, exec_script
import time

SCRIPT_BCBIO = "/usr/local/bin/bcbio.sh"
WORKFLOW = "bcbio"

def bcbio_workflow(run):
    
    print("Executing Bcbio workflow")
    
    s = exec_script.signature((SCRIPT_BCBIO, run,),
                              queue=WORKFLOW, routing_key=WORKFLOW,
                              immutable=True)
    
    async_result = s.apply_async()

    return async_result
    

# command line invocation program
if __name__ == '__main__':
    
    # submit N tasks asynchronously
    from labcas.celery.tasks.bcbio.bcbio_tasks import bcbio_workflow
    
    bcbio_workflow(str("test_param"))
    
