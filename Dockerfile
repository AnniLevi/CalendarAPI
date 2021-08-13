FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get -y install python3-pip
RUN mkdir /src
WORKDIR /src
COPY ./requirements.txt /scripts/
RUN pip3 install -r /scripts/requirements.txt
