FROM graphiteapp/graphite-statsd

WORKDIR /scripts

VOLUME [ "/igdata" ]

RUN apk add nodejs iproute2-ss
RUN npm i -g zx
RUN npm i csv-parse

COPY scripts /scripts
COPY dataset /dataset

# Start data ingestion
RUN ./build.mjs

ENTRYPOINT []

CMD ["./start.mjs"]
