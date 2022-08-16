FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /docker/requirements.txt
    && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /docker
COPY requirements.txt requirements.txt
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
