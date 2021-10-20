# Workflow for setting up Graphite and ingesting data through CSV

Put a few CSVs in the `dataset` folder.

`cd` into this directory with your terminal and then

```bash
docker build -t org.mints.graphite .
```

That should build an image named `graphite-mints` with all CSVs in the `dataset` folder.

```bash
docker run -d -p 80:80 -p 2003-2004:2003-2004 -p 2023-2024:2023-2024 -p 8125:8125/udp -p 8126:8126 -it org.mints.graphite
```

That should get a container running with your ingested data. Adjust the time range to that of the data and hopefully that gets displayed on-screen.
