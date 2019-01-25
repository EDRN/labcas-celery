'''
Celery worker app configured with LabCAS tasks.
'''
from celery import Celery
import os

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.environ.get("CELERY_BACKEND_URL", "redis://localhost:6379/0")

app = Celery('labcas.celery',
             broker=broker_url,
             backend=backend_url,
             include=['labcas.celery.tasks.system'])

# optional configuration
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

