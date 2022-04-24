# Grafana Configuration Docs

## Grafana Quirks

Grafana has the following [bug](https://github.com/grafana/grafana/issues/46247). What to know from this is to not
create any library panels if they are to be provisioned on startup. I (Eric) have deleted the `libraryPanel`
property of all panels in the dashboard json created by John, to get it to load properly.

Grafana generates a random UID for everything unless provided. So, I have manually provided a UID in the InfluxDB
datasource, which should be referenced in every dashbaord which uses InfluxDB.

## Additional Information

Here, Grafana is configured with ENV variables rather than providing a complete configuration.ini file. This way, we
know we're using default values if not specified.

## External Docs

- [Docker configuration](https://grafana.com/docs/grafana/latest/administration/configure-docker/)
    - Contains paths of where to put configuration files
- [Configuring Grafana with ENV Variables](https://grafana.com/docs/grafana/latest/administration/configuration/#override-configuration-with-environment-variables)
- [General provisioning documentation](https://grafana.com/docs/grafana/latest/administration/provisioning)
    - Data sources, dashboards, alerts, etc.
- [InfluxDB datasource configuration](https://grafana.com/docs/grafana/latest/datasources/influxdb/provision-influxdb/)