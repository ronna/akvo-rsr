FROM python:2.7.15-stretch

RUN set -ex; apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests \
    libgeos-dev postgresql-client-9.6 && \
    rm -rf /var/lib/apt/lists/*

ENV NODE_VERSION 8.11.3

RUN curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.xz" \
  && tar -xJf "node-v$NODE_VERSION-linux-x64.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
  && rm "node-v$NODE_VERSION-linux-x64.tar.xz" \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs

RUN npm install -g yuglify

WORKDIR /var/akvo/rsr/code

COPY scripts/deployment/pip/requirements/2_rsr.txt ./
RUN pip install --no-cache-dir -r 2_rsr.txt

COPY scripts/deployment/pip/requirements/5_dev.txt ./
RUN pip install --no-cache-dir -r 5_dev.txt

COPY scripts/deployment/pip/requirements/3_testing.txt ./
RUN pip install --no-cache-dir -r 3_testing.txt

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /var/akvo/rsr/logs/
RUN mkdir -p /var/log/akvo/

CMD scripts/docker/dev/start-django.sh