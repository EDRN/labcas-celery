# Docker image containing Smart3seq pipelines

FROM ubuntu:18.04

RUN apt-get update

RUN apt-get update && \
    apt-get install -y wget unzip tar bzip2 make gcc libz-dev g++ vim curl git

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
    
# download STAR binary
#RUN cd /usr/local/bin && \
#    wget -O STAR 'https://github.com/alexdobin/STAR/blob/master/bin/Linux_x86_64_static/STAR?raw=true' && \
#    chmod +x STAR
RUN cd /usr/local &&\
    curl -OLk https://github.com/alexdobin/STAR/archive/2.6.1d.tar.gz &&\
	gunzip 2.6.1d.tar.gz &&\
    tar -xvf 2.6.1d.tar &&\
	cd STAR-2.6.1d/source &&\
	make STAR &&\
	mv STAR /usr/local/bin/.
ENV PATH=$PATH:/usr/local/bin

# install Python 3
ENV CONDA_HOME=/usr/local/miniconda3
RUN cd /usr/local && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p ${CONDA_HOME}
ENV PATH=${CONDA_HOME}/bin:$PATH
    
# install 3SEQtools
RUN cd /usr/local &&\
    git clone https://github.com/jwfoley/3SEQtools.git
    
# install UMI-dedeup
RUN cd /usr/local &&\
    git clone https://github.com/jwfoley/umi-dedup.git
    
# install dependencies
RUN pip install numpy numba pysam

ENV PYTHONPATH=/usr/local/umi-dedup
