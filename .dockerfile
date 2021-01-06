FROM python:3.7.6

ENV LANG en_US.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONIOENCODING utf_8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_dev.txt /usr/src/app/
RUN pip3 install -r requirements_dev.txt

RUN apt-get update && apt-get install -y \
        gettext \
    --no-install-recommends

# Create unprivileged celery user
RUN addgroup celery
RUN adduser -D -g '' celery -G celery

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
CMD ["gunicorn","iati.wsgi:application","--bind","0.0.0.0:5000","--workers","3"]

