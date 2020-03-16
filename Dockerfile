FROM python:3.7.2-stretch

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install git -y

WORKDIR /opt
COPY requirements.txt /opt/requirements.txt
RUN pip3 install -U pip setuptools wheel
RUN pip3 install -U -r requirements.txt
COPY . /opt
