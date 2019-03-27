# Docker image containing Smart3seq pipelines
FROM edrn/labcas-celery as labcas-celery

FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y \
    wget unzip tar bzip2 make gcc libz-dev g++ vim curl git pigz pypy parallel \
    libncurses5-dev libncursesw5-dev libbz2-dev libssl-dev liblzma-dev

# install samtools
ENV SAMTOOLS_VERSION=1.5
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

# install Miniconda3
# downgrade to Python 3.6 to run Celery and Flower
ENV CONDA_HOME=/usr/local/miniconda
ENV PATH=${CONDA_HOME}/bin:$PATH
RUN cd /usr/local && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p ${CONDA_HOME} &&\
    conda install python=3.6

# install 3SEQtools
RUN cd /usr/local &&\
    git clone https://github.com/jwfoley/3SEQtools.git
    
# install UMI-dedeup (expected to be located under $HOME)
RUN cd $HOME &&\
    git clone https://github.com/jwfoley/umi-dedup.git
ENV PYTHONPATH=$HOME/umi-dedup
    
# install dependencies
RUN pip install numpy numba pysam

# Install R
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update &&\
    apt-get install -y r-base

# install R packages including BioConductors
RUN apt-get update &&\
    apt-get install -y libcurl4-openssl-dev libxml2-dev
RUN sh -c "R -e \"install.packages('devtools', repos='http://cran.rstudio.com/')\""
RUN sh -c "R -e \"install.packages('WriteXLS', repos='http://cran.rstudio.com/')\""
RUN sh -c "R -e \"source('http://bioconductor.org/biocLite.R'); biocLite('BiocParallel')\""
RUN sh -c "R -e \"source('http://bioconductor.org/biocLite.R'); biocLite('Rsubread')\""
RUN sh -c "R -e \"source('http://bioconductor.org/biocLite.R'); biocLite('rtracklayer')\""

# install Celery and Flower
RUN pip install --no-cache-dir celery[redis] flower

# install labcas celery package
COPY --from=labcas-celery /usr/local/src/labcas /usr/local/src/labcas 
ENV PYTHONPATH $PYTHONPATH:/usr/local/src

# install smart3seq python tasks within labcas package
COPY src/labcas/celery/tasks/smart3seq/ /usr/local/src/labcas/celery/tasks/smart3seq/

# install program scripts
COPY scripts /usr/local/bin

# create non-privileged user to run Celery workers
RUN groupadd -g 999 noroot && \
    useradd -r -u 999 -g noroot -d /home/noroot noroot
RUN mkdir -p /home/noroot && chown noroot:noroot /home/noroot
WORKDIR /home/noroot	

