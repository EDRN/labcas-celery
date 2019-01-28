# LabCAS Celery worker equipped with Tensorflow package
FROM edrn/labcas-celery

RUN apt-get update

# install Tensorflow in system Python
RUN pip install tensorflow

# install LabCAS Celery tasks for Tensorflow
COPY src/labcas/celery/tasks/tensorflow/ /usr/local/src/labcas/celery/tasks/tensorflow/