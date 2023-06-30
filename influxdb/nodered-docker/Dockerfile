FROM docker.io/nodered/node-red

# Install modified node modules, including the influxdb support
COPY package.json .
RUN npm install --unsafe-perm --no-update-notifier --no-fund --only=production

# Move flows o custom-flows (not data/ because that will get overwritten)
COPY flows.json /data/flows.json
COPY flows_cred.json /data/flows_cred.json
COPY settings.js /data/settings.js
COPY id_lookup.csv /data/id_lookup.csv
COPY id_lookup_va.csv /data/id_lookup_va.csv
#ENV FLOWS="/custom-data/flows.json"
