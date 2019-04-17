FROM ubuntu:18.04

RUN apt-get update

RUN apt-get update && \
    apt-get install -y wget unzip tar bzip2 make gcc libz-dev g++ vim git curl

# install Python 3
ENV CONDA_HOME=/usr/local/miniconda3
RUN cd /usr/local && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p ${CONDA_HOME}
ENV PATH=${CONDA_HOME}/bin:$PATH

# install bcbio without downloading data
RUN wget https://raw.github.com/bcbio/bcbio-nextgen/master/scripts/bcbio_nextgen_install.py
RUN python bcbio_nextgen_install.py /usr/local/share/bcbio-nextgen\
    --tooldir=/usr/local --isolate --minimize-disk --nodata --aligners bwa --aligners bowtie2
