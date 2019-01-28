'''
Celery worker app configured with LabCAS tasks.
'''
from celery import Celery
import os
import pkgutil
import labcas.celery.tasks


# utility functions to list all modules of a given package, recursively
def list_modules(package):
    modules = []
    _list_modules(package, modules)
    return modules


def _list_modules(package, modules):
    for _, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                   prefix=package.__name__+'.',
                                                   onerror=lambda _: None):
        if not ispkg:
            modules.append(modname)


broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.environ.get("CELERY_BACKEND_URL", "redis://localhost:6379/0")

task_modules = list_modules(labcas.celery.tasks)
app = Celery('labcas.celery',
             broker=broker_url,
             backend=backend_url,
             include=task_modules)

# optional configuration
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
