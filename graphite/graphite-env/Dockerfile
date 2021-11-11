FROM golang:1.17.3-alpine3.14

WORKDIR /go

# Build the deletion handler
COPY deletehandler.go /go
RUN go build -o deletehandler deletehandler.go
RUN chmod +x deletehandler

FROM graphiteapp/graphite-statsd

RUN mkdir /program
COPY --from=0 /go/deletehandler /program/deletehandler

ENTRYPOINT []

CMD [ "sh", "-c", "/program/deletehandler & /entrypoint" ]