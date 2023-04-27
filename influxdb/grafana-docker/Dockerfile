FROM docker.io/grafana/grafana

COPY dashboards /var/lib/grafana/dashboards
COPY provisioning /etc/grafana/provisioning

ENV GF_DEFAULT_APP_MODE "development"

