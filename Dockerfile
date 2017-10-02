FROM ubuntu:14.04.2

RUN apt-get clean
RUN apt-get install -f
RUN dpkg --configure -a

RUN apt-get update
RUN apt-get install -y git --fix-missing
RUN apt-get install -y python3-pip --fix-missing
RUN apt-get install -y libpq-dev --fix-missing
RUN apt-get install -y libffi-dev

COPY requirements.txt ./
RUN python3.4 -m pip install -r requirements.txt

RUN mkdir -p /app

WORKDIR /app
COPY ./app /app

ENV APP_SETTINGS config/dev.cfg

CMD gunicorn app:app -b 0.0.0.0:5000 --workers 4 --worker-class eventlet --reload
