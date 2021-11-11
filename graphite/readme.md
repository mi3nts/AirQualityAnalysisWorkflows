# Instructions on how to set up

## Building and starting the containers

Put a few CSV files in the `webui/dataset` folder. Then, run

```bash
docker-compose up -d
```

This will take a while, as the initial build of the Graphite image will do the ingestion. Once it's up, access the web UI at `localhost:8080` and Grafana at `localhost:3000`.

## Data ingestion & deletion

Right now the web UI is relatively bare-bones, but you can do the most important task here, and that is ingestion. In the future I will make the dataset folder bindmounted, so you can ingest data you *just* put in the folder.

- Check the status of the ingestion engine with the `Status` button. Make sure it's `idle`.
- Start ingestion by clicking on the `Ingest` button. The status should say `ingesting` now and should take a while to finish. In the future, I will make this status update in real-time, but for now, please routinely check if the status returns again to `idle`. That's when the ingestion has finished.
- If you want to remove the ingested data for any reason, click on `Delete`.

## Setting up a dashboard

Access Grafana at `localhost:3000` and log in with the default credentials of `admin:admin`.

Next, hover over the **Configuration** submenu (cog wheel) and click on **Data Sources**, then **Add data source**. Choose **Graphite**, and in the URL field type `graphite`. Then at the bottom of the page click on **Save & test**. It should say "Data source is working".

Then hover over the **Create** submenu (plus icon) and click on **Dashboard**, then click on **Add an empty panel**. At the lower half of the screen, you can name your query anything instead of `A`; you can select your metrics. The data should be under `data`, from which you can choose among `C2H5OH`, `C3H8`, `C4H10`, etc. or all of them by selecting `*`. Next, you'll need to select a time range for your graph, which can be accessed with the clock icon in the upper right:

![time range selection](./readme_time-range.png)

If you're done, click **Apply**. Then click on **Save dashboard** (save icon) in the top right. Name your dashboard however you like.

## Stopping the containers

Run `docker compose down` to stop the 2 containers. The dashboard information should be persisted under the `grafana-data` volume.
