FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add libffi-dev

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
COPY . /app/

RUN useradd -ms /bin/sh appuser

EXPOSE 8000

ENTRYPOINT [ "/app/django.sh" ]
