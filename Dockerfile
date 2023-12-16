FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
COPY . /src

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /src/requirements/dev.txt
