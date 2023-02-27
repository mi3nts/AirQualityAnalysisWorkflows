The purpose of this folder is to contain a variety of jupyter template notebooks to be used to automatically generate analysis for our sensor network. The idea is as follows: 

- We will create template notebooks for each node type (Central Node, LoRa Node, UTD Node, etc...) for each type of analysis (daily, weekly, monthly, annual, etc...). 
- These notebooks will be templates, in the sense that the same notebooks can be run for different nodes by changing the `device_name` parameter used to query data from influxdb. 
- Once the templates are defined, we will use the python tool `papermill` to orchestrate workflows an enable evaluation of each analysis notebook at the command line 
- We can then set up crontrabs to submit notebooks for evaluation on a schedule via Europa
- We should back up the outputs by writing them to Dr. Simmons long term S3 storage system. 
