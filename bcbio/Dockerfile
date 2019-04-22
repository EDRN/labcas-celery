FROM ubuntu:18.04

RUN apt-get update

RUN apt-get update && \
    apt-get install -y wget unzip tar bzip2 make gcc libz-dev g++ vim git curl

# install Miniconda3
# downgrade to Python 3.6 to run Celery and Flower
ENV CONDA_HOME=/usr/local/miniconda
ENV PATH=${CONDA_HOME}/bin:$PATH
RUN cd /usr/local && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p ${CONDA_HOME} &&\
    conda install python=3.6

# install bcbio without downloading data
# note: installation path '/efs-ecs/docker/bcbio' must match verbatim the path on the host
# because paths are hard-wired in the bcbio configuration
RUN wget https://raw.github.com/bcbio/bcbio-nextgen/master/scripts/bcbio_nextgen_install.py
ENV BCBIO_INSTALL /efs-ecs/docker/bcbio
RUN mkdir -p $BCBIO_INSTALL/data $BCBIO_INSTALL/tools
RUN python bcbio_nextgen_install.py $BCBIO_INSTALL/data\
    --tooldir=$BCBIO_INSTALL/tools --aligners bwa --aligners bowtie2\
    --isolate --minimize-disk --nodata
ENV PATH=$PATH:$BCBIO_INSTALL/tools/bin/

# install Celery and Flower
RUN pip install --no-cache-dir celery[redis] flower

# install labcas celery package
COPY --from=edrn/labcas-celery /usr/local/src/labcas /usr/local/src/labcas 
ENV PYTHONPATH $PYTHONPATH:/usr/local/src

# create non-privileged user to run Celery workers
RUN groupadd -g 999 noroot && \
    useradd -r -u 999 -g noroot -d /home/noroot noroot
RUN mkdir -p /home/noroot && chown noroot:noroot /home/noroot
WORKDIR /home/noroot	

