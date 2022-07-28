FROM python:3.7-bullseye

# create and switch to ubuntu user
ENV PATH /home/ubuntu/.local/bin:$PATH
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1001 ubuntu && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ubuntu

WORKDIR /home/ubuntu/mix/
ENV PYTHONUNBUFFERED 1

# install python dependencies
ADD requirements.txt ./
RUN pip install -r requirements.txt
