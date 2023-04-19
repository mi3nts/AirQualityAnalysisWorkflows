# InfluxDB

## Quickstart

### Initialize Configuration File

In `influxdb/` (this directory), create a file called `.env`. We will put passwords into this file, so do not commit it
to Git!

You may want to make a copy of `.example.env` to start with.

```shell
cp .env .env
```

### InfluxDB Configuration

Be sure to keep the first line, because this tells InfluxDB to automatically set up based on the other variables:

```dotenv
DOCKER_INFLUXDB_INIT_MODE=setup
```

Read about the other InfluxDB environment variables in the "Automated Setup" section
[here](https://hub.docker.com/_/influxdb). Also, feel free to change the other InfluxDB variables, because NodeRED and
InfluxDB will adjust from it.

### NodeRED Configuration

Set the 4 MQTT credentials (username and password for both Central and LoRa nodes). Use the same credentials as the ones
in `credentials.yml` and `loRacredentials.yml`, for in the mqttSubscribers repository.

### Start Docker Services

For your first time running the services, Docker will build our custom influxdb image.

```shell
docker-compose up --build
```

You should now be able to access InfluxDB at http://localhost:8086. Log in using the initial username/password combo you
specified in `.env`.

### Run Ingestion

Ingestion is not automated yet. Run the ingestion script to get old data into InfluxDB.

```shell
docker exec -it influxdb_influxdb_1 /custom-data/csvtoinflux.sh /custom-data/mqttSubscribers_dump
```

You should see output that looks similar to this:

```
Loading GPGGALR (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_GPGGALR_2022_03_25.csv) into InfluxDB
Detected single-sensor CSV
Loading IPS7100 (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_IPS7100_2022_03_25.csv) into InfluxDB
Detected single-sensor CSV
Loading BME280 (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_BME280_2022_03_25.csv) into InfluxDB
Detected single-sensor CSV
Loading INA219Duo (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_INA219Duo_2022_03_25.csv) into InfluxDB
Detected single-sensor CSV
Loading PM (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_PM_2022_03_25.csv) into InfluxDB
Detected single-sensor CSV
Loading BME280 (../mqttSubscribers_dump/rawMqtt/478b5fe30040004b/2022/03/25/MINTS_478b5fe30040004b_BME280_2022_03_25.csv) into InfluxDB
Detected single-sensor CSV
...
```

### Display Data

In the InfluxDB dashboard, navigate to `Explore`, and select the `SharedAirDFW` bucket (or whatever you set as
`DOCKER_INFLUXDB_INIT_BUCKET`). Configure the filters to whatever you want, make sure the time range (top right of
bottom panel) surrounds the data you want to graph, and hit `Submit`.

You may want to use a custom, 1-minute mean aggregate function to view the trends in more detail. Configure this on the
right side, under the `Submit` button.

Example:  
![Example showing custom aggregate function](doc-img/Screen%20Shot%202022-04-08%20at%204.12.52%20PM.png)

## Other Useful Knowledge

### Commands

Start the containers again, preserving all data:

```shell
docker-compose up
```

Start the containers again, rebuilding from scratch:

```shell
docker-compose down --volumes && docker-compose up --build
```

### Environment

The environment is specified in `.env`, and variables from it are pulled in with `docker-compose.yml`

## Docker Services

### Custom InfluxDB

InfluxDB is plug-and-play, with data persisted to the `influxdb_data` volume. It will read the environment variables on
build and automatically initialize an admin user. A token is also specified, rather than being automatically generated,
for simplicity.

The only manual step at this time is data ingestion.

`influxdb-docker/Dockerfile` copies everything in `influxdb-docker/` to `/custom-data/` in the container. This includes
the
`csvtoinflux.sh` ingestion script, and the original data.

### Custom NodeRED

NodeRED is plug-and-play, *with no data persisted*. Read more about this choice below. It, too, reads environment
variables on build to be used in the imported flows.

`nodered-docker/Dokerfile` copies `package.json`, with InfluxDB support included, to the container. It then installs
InfluxDB support. The dockerfile also copies flows, credentials, and settings to the container. The settings are
configured to read/store credentials in plaintext. This is not an issue because the plaintext "credentials" should refer
to environment variables only.

**Why not persist data?** short ramble: This service does not persist any data, because the container's `/data/`
needs to be written to by the Dockerfile at build time. Since containers are mounted after build, this would wipe all
configurations. There is definitely way around this, but the added complexity is not worth it at this time (flows and
settings will not change regularly). **To persist any changes, export them from the container and re-build.**

### Grafana

Grafana is *not* plug-and-play. This is a todo item.  

## External Resources

- [influx write](https://docs.influxdata.com/influxdb/v2.1/reference/cli/influx/write/)
- [Python client](https://github.com/influxdata/influxdb-client-python)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker compose file reference](https://docs.docker.com/compose/compose-file/)
- [influxdb Docker page/docs](https://hub.docker.com/_/influxdb)