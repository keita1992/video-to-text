FROM python:3.9-slim

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN apt-get update && apt-get install -y libmagic1 git vim

RUN pip install --no-cache-dir pipenv
RUN cd /app && pipenv sync --dev

WORKDIR /app