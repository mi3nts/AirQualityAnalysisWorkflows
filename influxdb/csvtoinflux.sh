#!/bin/bash

# Recursively find csv files, and load them into influxdb

# Assumes InfluxDB host, organization, and token are in the active configuration.
# See more details: https://docs.influxdata.com/influxdb/cloud/reference/cli/influx/#provide-required-authentication-credentials

if [ -z $1 ]; then
  echo "Usage: $0 <csv_data_dir>"
  exit
fi

function loadCsvToInflux() {
  filename=$1
  echo "Loading $filename"
  sed '2,$s/^\([^ ]*\) \([^,]*\)/\1T\2Z/' "$filename" | \
  sed '2,$s/nan/-1/g' | \
  influx write \
    --bucket sharedairdfw \
    --format csv \
    --header '#datatype dateTime,measurement,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double,double'
}

export -f loadCsvToInflux

find "$1" -name '*.csv' -exec bash -c "loadCsvToInflux \"{}\"" \;
