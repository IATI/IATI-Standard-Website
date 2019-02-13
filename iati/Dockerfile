FROM python:3.6.8-stretch

WORKDIR /tmp/
RUN apt-get update && apt-get install -y wget software-properties-common firefox-esr

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.17.0/geckodriver-v0.17.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_dev.txt /usr/src/app/
RUN pip install -r requirements_dev.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONIOENCODING utf_8
ENV LANG en_US.UTF-8

