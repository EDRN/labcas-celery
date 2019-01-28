# Dockerfile to build the LabCAS Celery Worker
# NOTE: "if you want to use python 3.7 with celery then install celery from the master branch. celery 4.2.x supports 3.6 only"
FROM python:3.6
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

RUN apt-get update

# create non-privileged user to run Celery workers
RUN groupadd -g 999 noroot && \
    useradd -r -u 999 -g noroot noroot
    
# FIXME
# RUN pip install tensorflow

# install LabCAS-celery source code
COPY ./src /usr/local/src
ENV PYTHONPATH /usr/local/src

# install Celery and Flower
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir -r /usr/local/src/requirements.txt
    
# expose Flower port
EXPOSE 5555
    
WORKDIR /usr/local/src