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

1. Have the docker container running
2. Go to localhost:9090/graph. You should see a screen like this:

![image](https://user-images.githubusercontent.com/60592738/138327376-0cb13fe6-3cb3-4cca-8059-fe828a9b8c47.png)

3. Test queries and see results in the table or graph.

example:

![image](https://user-images.githubusercontent.com/60592738/138327588-6af7fff8-bc0f-41fc-a86d-d56b822c39bd.png)

