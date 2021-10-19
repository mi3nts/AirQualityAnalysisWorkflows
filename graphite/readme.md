Start up the grafana container (if you haven't already) with :
> docker run -d -p 3000:3000 grafana/grafana

Access it in the browser by either:
> Right clicking and selecting "Open in browser" (if in Visual Studio Code)
or
> Selecting the open in browser option (if on docker desktop)
or
> Locating the port with:
> docker volume ls
> cat grafana.ini
> locating the redis:, which will have the address that you can put in a browser
(I'm not quite sure about this last one. Thats how this tutorial: https://www.youtube.com/watch?v=UG_bZzhhnbc did it. But I wasn't able to get there)
The first two have worked for me.

Should have a login screen displaying the grafana logo, as well as a prompt for username and password.
Default username and password are both admin.
Next screen will ask you to change password.

Next screen will show "Welcome to Grafana".

Select "Data Sources/ Add your first data source"

Graphite should be the second option. (Prometheus is also there)

There will be an option for a url to load in data. 
