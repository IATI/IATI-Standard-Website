FROM alpine:3.20.2

ENV LANG en_US.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONIOENCODING utf_8

RUN apk update
RUN apk add --no-cache bash curl

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


RUN apk add build-base libffi-dev && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 usr/bin/pip

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache libmemcached-dev zlib-dev

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
        pip3 install --upgrade pip &&\
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
