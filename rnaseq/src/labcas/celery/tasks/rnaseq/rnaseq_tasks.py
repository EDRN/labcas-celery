"""
Sample RNA Sequencing tasks.
"""
import argparse
import sys
from labcas.celery.worker import app
from celery import chain
from labcas.celery.tasks.system_tasks import echo

WORKFLOW = "rnaseq"

def rnaseq_workflow(metadata={}):
    
    print("Executing RNASEQ workflow")
    
    s1 = echo.signature(("Running Tophat",),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    s2 = echo.signature(("Running Samtools",),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    s3 = echo.signature(("Running Htseq",),
                        queue=WORKFLOW, routing_key=WORKFLOW,
                        immutable=True)
    
    async_result = chain(s1 | s2 | s3).apply_async()

    return async_result
    

  # command line invocation program
if __name__ == '__main__':
    
    # submit N tasks asynchronously
    from labcas.celery.tasks.rnaseq.rnaseq_tasks import rnaseq_workflow
    
    rnaseq_workflow()
    
