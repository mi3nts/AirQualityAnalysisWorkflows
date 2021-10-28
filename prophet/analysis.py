import pandas as pd
from prophet import Prophet
#from prometheus_api_client import PrometheusConnect
import datetime as dt
from prometheus_api_client import PrometheusConnect, MetricSnapshotDataFrame, MetricRangeDataFrame

prom = PrometheusConnect(disable_ssl=True)      #establish connection w/ prometheus server
my_label_config = {'id': '47cb5580002e004a'}    #use node id ...

#query data for metric_name for the last 1200 day(s)
metric_data = prom.get_metric_range_data(
    metric_name='P2_ratio',
    label_config=my_label_config,
    start_time=(dt.datetime.now() - dt.timedelta(days=1200)),
    end_time=dt.datetime.now(),
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


