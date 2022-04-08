# InfluxDB

## Resources
- [influx wrote](https://docs.influxdata.com/influxdb/v2.1/reference/cli/influx/write/)
- [Python client](https://github.com/influxdata/influxdb-client-python)

## Running the Code
Run the script, with the mqttSubscribers data directory as an argument.  
```shell
cd influxdb
./csvtoinflux.sh ../mqttSubscribers_dump
```

You should see output that looks similar to this:  
```
Loading GPGGALR (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_GPGGALR_2022_03_25.csv) into InfluxDB
Loading IPS7100 (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_IPS7100_2022_03_25.csv) into InfluxDB
Loading BME280 (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_BME280_2022_03_25.csv) into InfluxDB
Loading INA219Duo (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_INA219Duo_2022_03_25.csv) into InfluxDB
Loading PM (../mqttSubscribers_dump/rawMqtt/471a55800038004e/2022/03/25/MINTS_471a55800038004e_PM_2022_03_25.csv) into InfluxDB
Loading BME280 (../mqttSubscribers_dump/rawMqtt/478b5fe30040004b/2022/03/25/MINTS_478b5fe30040004b_BME280_2022_03_25.csv) into InfluxDB
Loading GPGGALR (../mqttSubscribers_dump/rawMqtt/478b5fe30040004b/2022/03/25/MINTS_478b5fe30040004b_GPGGALR_2022_03_25.csv) into InfluxDB
Loading IPS7100 (../mqttSubscribers_dump/rawMqtt/478b5fe30040004b/2022/03/25/MINTS_478b5fe30040004b_IPS7100_2022_03_25.csv) into InfluxDB
Loading PM (../mqttSubscribers_dump/rawMqtt/478b5fe30040004b/2022/03/25/MINTS_478b5fe30040004b_PM_2022_03_25.csv) into InfluxDB
Loading INA219Duo (../mqttSubscribers_dump/rawMqtt/478b5fe30040004b/2022/03/25/MINTS_478b5fe30040004b_INA219Duo_2022_03_25.csv) into InfluxDB
Loading PM (../mqttSubscribers_dump/rawMqtt/47db5580001e0039/2022/03/25/MINTS_47db5580001e0039_PM_2022_03_25.csv) into InfluxDB
Loading BME280 (../mqttSubscribers_dump/rawMqtt/47db5580001e0039/2022/03/25/MINTS_47db5580001e0039_BME280_2022_03_25.csv) into InfluxDB
Loading IPS7100 (../mqttSubscribers_dump/rawMqtt/47db5580001e0039/2022/03/25/MINTS_47db5580001e0039_IPS7100_2022_03_25.csv) into InfluxDB
Loading GPGGALR (../mqttSubscribers_dump/rawMqtt/47db5580001e0039/2022/03/25/MINTS_47db5580001e0039_GPGGALR_2022_03_25.csv) into InfluxDB
```