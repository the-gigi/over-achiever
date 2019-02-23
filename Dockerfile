FROM python:3
MAINTAINER Gigi Sayfan "the.gigi@gmail.com"
COPY . /over_achiever
WORKDIR /over_achiever
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python run.py
