import pandas
import glob
import os
from datetime import datetime
import pandas as pd
from pathlib import Path
import subprocess

# File name specification
input_path = '/csv_data/**/*.csv'
output_path = '/openmetrics_data/'
prometheus_path = '/prometheus-2.30.0.linux-amd64/'


# remember what files are new
new_files = []

# Iterate over the files in the input path
for file in glob.iglob(input_path):
    csv_df = pd.read_csv(file)
    csv_df.drop_duplicates(inplace=True, ignore_index=True)
    # Remove missing rows/corrupted lines
    csv_df.dropna(subset=['dateTime'], inplace=True)
    base_file_name = Path(file).stem

    # Do not recreate files already converted to openmetrics
    # Skip to next file in input path
    if Path(output_path+base_file_name).is_file():
        continue

    new_files.append(output_path + base_file_name)
    openmetrics_file = open(output_path + base_file_name, "w")
    # Convert date time to UNIX time
    csv_df['dateTime'] = csv_df['dateTime'].apply(lambda x: int(datetime.fromisoformat(x).timestamp()))

    # Sort the rows by dateTime
    csv_df.sort_values(by=['dateTime'], inplace=True)

    # Iterate over columns of the data frame
    for column in csv_df:
    	# Don't encode dateTime or id as metrics
        if column == 'dateTime' or column == 'id':
            continue

        # Extract subset (to create the current metric from)
        sub_df = csv_df[[column, 'dateTime', 'id']]

        # Use the csv column name as the metric name (remove any - characters for formatting)
        metric_name = column
        metric_name = metric_name.replace('-', '')

        # Declare a new metric with the given name, and of type gauge
        openmetrics_file.write('# TYPE ' + metric_name + ' gauge\n')

        # Iterate over all the rows of the current subset
        for index, row in sub_df.iterrows():
        	# Include an entry if the metric value is present
            if pd.isna(row[column]) == False:
                openmetrics_file.write(metric_name + '{id=\"' + str(row['id']) + '\"} ' + str(float(row[column])) + ' ' + str(row['dateTime']) + '\n')
    # Denote the end of file            
    openmetrics_file.write('# EOF')

    openmetrics_file.close()

# Iterate over all new openmetric format files
for file in new_files:
    print('Ingesting file ' + file)
    # Ingest the current file using promtool
    ingest_file = subprocess.run([prometheus_path + 'promtool', 'tsdb', 'create-blocks-from', 'openmetrics', file, prometheus_path + 'data'])
    ingest_file.check_returncode()
