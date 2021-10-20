#!/bin/bash

RECORD=/prometheus/firstrun.record
CSVDATA=/prometheus/csv_data
if [ -f "$RECORD" ];
then
	echo "Booting up Prometheus."
	./prometheus --storage.tsdb.retention.time=5y --query.lookback-delta=5y --storage.tsdb.allow-overlapping-blocks
else
	if [ -d "$CSVDATA" ] 
	then
		echo "First run - ingesting data into Prometheus"
		python3 csvtoopenmetrics.py
		touch $RECORD
	else
		echo "First run, but CSV_DATA not found!"
	fi
fi

