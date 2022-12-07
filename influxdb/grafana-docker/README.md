# Grafana Configuration Docs

## Grafana Quirks

Grafana has the following [bug](https://github.com/grafana/grafana/issues/46247). What to know from this is to not
create any library panels if they are to be provisioned on startup. I (Eric) have deleted the `libraryPanel`
property of all panels in the dashboard json created by John, to get it to load properly.

Grafana generates a random UID for everything unless provided—including datasources. So, I have manually provided a UID
in the InfluxDB datasource, which should be referenced in every dashboard which uses InfluxDB.

The provisioning docs are wrong for plugin installation. To install plugins, use the `GF_INSTALL_PLUGINS`
environment variable. The format is a comma-separated list of identifiers.

## Additional Information

Here, Grafana is configured with ENV variables rather than providing a complete configuration.ini file. This way, we
know we're using default values if not specified.

## Provisioned Alerts

Grafana lets you easily develop alerts on the localhost website, but there is no way to easily download the file it generates as of writing.
Thus, in order to easily modify and provision the alerts via the .yaml file, it is necessary to somehow find and read this generated file during execution.

One such way is as follows:
Develop the alert rule as normal in Grafana, then (in chrome) opening up the devtools via pressing F12
Navigate to the Network tab
Click save and exit on the Grafana page
Some fetch requests should show up on the network manager. Select a request with "rules" in the name and then hit preview.
Gather the necessary information to provision your alert through the information displayed

## Slack Alert App

In order to change where the slack app posts alerts, simply generate an app via Slack's website, enable webhooks for it, then copy its webhook
and paste it in the url attribute in the file contactpoints.yaml.

## External Docs

- [Docker configuration](https://grafana.com/docs/grafana/latest/administration/configure-docker/)
    - Contains paths of where to put configuration files
- [Configuring Grafana with ENV Variables](https://grafana.com/docs/grafana/latest/administration/configuration/#override-configuration-with-environment-variables)
- [General provisioning documentation](https://grafana.com/docs/grafana/latest/administration/provisioning)
    - Data sources, dashboards, alerts, etc.
- [InfluxDB datasource configuration](https://grafana.com/docs/grafana/latest/datasources/influxdb/provision-influxdb/)