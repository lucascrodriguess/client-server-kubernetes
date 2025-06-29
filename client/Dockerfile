FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod ./
COPY client.go ./

RUN go build -o client client.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/client .

CMD ["./client"]
