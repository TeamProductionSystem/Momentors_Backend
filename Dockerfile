FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

RUN pip install -r /requirements.txt

WORKDIR /app
COPY . /app/

EXPOSE 8080

CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py runserver 0.0.0.0:8000
