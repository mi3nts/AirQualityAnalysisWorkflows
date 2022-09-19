FROM docker.io/ubuntu

#Copies Automated_Reports Folder
COPY ./ /automated_reports

#Install Curl
RUN apt-get update \ 
    && apt-get install -y gcc \ 
    && apt-get install -y curl

#Install Quarto
RUN curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb \
    && apt-get install -y gdebi-core \
    && gdebi quarto-linux-amd64.deb \
    && /usr/local/bin/quarto check

#Run Automated Reports
RUN quarto preview automated_reports
    

