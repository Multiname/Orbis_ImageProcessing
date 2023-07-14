FROM python:3.11
RUN apt install curl
RUN pip install Flask uWSGI
COPY ./requirements.txt /src/requirements.txt
WORKDIR /src
RUN pip install -r requirements.txt
COPY . /src
EXPOSE 5002
ENV PYTHONUNBUFFERED=1 