FROM python:3.7.2-alpine

RUN apk -U add \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        musl-dev \
        openssl-dev \
        python-dev \
        bash \
        curl ca-certificates \
    && update-ca-certificates \
    && pip install scrapy \
    && rm -rf /var/cache/apk/*

COPY run.sh /
COPY scraper.py /
RUN chmod +x /run.sh

ENTRYPOINT  ["/run.sh"]