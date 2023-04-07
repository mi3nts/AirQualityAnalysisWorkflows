FROM continuumio/miniconda3:latest

# install eccodes
RUN conda install -c conda-forge eccodes

# install python library
RUN pip3 install eccodes


# copy uv wind script into tmp
COPY ./conda_scripts/uvwind.sh /tmp/
# change mode to executable
RUN chmod +rx /tmp/uvwind.sh
# run script on startup
ENTRYPOINT ["/bin/bash", "/tmp/uvwind.sh"]