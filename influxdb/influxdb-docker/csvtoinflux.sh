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
  local part1
  local part2
  local header
  local datatype=''

  # Do not process if cannot parse part2 (sensor name or "Summary") & part1 (mac address or "LoraNodes") from file name
  filename=$(basename "$filepath")
  if [[ ! "$filename" =~ MINTS_[0-9A-Za-z]*_[0-9A-Za-z_]*_[0-9]{4}_[0-9]{2}_[0-9]{2}.csv ]]; then
    echo "Skipping because $filename did not match the required format."
    exit
  fi

  # Parse part2 name & part1 from title
  part1=$(echo "$filename" | perl -pe 's/MINTS_(.*)_(.*)_\d{4}_\d{2}_\d{2}.csv/\1/')
  part2=$(echo "$filename" | perl -pe 's/MINTS_(.*)_(.*)_\d{4}_\d{2}_\d{2}.csv/\2/')

  echo "Loading $part2 ($filepath) into InfluxDB"

  # Determine if this is a summary or individual sensor CSV
  if [[ "$part2" == 'Summary' ]]; then
    echo "Detected summarized CSV"


    # Build datatype string from column names
    # https://docs.influxdata.com/influxdb/v2.1/reference/syntax/annotated-csv/extended/
    header=$(head -1 "$filepath")
    IFS=',' read -ra headerArr <<< "$header"

    for col in "${headerArr[@]}"; do
      if [[ "$col" == 'sensorID' ]]; then
        datatype="${datatype},measurement"
      elif [[ "$col" == 'nodeId' ]]; then
        datatype="${datatype},tag"
      elif [[ "$col" == 'dateTime' ]]; then
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
    #  5. Change "nodeid" (case insensitive) to "location"
    perl -pe 's/^([0-9-]+) ([0-9:.]+)/\1T\2Z/ and s/,\s+/,/g and s/NAN//g and s/,$/,,/ and s/nodeid/location/i' < "$filepath" | \
    influx write \
      --bucket SharedAirDFW \
      --format csv \
      --header "#datatype $datatype"
  else
    echo "Detected single-sensor CSV"
    # Build datatype string from column names
    # https://docs.influxdata.com/influxdb/v2.1/reference/syntax/annotated-csv/extended/
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
    perl -pe 's/^([0-9-]+) ([0-9:.]+)/\1T\2Z/ and s/,\s+/,/g and s/NAN//g and s/,$/,,/' < "$filepath" | \
    influx write \
      --bucket SharedAirDFW \
      --format csv \
      --header "#constant measurement,$part2" \
      --header "#constant tag,location,$part1" \
      --header "#datatype $datatype"
  fi
}

export -f loadCsvToInflux

# Run on all csv files found in the specified dir (recursive)
find "$1" -name '*.csv' -exec bash -c "loadCsvToInflux \"{}\"" \;
