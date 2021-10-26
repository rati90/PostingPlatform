FROM python:3.9-slim-buster

WORKDIR /usr/src/app

RUN apt-get update

COPY ./req.txt .
RUN pip install -r req.txt
COPY . .