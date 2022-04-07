FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG env_file=docker.dev.env

WORKDIR /home/code/
COPY . .

RUN mkdir static
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY ${env_file} .

RUN export $(cat ${env_file}) && \
    python3 manage.py collectstatic --no-input
