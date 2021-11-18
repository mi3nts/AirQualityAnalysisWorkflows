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

RUN npm i -g zx csv-parse
ENV NODE_PATH=/usr/local/lib/node_modules

COPY --from=0 /workdir/main /usr/bin/backend-server
COPY frontend /home/node/frontend
COPY dataset /dataset
COPY scripts /scripts

WORKDIR /home/node/frontend

RUN npm i
RUN npm run build

CMD [ "sh", "-c", "/usr/bin/backend-server & npm run serve --host" ]