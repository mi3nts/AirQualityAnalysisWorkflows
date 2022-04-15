# InfluxDB

## Quickstart

### Configure

In `influxdb/` (this directory), create a file called `.env`. We will put passwords into this file, so do not commit it
to Git!

You may want to make a copy of `.example.env` to start with.

```shell
cp .example.env .env
```

Be sure to keep the first line:

```dotenv
DOCKER_INFLUXDB_INIT_MODE=setup
```

This tells InfluxDB to automatically set up based on the other variables.  
Read about the rest of the environment variables in the "Automated Setup"
section [here](https://hub.docker.com/_/influxdb).

### Start Docker Services

For your first time running the services, Docker will build our custom influxdb image.

```shell
docker-compose up --build
```

You should now be able to InfluxDB at http://localhost:8086. Log in using the values you specified in `.env`.

### Run Ingestion

Ingestion is not automated yet. Run the ingestion script to get data into InfluxDB.

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

In the InfluxDB dashboard, navigate to `Explore`, and select the `sharedairdfw` bucket (or whatever you set as
`DOCKER_INFLUXDB_INIT_BUCKET`). Configure the filters to whatever you want, make sure the time range (top right of
bottom panel) surrounds the data you want to graph, and hit `Submit`.

You may want to use a custom, 1-minute mean aggregate function to view the trends in more detail.

Example:  
![Example showing custom aggregate function](doc-img/Screen%20Shot%202022-04-08%20at%204.12.52%20PM.png)

## Other Useful Things

### Commands

Start the containers again, preserving all data:

```shell
docker-compose up
```

Start the containers again, rebuilding from scratch:

```shell
docker-compose down --volumes && docker-compose up --build
```

### Dockerfile

The `Dockerfile` copies everything in `influxdb-docker/` to `/custom-data/` in the container.

### Environment

The environment is specified in `.env`, and variables from it are pulled in with `docker-compose.yml`

### External Resources

- [influx write](https://docs.influxdata.com/influxdb/v2.1/reference/cli/influx/write/)
- [Python client](https://github.com/influxdata/influxdb-client-python)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker compose file reference](https://docs.docker.com/compose/compose-file/)
- [influxdb Docker page/docs](https://hub.docker.com/_/influxdb)