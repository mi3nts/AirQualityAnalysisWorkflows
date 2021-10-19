To build this dockerfile:

1. Change directory to this folder.
2. Run "docker build -t mints/prometheus ." to build the image 
3. Run "docker create -p 9090:9090 --name mints_container mints/prometheus" to create a container of the image 
4. Run "docker cp csv_data mints_container:/prometheus/csv_data" to copy the csv_data into the volume (you may need to change directory to csv_data parent directory)
5. Run "docker start mints_container" to start the container (or you can use the docker desktop GUI to do this easier)

The container should automatically ingest data on the first run.
