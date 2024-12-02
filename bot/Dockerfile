FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /bot

COPY requirements.txt bot/requirements.txt
RUN pip3 install -r bot/requirements.txt

COPY . /bot