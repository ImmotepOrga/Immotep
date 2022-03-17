FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

ADD project/requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

ADD project /code/
WORKDIR /code/