# syntax=docker/dockerfile:1

FROM python:3.11
RUN apt install curl
RUN pip install Flask uWSGI
COPY ./requirements.txt /server/requirements.txt
WORKDIR /server
RUN pip install -r requirements.txt
COPY . /server
EXPOSE 5001