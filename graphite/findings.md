# Workflow for setting up Graphite and ingesting data through CSV

Here are my current findings on how to set up Graphite and ingesting CSV data.

First, make sure you are in a Linux environment with Docker and Node.js installed. Also, the Node.js packages `zx` and `csv-parse` are also needed to run the script. Make sure it is installed globally, i.e. you installed it with `npm i -g zx`.

Next, run Graphite on Docker:

```console
docker run -d \
 --name graphite \
 --restart=always \
 -p 80:80 \
 -p 2003-2004:2003-2004 \
 -p 2023-2024:2023-2024 \
 -p 8125:8125/udp \
 -p 8126:8126 \
 graphiteapp/graphite-statsd
```

This will spin up Graphite. Now run the following to ingest the `test.csv` file into Graphite, which was originally `475a5fe3003e0023_2020-10-26.csv` in the given dataset zip:

```console
zx ./ingest.mjs --csv ./test.csv
```

Since this CSV is quite small, ingestion should not take more than a few minutes on a decently fast computer.

Next, open `localhost` (port 80) on a browser, and set the time frame to include 10/26/2020-10/27/2020, preferably small enough so we can actually see the data points in the visualization.

## In progress

Will be writing up how to properly build and launch the container.
