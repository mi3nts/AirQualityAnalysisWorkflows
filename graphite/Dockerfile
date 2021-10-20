FROM graphiteapp/graphite-statsd

RUN apk add nodejs iproute2-ss
RUN npm i -g zx
RUN npm i csv-parse

COPY scripts /scripts
COPY dataset /dataset

# Start data ingestion
WORKDIR /scripts
RUN ./start.mjs

CMD ["/entrypoint"]