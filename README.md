# AirQualityAnalysisWorkflows


# Container Setup 

1. Navigate to `/influxdb`. Copy `.example.env` to `.env` and edite the file with appropriate paths for your machine and desired settings. Contact *John Waczak* or *Lakitha Weijeratne* to obtain the necessary credentials files. 
2. Build the container via `docker-compose up --build`. If you want the container to remain on in the background, instead run `docker-compose up --build -d`. 
3. Sign into the grafana dashboards and copy the contents of each file in `/influxdb/grafana-docker/dashboards` to populate the list of available dashboards. 
4. To turn of the containers, run `docker-compose down` 

# Automate Reports 

1. Install [quarto](https://quarto.org/) on your device 
2. In the root of the directory run `quarto render automated_reports`
3. View the output in `/automated_reports/_site`. 
4. While developing, use `quarto preview automated_reports` to see the pages update live in your browser as you work on the source files. 


# Import Notes for Deployment on MDASH 
See [this thread](https://stackoverflow.com/questions/42529211/how-to-rebuild-and-update-a-container-without-downtime-with-docker-compose) for updating the containers. **DO NOT** do `podman-compose down` as this will remove the volumes for influxdb. Instead, simply running `podman-compose up -d` should rebuild any containers whose configuration files have changed. 

Also, [this link](https://linuxhandbook.com/update-docker-container-zero-downtime/)
