# Instructions

## Setup

Prerequisites:
Docker, Some csv data in the `csv_data` folder

1. Change the working directory to this directory
2. Run:
```console
docker-compose up -d
```
3. This will build and start two containers, one for the prometheus server (with the data put in `csv_data` already ingested) and one for Grafana.
4. Access prometheus at `localhost:9090` and Grafana at `localhost:3000`

## Querying instructions (Prometheus):

1. Go to `localhost:9090/graph`. You should see a screen like this:

![image](https://user-images.githubusercontent.com/60592738/138327376-0cb13fe6-3cb3-4cca-8059-fe828a9b8c47.png)

3. Test queries and see results in the table or graph.

example:

![image](https://user-images.githubusercontent.com/60592738/138327588-6af7fff8-bc0f-41fc-a86d-d56b822c39bd.png)

(Example query formats:
- All time series for a given metric: `metric_name`
- All time series for a given metric for a given node id: `metric_name{id="node_id"}`
- A range of time series for a given metric for a given node id: `metric_name{id="node_id"}[time_duration]`

(`metric_name` can take values like `NH3`, `CO2`, `P1_conc`, `P1_lpo` etc. (corresponding to the columns in the csv data), `node_id` can take values like `47cb5580002e004a` (corresponding to the node id in the csv data), `time_duration` can take values like `5m` (5 minutes), `2y` (2 years) etc.

More querying information: https://prometheus.io/docs/prometheus/latest/querying/basics/

## Grafana Dashboard instructions:

1. Go to `localhost:3000`. You should see a screen like this:

![Screenshot (204)](https://user-images.githubusercontent.com/60592738/142471407-669b6b1f-3e28-474e-9ae2-fecfe7fee189.png)

2. Login using username: `admin`, password: `admin` (skip the password change prompt)
3. Hover over the cogwheel (Configuration menu) and select Data Sources, then click on Add data source. 
4. Select Prometheus (under Time Series Databases) as the data source type, and put `prometheus:9090` in the URL field
5. Click on Save & test. It should say "Data source is working"
6. Hover over the plus sign (Create Menu) and select Dashboard
7. Click on Add panel, then Add an empty panel. You should see a screen like this:

![Screenshot (205)](https://user-images.githubusercontent.com/60592738/142473087-d9f10adb-3770-48c6-9222-178fca50c641.png)

8. Populate the query/queries (same format as in the previous section), panel titles, time ranges, graph styles (units, thresholds etc.) as needed. Click Apply. Add more panels if needed, click on the save icon to save the dashboard.

example:

![Screenshot (206)](https://user-images.githubusercontent.com/60592738/142475802-ff60f9f1-7b58-4ac2-94e7-e35d97aff255.png)

## Shutdown

Run `docker-compose down` to stop and remove the containers. 

(Run `docker-compose stop` to stop them without deleting, can now be restarted using `docker-compose start`)
