FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
RUN apk update \
    && pip install --upgrade pip \
    && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD gunicorn core.wsgi --bind 0.0.0.0:$PORT
