FROM alpine:3.13.2

ENV LANG en_US.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONIOENCODING utf_8

RUN apk update
RUN apk add --no-cache bash

# Init engine

RUN apk add --no-cache openrc

# For psycopg + celery
RUN apk add postgresql-client && \
    set -ex \
	&& apk add gcc \
		g++ \
		make \
		libc-dev \
		musl-dev \
		linux-headers \
		pcre-dev \
		postgresql-dev \
		git

RUN apk add python3-dev

RUN apk add --no-cache python3 py3-pip && \
 if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
 if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi


RUN apk add build-base libffi-dev libressl-dev && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 usr/bin/pip && \
    pip install --upgrade pip

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache libmemcached-dev zlib-dev

# Elasticsearch from https://github.com/blacktop/docker-elasticsearch-alpine/blob/master/6.8/Dockerfile

RUN apk add --no-cache openjdk8-jre su-exec

ENV VERSION 6.8.23
ENV DOWNLOAD_URL "https://artifacts.elastic.co/downloads/elasticsearch"
ENV ES_TARBAL "${DOWNLOAD_URL}/elasticsearch-oss-${VERSION}.tar.gz"
# ENV EXPECTED_SHA_URL "${DOWNLOAD_URL}/elasticsearch-oss-${VERSION}.tar.gz.sha512"
ENV ES_TARBALL_SHA "14dbb2809b06499373c3ec5035d829d62255c2c93103618fbfe3d7d03cecf8847f654e83c78f765f23224126ff18ed713b959857e8ecf435c475b11bcd143d3f"
RUN apk add --no-cache -t .build-deps wget ca-certificates gnupg openssl \
  && set -ex \
  && cd /tmp \
  && echo "===> Install Elasticsearch..." \
  && wget --progress=bar:force -O elasticsearch.tar.gz "$ES_TARBAL"; \
  if [ "$ES_TARBALL_SHA" ]; then \
  echo "$ES_TARBALL_SHA *elasticsearch.tar.gz" | sha512sum -c -; \
  fi; \
  tar -xf elasticsearch.tar.gz \
  && ls -lah \
  && mv elasticsearch-$VERSION /usr/share/elasticsearch \
  && adduser -D -h /usr/share/elasticsearch elasticsearch \
  && echo "===> Creating Elasticsearch Paths..." \
  && for path in \
  /usr/share/elasticsearch/data \
  /usr/share/elasticsearch/logs \
  /usr/share/elasticsearch/config \
  /usr/share/elasticsearch/config/scripts \
  /usr/share/elasticsearch/tmp \
  /usr/share/elasticsearch/plugins \
  ; do \
  mkdir -p "$path"; \
  chown -R elasticsearch:elasticsearch "$path"; \
  done \
  && rm -rf /tmp/* \
  && apk del --purge .build-deps

COPY config/elastic/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
COPY config/elastic/log4j2.properties /usr/share/elasticsearch/config/log4j2.properties
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/config

RUN mkdir -p /var/log/messages
RUN apk add logrotate
COPY config/elastic/logrotate /etc/logrotate.d/elasticsearch
RUN chmod 644 /etc/logrotate.d/elasticsearch
COPY config/elastic/elasticsearch.service /etc/init.d/elasticsearch.service

# Web app dependencies

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_dev.txt /usr/src/app/
COPY entrypoint.sh /usr/src/app/
ENV VIRTUAL_ENV=/usr/src/venv
ENV PATH=$VIRTUAL_ENV/bin:$HOME/.cargo/bin:$PATH
ENV PYTHONPATH=/usr/src/app/

RUN apk -U upgrade
# Use a virtual env here, because othewise we get conflicats between Alpine's
# packages and pip's. (This has started happening because we switched to pip-
# tools which pins every dependency).
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo libwebp libwebp-tools &&\
        python3 -m venv /usr/src/venv &&\
        . /usr/src/venv/bin/activate &&\
        pip3 install -r requirements_dev.txt

RUN apk add --no-cache gettext

RUN chmod 775 /usr/src/app

EXPOSE 5000

RUN mkdir -p /var/log/gunicorn
RUN chmod 644 /var/log/gunicorn
RUN touch /var/log/gunicorn/gunicorn.log
COPY delete_large_logs /etc/periodic/15min/delete_large_logs
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["tail", "-n", "+0", "-f", "/var/log/gunicorn/gunicorn.log"]
