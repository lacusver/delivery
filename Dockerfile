FROM python:3.10-slim

WORKDIR /app

ADD . /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev musl-dev \
    postgresql postgresql-contrib \
    python3-pil \
    libxslt-dev libffi-dev zlib1g-dev \
    libjpeg-dev gettext \
    libc-dev make python3-pip python3-dev \
    gcc curl && \
    apt-get clean


ENV PATH="${PATH}:/usr/local/bin/python"


RUN pip install --upgrade pip\
    && pip install -r requirements.txt
