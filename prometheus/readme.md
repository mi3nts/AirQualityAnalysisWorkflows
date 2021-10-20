# Workflow for ingesting data through prometheus

How to run the dockerfile for prometheus?

Prerequisites:
Docker

1. Change directory to this folder.
2. Run the following commands

```console
docker build -t mints/prometheus .
docker run -d -p 9090:9090 mints/prometheus
```

3. This should ingest all the data in the csv_data folder and start up a prometheus server configured to interpret the new data

**Note:** If we want to ingest more data into prometheus, clear the csv_data folder of the old data. Copy the new csv files into csv_data. Do steps 1 to 3.

Querying instructions:
