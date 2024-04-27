FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV SECRET_KEY "django-insecure-&!#a^_mu_9u=8h91^#_+m@l!#o)0(4or(rv+_l^z^4@z9#6xgh"


RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt