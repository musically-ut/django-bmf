FROM ubuntu:14.04
MAINTAINER Sebastian Braun <sebastian@elmnt.de>

RUN rm /etc/apt/sources.list && \
    echo "deb http://archive.ubuntu.com/ubuntu trusty main" >> /etc/apt/sources.list && \
    echo "deb http://archive.ubuntu.com/ubuntu trusty universe" >> /etc/apt/sources.list && \
    echo "deb http://archive.ubuntu.com/ubuntu trusty-updates main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y

# Ensure UTF-8
RUN locale-gen en_US.UTF-8
ENV LANG       en_US.UTF-8
ENV LC_ALL     en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y python-pip python-dev && \
    apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN pip install flower redis

CMD ["celery", "flower", "--broker=redis://redis:6379/0"]
