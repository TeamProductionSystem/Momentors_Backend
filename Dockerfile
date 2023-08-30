FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

RUN pip install -r /requirements.txt

WORKDIR /app
COPY . /app/

RUN useradd -ms /bin/sh appuser

EXPOSE 8000

ENTRYPOINT [ "/app/django.sh" ]
