FROM python:3.5.4-alpine

COPY .git .git
COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps \
		gcc \
		git \
		libc-dev \
		libgcc \
		linux-headers \
	&& pip3 install -r requirements.txt \
	&& git rev-parse HEAD > /revision \
	&& rm -rf .git \
	&& apk del .build-deps \
	&& mkdir -p /app

WORKDIR /app
COPY ./app /app

ENV APP_SETTINGS config/dev.cfg

CMD gunicorn app:app -b 0.0.0.0:5000 --workers 4 --worker-class eventlet --reload
