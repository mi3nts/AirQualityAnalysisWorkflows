FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY test-gauge.py test-gauge.py


RUN pip3 install -r requirements.txt


CMD [ "python3", "test-gauge.py"]