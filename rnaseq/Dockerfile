# Docker image for sample rna-seq data processing

FROM edrn/labcas-celery as labcas-celery

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

# install Miniconda 3
# downgrade to Python 3.6 to run Celery and Flower
ENV CONDA_HOME /usr/local/miniconda
ENV PATH ${CONDA_HOME}/bin:${PATH}
RUN apt-get install -y  curl
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh\
	&& bash Miniconda3-latest-Linux-x86_64.sh -b -p ${CONDA_HOME} &&\
	conda install python=3.6

# install Celery and Flower
RUN pip install --no-cache-dir celery[redis] flower
    
# install HTseq in the same virtaul environment
RUN pip install numpy matplotlib\
	&& pip install HTSeq
	
# create non-privileged user to run Celery workers
RUN groupadd -g 999 noroot && \
    useradd -r -u 999 -g noroot -d /home/noroot noroot
    
# install labcas celery package
COPY --from=labcas-celery /usr/local/src/labcas /usr/local/src/labcas 
ENV PYTHONPATH /usr/local/src
	