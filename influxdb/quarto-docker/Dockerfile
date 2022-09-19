FROM docker.io/ubuntu

#Copies Automated_Reports Folder
COPY automated_reports /automated_reports

#Install Prereqs
RUN apt-get update \ 
    && apt-get install -y gcc \ 
    && apt-get install -y curl \ 
    && apt-get install -y gdebi-core

#Install Quarto
RUN curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb 
RUN gdebi --non-interactive quarto-linux-amd64.deb 

#Run Automated Reports
#RUN quarto preview automated_reports
    

