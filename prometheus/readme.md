# Workflow for ingesting data through prometheus

Here are the current steps to ingest CSV data into prometheus on your local machine. (Should also serve as steps to containerize the whole system)

Prerequisites:
Linux environment
Python 3.8.10 or above, with packages pandas (>=1.3.3)
Prometheus

1. Copy the required csv files into a directory called 'csv_data' (same as the beginning of the input_path in the script). No need to worry about the csvs being in subfolders.
2. Have prometheus installed in a folder called 'prometheus-2.30.0.linux-amd64' (same as the prometheus_path in the script)
3. Run the ingestion script as follows:

```console
python3 csvtoopenmetrics.py
```

3. This should ingest all the data and start up a prometheus server configured to interpret the new data

Querying instructions: