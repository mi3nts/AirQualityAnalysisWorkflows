import pandas as pd
from prophet import Prophet
#from prometheus_api_client import PrometheusConnect
import datetime as dt
from prometheus_api_client import PrometheusConnect, MetricSnapshotDataFrame, MetricRangeDataFrame
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', metavar='Metric', type=str, help='Name of the metric to graph.')
parser.add_argument('-start', metavar='Start Date', type=str, help='Start date of the graph (format: DD/MM/YYYY).')
parser.add_argument('-end', metavar='End Date', type=str, help='End date of the graph (format: DD/MM/YYYY).')
args = parser.parse_args()

metric = args.m
if metric == None:
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

#query data for metric_name for the last 1200 day(s)
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


df = metric_df      #takes dataframe and sets it to prometheus dataframe
m = Prophet()       #intialize prophet object
m.fit(df)           #fit the data

#creates future dataframe
future = m.make_future_dataframe(periods = 40)

#make predictions
forecast = m.predict(future)

#trend
fig1 = m.plot(forecast)

#yearly, weekly, and trend seasonality
fig2 = m.plot_components(forecast)

#saves plots in current working directory
fig1.savefig('my_figure.png')
fig2.savefig('my_figure2.png')


