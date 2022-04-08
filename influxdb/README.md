# InfluxDB

## Resources
- [influx write](https://docs.influxdata.com/influxdb/v2.1/reference/cli/influx/write/)
- [Python client](https://github.com/influxdata/influxdb-client-python)

## Quickstart
### Start InfluxDB
In `sharedairdfw/`, run `docker-compose up` to start InfluxDB, Grafana, and Node-RED.  
```shell
cd sharedairdfw
docker-compose up
```

### Initialize InfluxDB and Influx CLI
Log into InfluxDB at http://localhost:8086. Set the admin username/password, and remember it for later.  
- For the org name, put `sharedairdfw`. 
- For the default bucket, put `main`.

Navigate to `Data` > `API Tokens`, click on the entry (there should only be one), and take note of the token at the 
top of the popup.  

In command line, configure `influx` with the following:
```shell
influx config create --config-name default \
  --host-url http://localhost:8086 \
  --org sharedairdfw \
  --token <your-auth-token-from-prev-step> \
  --active
```

[based on documentation](https://docs.influxdata.com/influxdb/cloud/reference/cli/influx/#provide-required-authentication-credentials)

> TODO: This step requires you to have the `influx` tool installed locally, because the ingestion script currently 
> does not run in the container. Should be moved inside the container.

### Run the Ingestion Script
Run the script, with the mqttSubscribers data directory as an argument.  
```shell
cd influxdb
./csvtoinflux.sh ../mqttSubscribers_dump
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
In the InfluxDB dashboard, navigate to `Explore`, and select the `sharedairdfw` bucket. Configure the filters to 
whatever you want, make sure the time range (top right of bottom panel) surrounds the data you want to graph, and 
hit `Submit`. 

You may want to use a custom, 1-minute mean aggregate function to view the trends in more detail.  

Example:  
![Example showing custom aggregate function](doc-img/Screen%20Shot%202022-04-08%20at%204.12.52%20PM.png)