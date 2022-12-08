#Small http server to host website
FROM ghcr.io/openfaas/of-watchdog AS server

FROM alpine

#Copy Folders
COPY --from=server /fwatchdog .

#Start server
ENV mode="static"
ENV static_path="/site"
CMD ["./fwatchdog"]


