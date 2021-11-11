# 0: building backend
FROM golang:1.17.3-alpine3.14

WORKDIR /workdir

RUN go mod init mints-graphite-backend
RUN go get -u github.com/gofiber/fiber/v2

COPY backend/main.go .

RUN go mod tidy
RUN go build -o main main.go
RUN chmod +x main

# 1: for frontend and running backend app
FROM node:16.13.0-alpine3.14

COPY --from=0 /workdir/main /usr/bin/backend-server

CMD [ "/usr/bin/backend-server" ]