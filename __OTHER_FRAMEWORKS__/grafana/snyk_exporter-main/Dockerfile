FROM golang:1.21.0 as builder

WORKDIR /src

ENV CGO_ENABLED=0
ENV GOOS=linux

RUN apt-get update
RUN apt-get install -y ca-certificates

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

RUN go build -o /tmp/snyk_exporter

FROM scratch

COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /tmp/snyk_exporter /

USER 65534

ENTRYPOINT ["/snyk_exporter"]
