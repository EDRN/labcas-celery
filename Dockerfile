# Dockerfile to build LabCAS Celery Worker
FROM python:3.7
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

RUN apt-get update

# install LabCAS-celery source code
COPY ./src /usr/local/src
ENV PYTHONPATH /usr/local/src

# install Celery
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir -r /usr/local/src/requirements.txt
    
WORKDIR /usr/local/src
CMD ["celery", "-A",  "labcas.celery.worker", "worker", "-l", "info"]