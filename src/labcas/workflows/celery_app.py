'''
Celery worker app.
'''
from celery import Celery

app = Celery('labcas.workflows',
             broker='amqp://',
             backend='amqp://',
             #backend='rpc://',
             #backend='redis://localhost',
             include=['labcas.workflows.tasks'])

# optional configuration
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

