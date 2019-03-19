# LabCAS bcbio image
#
FROM ubuntu:16.04

# install pre-requisites
RUN apt-get update && \
    apt-get install -y curl wget git unzip tar gzip bzip2 xz-utils pigz ttf-dejavu && \
    apt-get install -y --no-install-recommends libcurl4-gnutls-dev mbuffer python2.7-dev python-virtualenv

# install bcbio software
RUN wget https://raw.github.com/bcbio/bcbio-nextgen/master/scripts/bcbio_nextgen_install.py
#RUN python bcbio_nextgen_install.py /usr/local/share/bcbio --tooldir=/usr/local \
#    --genomes GRCh37 --aligners bwa --aligners bowtie2
RUN python bcbio_nextgen_install.py /usr/local/share/bcbio --tooldir=/usr/local \
    --nodata
