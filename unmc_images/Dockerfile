# Docker image to process UNMC images
FROM python:3.7

RUN apt-get update

RUN pip install scikit-image tifffile glob2

COPY translate_multi_channel_frames.py /usr/local/translate_multi_channel_frames.py

WORKDIR /usr/local
ENTRYPOINT ["python", "translate_multi_channel_frames.py"]
