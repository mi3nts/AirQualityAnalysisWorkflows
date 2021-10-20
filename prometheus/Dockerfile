FROM python:3.8.10

RUN apt update

RUN apt install build-essential gcc -y

RUN pip install --upgrade pip

RUN pip install numpy

RUN pip install python-dateutil

RUN pip install pytz

RUN pip install pandas

RUN pip install pathlib

RUN ulimit unlimited

### Setup prometheus
COPY prometheus-2.30.0.linux-amd64/         /prometheus-2.30.0.linux-amd64
COPY csv_data/                   /csv_data
RUN mkdir openmetrics_data/
COPY csvtoopenmetrics.py         /prometheus-2.30.0.linux-amd64/csvtoopenmetrics.py

RUN python /prometheus-2.30.0.linux-amd64/csvtoopenmetrics.py

EXPOSE     9090

WORKDIR /prometheus-2.30.0.linux-amd64

CMD ["/bin/sh", "-c", "./prometheus --storage.tsdb.retention.time=5y --query.lookback-delta=5y --storage.tsdb.allow-overlapping-blocks"]


