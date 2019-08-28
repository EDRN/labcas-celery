# Docker image to process UNMC images
FROM python:3.7

RUN apt-get update

RUN pip install scikit-image tifffile glob2

COPY translate_multi_channel_frames_parallel_new.py /usr/local/bin/translate_multi_channel_frames_parallel.py

WORKDIR /usr/local/bin
#ENTRYPOINT ["python", "translate_multi_channel_frames_parallel.py"]
