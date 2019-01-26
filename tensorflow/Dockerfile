# LabCAS Celery worker equipped with Tensorflow
FROM edrn/labcas-celery

# install tensorflow in system Python
USER root
RUN apt-get update
RUN pip install tensorflow
USER celery