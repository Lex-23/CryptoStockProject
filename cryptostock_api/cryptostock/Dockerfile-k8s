FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/code/
COPY . .

RUN mkdir django_static
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
