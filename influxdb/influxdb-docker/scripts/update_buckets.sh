#!/bin/sh

# set -e

# run command to add bucket
influx bucket create -n open-aq -o $DOCKER_INFLUXDB_INIT_ORG -t $DOCKER_INFLUXDB_INIT_ADMIN_TOKEN
