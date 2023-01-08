FROM python:3.10-alpine3.16

COPY poetry.lock pyproject.toml /temp/
COPY req.txt /temp/req.txt
COPY service /service
WORKDIR /service

EXPOSE 8000

RUN pip install -r /temp/req.txt
USER root