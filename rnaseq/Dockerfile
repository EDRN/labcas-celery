# Docker image for sample rna-seq data processing

ARG WRC_HUB=611908976619.dkr.ecr.us-west-2.amazonaws.com
ARG WRC_DC_VERSION
FROM ${WRC_HUB}/wrc-dcpylib:${WRC_DC_VERSION} as wrc-dcpylib

FROM ${WRC_HUB}/wrc-wmgr:${WRC_DC_VERSION} as oodt-wmgr

FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y default-jre
ENV JAVA_HOME=/usr/lib/jvm/default-java

RUN apt-get update && \
    apt-get install -y wget unzip tar bzip2 make gcc libz-dev g++

# install bowtie2
RUN cd /usr/local && \
    wget 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.2.9/bowtie2-2.2.9-linux-x86_64.zip' && \
    unzip bowtie2-2.2.9-linux-x86_64.zip && \
    ln -s ./bowtie2-2.2.9 ./bowtie2 && \
    rm bowtie2-2.2.9-linux-x86_64.zip
ENV PATH=$PATH:/usr/local/bowtie2
ENV BT2_HOME=/usr/local/bowtie2

# install tophat
RUN cd /usr/local && \
    wget 'https://ccb.jhu.edu/software/tophat/downloads/tophat-2.1.1.Linux_x86_64.tar.gz' && \
    tar xvfz tophat-2.1.1.Linux_x86_64.tar.gz && \
    ln -s ./tophat-2.1.1.Linux_x86_64 ./tophat && \
    rm tophat-2.1.1.Linux_x86_64.tar.gz
ENV PATH=$PATH:/usr/local/tophat

# install samtools
ENV SAMTOOLS_VERSION=1.5
RUN apt-get update && \
    apt-get install -y libncurses5-dev libncursesw5-dev libbz2-dev libssl-dev liblzma-dev
RUN cd /usr/local && \
    mkdir samtools_install && \
    wget "https://github.com/samtools/samtools/releases/download/${SAMTOOLS_VERSION}/samtools-${SAMTOOLS_VERSION}.tar.bz2" && \
    tar xvf samtools-${SAMTOOLS_VERSION}.tar.bz2 && \
    cd samtools-${SAMTOOLS_VERSION} && \
    make && \
    make prefix=/usr/local/samtools_install install && \
    rm "/usr/local/samtools-${SAMTOOLS_VERSION}.tar.bz2"
ENV PATH=$PATH:/usr/local/samtools_install/bin
    
# install HTSeq
# requires numpmy and matplotlib as pre-requisites
# must install Python 2.7+ to run HTseq
RUN cd /usr/local && \
    wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /usr/local/miniconda2 
ENV PATH=/usr/local/miniconda2/bin:$PATH
RUN pip install --upgrade pip
RUN pip install numpy matplotlib
RUN pip install HTSeq==0.9.1

# install FastQC
RUN apt-get update && \
    apt-get install -y build-essential
RUN cd /usr/local && \
    wget 'https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.7.zip' && \
    unzip fastqc_v0.11.7.zip && \
    chmod +x FastQC/fastqc
ENV PATH=$PATH:/usr/local/FastQC

# install Workflow Manager executable and OODT directories
COPY --from=oodt-wmgr /usr/local/oodt /usr/local/oodt

# install OODT configuration for these specific workflows
COPY conf/workflows/rpccc-genomics /usr/local/oodt/workflows/rpccc-genomics
COPY conf/workflows/rpccc-genomics-example /usr/local/oodt/workflows/rpccc-genomics-example

# install Python3 to run wrc-dcpylib
RUN cd /usr/local && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /usr/local/miniconda3
ENV PATH=/usr/local/miniconda3/bin:$PATH
RUN conda update -n base conda
RUN pip install --upgrade pip

# insall Kallisto
# setup dedicated python virtual environment within miniconda3
RUN conda create -n kallisto_venv && \
    . activate kallisto_venv && \
    conda config --add channels defaults && \
    conda config --add channels conda-forge && \
    conda config --add channels bioconda && \
    conda install kallisto && \
    . deactivate
    
# insall Salmon
# setup dedicated python virtual environment within miniconda3
RUN conda create -n salmon_venv &&\
    . activate salmon_venv && \
    conda config --add channels defaults &&\
    conda config --add channels conda-forge &&\
    conda config --add channels bioconda &&\
    conda install salmon &&\
    . deactivate
    
# download STAR binary
RUN cd /usr/local/bin && \
    wget -O STAR 'https://github.com/alexdobin/STAR/blob/master/bin/Linux_x86_64_static/STAR?raw=true' && \
    chmod +x STAR

# install Data Commons python library and its dependencies
COPY --from=wrc-dcpylib /usr/src/wrc /usr/local/wrc-dcpylib/src/wrc
COPY --from=wrc-dcpylib /usr/src/requirements.txt /usr/local/wrc-dcpylib/src/requirements.txt
RUN pip install --no-cache-dir --ignore-installed -r /usr/local/wrc-dcpylib/src/requirements.txt
ENV PYTHONPATH=.:/usr/local/wrc-dcpylib/src

# environment
ENV OODT_HOME /usr/local/oodt
ENV OODT_CONFIG ${OODT_HOME}/workflows
ENV PGE_ROOT ${OODT_HOME}/pges
ENV WORKFLOW_URL http://localhost:9001/

EXPOSE 9001

# start Workflow Manager
WORKDIR ${OODT_HOME}/cas-workflow/bin
CMD ./wmgr start && tail -f ${OODT_HOME}/cas-workflow/logs/cas_workflow.log