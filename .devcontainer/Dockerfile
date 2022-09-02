FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

# install packages
RUN \
  apt-get update \
  && apt-get install -qq -y \
    sudo nano htop build-essential libssl-dev zlib1g-dev libffi-dev libbz2-dev \
    liblzma-dev libkrb5-dev libsqlite3-dev openjdk-8-jdk zip dos2unix maven nodejs \
    python3.7 python3.7-dev python3.7-distutils \
    curl wget git openjdk-8-jdk maven zip apt-transport-https \
  && curl -sL https://deb.nodesource.com/setup_current.x | bash - \
  && apt-get update && apt install -y nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-amd64

# Register the version in alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# Set python 3 as the default python
RUN update-alternatives --set python /usr/bin/python3.7
RUN update-alternatives --set python3 /usr/bin/python3.7

# Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py --force-reinstall && \
    rm get-pip.py

# create and switch to ubuntu user
ENV PATH /home/ubuntu/.local/bin:$PATH
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1001 ubuntu && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ubuntu
WORKDIR /home/ubuntu

# install python dependencies
ADD requirements.txt ./
RUN pip install -r requirements.txt
