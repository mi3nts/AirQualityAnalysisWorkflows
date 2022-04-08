FROM python:3.8.10

RUN apt update
RUN apt install build-essential gcc -y

### Setup prometheus
COPY prometheus-2.30.0.linux-amd64/         /prometheus-2.30.0.linux-amd64
COPY rawMqtt/                   /rawMqtt
RUN chmod -R u=rwx rawMqtt/
RUN mkdir openmetrics_data/
RUN chmod -R u=rwx openmetrics_data/
COPY mqtt_csvtoopenmetrics.py         /prometheus-2.30.0.linux-amd64/mqtt_csvtoopenmetrics.py
RUN chmod u=rwx /prometheus-2.30.0.linux-amd64/mqtt_csvtoopenmetrics.py
COPY requirements.txt requirements.txt
RUN chmod u=rwx requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN ulimit unlimited

RUN python /prometheus-2.30.0.linux-amd64/mqtt_csvtoopenmetrics.py

WORKDIR /prometheus-2.30.0.linux-amd64

CMD ["/bin/sh", "-c", "./prometheus --storage.tsdb.retention.time=5y --query.lookback-delta=5y --storage.tsdb.allow-overlapping-blocks"]
