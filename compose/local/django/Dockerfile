FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev \
    && apk add --no-cache bash

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

COPY ./compose/local/django/entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY ./compose/local/django/start.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /app

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
