FROM ubuntu:16.04 as common

RUN apt-get update --fix-missing \
    && apt-get install -y wget git

COPY .git .git

ARG lumavate_signer_branch=master

RUN apt-get update && apt-get install -y git \
  && mkdir /root/.ssh/ \
  && touch /root/.ssh/known_hosts \
  && ssh-keyscan github.com >> /root/.ssh/known_hosts \
  && mkdir /python_packages \
  && cd /python_packages \
  && git clone https://github.com/Lumavate-Team/python-signer.git lumavate_signer \
  && git checkout $lumavate_signer_branch \
  && rm -rf /python_packages/lumavate_signer/.git

FROM python:3.5.4-alpine

EXPOSE 5000

COPY --from=common /python_packages ./python_packages/
COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps \
		gcc \
		git \
		libc-dev \
		libgcc \
		linux-headers \
	&& pip3 install -r requirements.txt \
	&& apk del .build-deps \
	&& mkdir -p /app

ENV PYTHONPATH /python_packages
WORKDIR /app
COPY ./app /app

ENV APP_SETTINGS config/dev.cfg

CMD gunicorn app:app -b 0.0.0.0:5000 --workers 4 --worker-class eventlet --reload
