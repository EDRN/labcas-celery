# Docker image to run Smart3seq pipeline
FROM edrn/labcas-celery as labcas-celery

FROM centos:7

RUN yum update -y &&\
    yum install -y git wget bzip2 which

# Anaconda pre-requisites for graphical packages
RUN yum install -y libXcomposite libXcursor libXi\
                   libXtst libXrandr alsa-lib mesa-libEGL\
                   libXdamage mesa-libGL libXScrnSaver

# Anaconda
ENV CONDA_HOME=/usr/local/anaconda3
ENV PATH=${CONDA_HOME}/bin:$PATH
RUN wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh &&\
    bash Anaconda3-2019.03-Linux-x86_64.sh -b -p ${CONDA_HOME}
RUN source ${CONDA_HOME}/bin/activate && conda init bash

# clone Smart-3seq repo
RUN cd /usr/local &&\
    git clone https://github.com/danielanach/SMART-3SEQ-smk.git

# create and activate virtual environment
RUN cd /usr/local/SMART-3SEQ-smk &&\
    conda env create -f environment.yml
RUN echo "source activate smart-3seq" > ~/.bashrc

# clone 3SEQtools repositories for UMI-handling tools
RUN cd /usr/local/SMART-3SEQ-smk/code &&\
    git clone https://github.com/jwfoley/3SEQtools.git &&\
    git clone https://github.com/jwfoley/umi-dedup.git

#COPY config.yaml /usr/local/SMART-3SEQ-smk/code/config.yaml

WORKDIR /usr/local/SMART-3SEQ-smk/code
