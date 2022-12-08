FROM python:3.8.10 AS installQuarto

#Install Prereqs
RUN apt-get update \ 
    && apt-get install -y gcc \ 
    && apt-get install -y curl \ 
    && apt-get install -y gdebi-core

#Install Quarto
RUN curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb 
RUN gdebi --non-interactive quarto-linux-amd64.deb 

#Python dependencies
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
RUN pip install numpy \
    && pip install pandas \
    && pip install plotly \
    && pip install jupyter \
    && pip install influxdb-client[extra] \
    && pip install python-dotenv

#Copies Automated_Reports Folder
COPY automated_reports /automated_reports


# #Render Automated Reports
RUN quarto render automated_reports

# #Small http server to host website
# FROM ghcr.io/openfaas/of-watchdog AS server

# FROM alpine

# #Copy Folders
# RUN mkdir /site
# COPY --from=installQuarto /automated_reports/_site /site
# COPY --from=server /fwatchdog .

# #Start server
# ENV mode="static"
# ENV static_path="/site"
# CMD ["./fwatchdog"]


