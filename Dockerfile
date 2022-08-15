FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD python3 manage.py runserver 0.0.0.0:$PORT
