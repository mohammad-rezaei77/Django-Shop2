FROM python:3.10-slim-buster

LABEL maintainer="mrezaei073@gmail.com" 

ENV PYTHONONBUFFER=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./core .