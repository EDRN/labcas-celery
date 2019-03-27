"""
Sample RNA Sequencing tasks.
"""
import argparse
import sys
from labcas.celery.worker import app
from celery import chain
from labcas.celery.tasks.system_tasks import echo, exec_script

SCRIPT_DATA_DOWLOAD = "/usr/local/bin/run_data_download.sh"
SCRIPT_TOPHAT = "/usr/local/bin/run_tophat.sh"
SCRIPT_SAMTOOLS = "/usr/local/bin/run_samtools.sh"
SCRIPT_HTSEQ_COUNT = "/usr/local/bin/run_htseq_count.sh"

WORKFLOW = "rnaseq"

def rnaseq_workflow(metadata={}):
    
    print("Executing RNASEQ workflow")
    
    s0 = exec_script.signature((SCRIPT_DATA_DOWLOAD,),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    s1 = exec_script.signature((SCRIPT_TOPHAT,),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    s2 = exec_script.signature((SCRIPT_SAMTOOLS,),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    s3 = exec_script.signature((SCRIPT_HTSEQ_COUNT,),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    
    async_result = chain(s0 | s1 | s2 | s3).apply_async()

    return async_result
    

# command line invocation program
if __name__ == '__main__':
    
    # submit N tasks asynchronously
    from labcas.celery.tasks.rnaseq.rnaseq_tasks import rnaseq_workflow
    
    rnaseq_workflow()
    
