FROM docker.io/python:latest


#Install Prereqs
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    pandoc-citeproc \
    curl \
    gdebi-core \
    && rm -rf /var/lib/apt/lists/*

#Python dependencies
RUN pip install numpy \
    && pip install pandas \
    && pip install plotly \
    && pip install jupyter \
    && pip install influxdb-client[extra] \
    && pip install python-dotenv


#Install Quarto
RUN curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb
RUN gdebi --non-interactive quarto-linux-amd64.deb

#Copies Automated_Reports Folder
COPY automated_reports /automated_reports
COPY .env /automated_reports/env_file

RUN quarto check jupyter

# #Render Automated Reports
# RUN quarto render automated_reports --to html
