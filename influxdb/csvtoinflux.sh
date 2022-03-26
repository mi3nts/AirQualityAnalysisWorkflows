#!/bin/bash

# Recursively find csv files, and load them into influxdb

# Assumes InfluxDB host, organization, and token are in the active configuration.
# See more details: https://docs.influxdata.com/influxdb/cloud/reference/cli/influx/#provide-required-authentication-credentials

# Exit if no data dir provided
if [ -z $1 ]; then
  echo "Usage: $0 <csv_data_dir>"
  exit
fi

function loadCsvToInflux() {
  local filepath=$1
  local filename
  local mac
  local sensor
  local header
  local datatype=''

  # Do not process if cannot parse sensor name & mac from title
  filename=$(basename "$filepath")
  if [[ ! "$filename" =~ MINTS_[0-9a-z]*_[0-9A-Za-z_]*_[0-9]{4}_[0-9]{2}_[0-9]{2}.csv ]]; then
    echo "Skipping because $filename did not match the required format."
    exit
  fi

  # Parse sensor name & mac from title
  mac=$(echo "$filename" | perl -pe 's/MINTS_(.*)_(.*)_\d{4}_\d{2}_\d{2}.csv/\1/')
  sensor=$(echo "$filename" | perl -pe 's/MINTS_(.*)_(.*)_\d{4}_\d{2}_\d{2}.csv/\2/')

  echo "Loading $sensor ($filepath) into InfluxDB"

  # Build datatype string from column names
  header=$(head -1 "$filepath")
  IFS=',' read -ra headerArr <<< "$header"

  for col in "${headerArr[@]}"; do
    if [[ "$col" == 'dateTime' ]]; then
      datatype="${datatype},dateTime"
    elif [[ "$col" =~ timestamp|dateStamp ]]; then
      datatype="${datatype},ignored"
    elif [[ "$col" =~ status|Direction|Units|base64Data|base16Data|devAddr|deviceAddDecoded|codeRate|ID ]]; then
      datatype="${datatype},string"
    else
      datatype="${datatype},field"
    fi
  done

  # Remove first comma
  datatype=${datatype:1}

  # Perform some edits on the CSV, and load into influx using influx write.

  # The replacements are for:
  #  1. Convert timestamp to RFC3339 format
  #  2. Remove prefix spaces (occurs in some files)
  #  3. Remove NANs
  #  4. Add trailing comma to lines with trailing comma, due to a bug in the CSV parser. This bug reads the first value
  #     of the next line as the last value of the current line, if there is no value specified in the CSV (i.e. it's
  #     empty)
  perl -pe 's/^([0-9-]+) ([0-9:.]+)/\1T\2Z/ and s/,\s+/,/g and s/NAN//g and s/,$/,,/' < "$filepath" | \
  influx write \
    --bucket sharedairdfw \
    --format csv \
    --header "#constant measurement,$sensor" \
    --header "#constant tag,macAddress,$mac" \
    --header "#datatype $datatype"
}

export -f loadCsvToInflux

# Run on all csv files found in the specified dir (recursive)
find "$1" -name '*.csv' -exec bash -c "loadCsvToInflux \"{}\"" \;
