FROM ubuntu:latest
MAINTAINER Gigi Sayfan "the.gigi@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /over_achiever
WORKDIR /over_achiever
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python run.py
