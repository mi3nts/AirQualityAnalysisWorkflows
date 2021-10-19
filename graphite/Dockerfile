FROM graphiteapp/graphite-statsd

ENTRYPOINT []

RUN apk add nodejs iproute2-ss
RUN npm i -g zx
RUN npm i csv-parse

# Start data ingestion
WORKDIR /data
RUN ./start.mjs

CMD ["/bin/sh"]