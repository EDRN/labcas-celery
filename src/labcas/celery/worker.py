'''
Celery worker app configured with LabCAS tasks.
'''
from celery import Celery

app = Celery('labcas.celery',
             # FIXME: read from env?
             broker='redis://redis:6379/0',
             #backend='redis://redis:6379/0',
             #backend='rpc://',
             #backend='redis://localhost',
             include=['labcas.celery.tasks.system'])

# optional configuration
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

