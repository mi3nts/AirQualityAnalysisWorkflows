FROM python:3.10.0-alpine3.14

RUN pip install pandas

RUN pip install pathlib

### Setup prometheus

COPY prometheus        						/bin/prometheus
COPY promtool          						/bin/promtool
COPY documentation/examples/prometheus.yml  /etc/prometheus/prometheus.yml
COPY console_libraries/                     /usr/share/prometheus/console_libraries/
COPY consoles/                              /usr/share/prometheus/consoles/
COPY LICENSE                                /LICENSE
COPY NOTICE                                 /NOTICE
COPY startup.sh 							/bin/startup.sh

WORKDIR /prometheus

COPY csvtoopenmetrics.py         /prometheus/csvtoopenmetrics.py

RUN ln -s /usr/share/prometheus/console_libraries /usr/share/prometheus/consoles/ /etc/prometheus/ && \
    chown -R nobody:nobody /etc/prometheus /prometheus

USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
CMD		   [ "sh", "/bin/startup.sh" ]
