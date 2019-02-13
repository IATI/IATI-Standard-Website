FROM ubuntu:18.04

ENV LANG en_US.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONIOENCODING utf_8

WORKDIR /tmp/
RUN apt-get update && apt-get install -y python3 \
   python3-dev python3-pip wget firefox

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.16.0/geckodriver-v0.16.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_dev.txt /usr/src/app/
RUN pip3 install -r requirements_dev.txt

