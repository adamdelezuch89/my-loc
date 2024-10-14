# FROM python:3.13.0-alpine3.20 # disabled because of psycopg not detected issue
FROM python:3.11-alpine
LABEL maintainer="adamdelezuch89@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Geometry field dependencies:
    apk add --update --no-cache \
        build-base \
        gdal-dev \
        geos-dev \
        postgresql-dev \
        musl-dev \
        libffi-dev \
        gcc \
        libc-dev \
        linux-headers \
        python3-dev \
        bash \
        g++ \
        jpeg-dev \
        zlib-dev \
        proj-dev \
        sqlite-dev && \
    ## end of geometry dependencies
    apk add --update --no-cache \
        postgresql-client && \
    apk add --update --no-cache --virtual \
        .tmp-build-deps \
        build-base \
        postgresql-dev \
        musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user


COPY ./app /app
WORKDIR /app

ENV PATH="/py/bin:$PATH"

# Run collectstatic to gather all static files
RUN python manage.py collectstatic --noinput

USER django-user
