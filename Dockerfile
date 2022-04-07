FROM python:3.9

ADD . /personal-diary

ENV PYTHONPATH=/personal-diary TERM=xterm

WORKDIR /personal-diary

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get -y install nano

WORKDIR /personal-diary/personal_diary