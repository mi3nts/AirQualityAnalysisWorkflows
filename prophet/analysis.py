import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from prophet import Prophet
#from prometheus_api_client import PrometheusConnect
import datetime as dt
from prometheus_api_client import PrometheusConnect, MetricSnapshotDataFrame, MetricRangeDataFrame
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m',
                    nargs = '+',
                    metavar='Metric', 
                    type=str, 
                    help='Name of the metric to graph.', 
                    required = True)
parser.add_argument('-start', metavar='Start Date', type=str, help='Start date of the graph (format: DD/MM/YYYY).')
parser.add_argument('-end', metavar='End Date', type=str, help='End date of the graph (format: DD/MM/YYYY).')
args = parser.parse_args()

metricList = args.m
if metricList == None:
    print("Missing --m (metric) argument: this is required.")
    exit()
    
start_datetime = args.start
end_datetime = args.end

if start_datetime == None:
    print("Missing -start (start date) argument: this is required.")
    exit()
if end_datetime == None:
    print("Missing -end (end date) argument: this is required.")
    exit()

start_datetime = dt.datetime.strptime(start_datetime,"%d/%m/%Y")
end_datetime = dt.datetime.strptime(end_datetime,"%d/%m/%Y")
    
prom = PrometheusConnect(disable_ssl=True)      #establish connection w/ prometheus server
my_label_config = {'id': '47cb5580002e004a'}    #use node id ...

"""
Need to iterate over the metric list to get the data
append the y columsn to each ofther for the quick analysis text file,
o.w. keep everything else the same for the predictions: i guess those will have to be in a list too.

so i think 2 sets of dataframes. one for all the metrics together, 
and another that is a list of dataframes, formatted as it was before so that the predictions can be outputted
"""

listOfMetricsForPredictions = []
analysisDF = None

# -------------------------------- Generating the dataframes --------------------------------

#query data for metric_name for the last 1200 day(s)
for metric in metricList:
    metric_data = prom.get_metric_range_data(
        metric_name=metric,
        label_config=my_label_config,
        start_time=start_datetime,
        end_time=end_datetime,
    )

    metric_df = MetricRangeDataFrame(metric_data)       #convert data to data frame

    #format data for prophet predictions
    metric_df['timestamp'] = metric_df.index
    metric_df = metric_df.rename({'timestamp': 'ds', 'value': 'y'}, axis='columns')
    metric_df['ds'] = metric_df['ds'].apply(lambda x: dt.datetime.fromtimestamp(x))

    if metric == metricList[0]:
        analysisDF = metric_df.drop(columns = ["__name__"])
        analysisDF = analysisDF.rename(columns={'y': metric})
        analysisDF[metric] = metric_df.y.astype("float")
    else:
        analysisDF[metric] = metric_df.y.astype("float")

    listOfMetricsForPredictions.append(metric_df)

# --------------------------------- Analysis ----------------------------------

with open("analysis.txt", 'w') as f:
    for metric in metricList:
        writeThisToFile = str(metric + " Analysis" + '\n')
        f.write(writeThisToFile)
        description = str(analysisDF[metric].describe()) + '\n\n'
        print(description)
        f.write(description)

# -------------------------------- Predictions --------------------------------
metricCounter = 0
figs = []
for dataframes in listOfMetricsForPredictions:
    m = Prophet()       #intialize prophet object
    m.fit(dataframes)   #fit the data

    #creates future dataframe
    future = m.make_future_dataframe(periods = 40)

    #make predictions
    forecast = m.predict(future)

    #trend
    fig1 = m.plot(forecast)

    #yearly, weekly, and trend seasonality
    fig2 = m.plot_components(forecast)

    #saves plots in current working directory
    figs.append(fig1)
    figs.append(fig2)

# saving plots in the figures folder of the current working directory
figCounter = 0
for fig in figs:
    name = 'figures/' + str(metricList[int(figCounter/2)]) + str(figCounter)
    fig.savefig(name)
    figCounter += 1