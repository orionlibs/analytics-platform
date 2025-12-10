# prerequisites:

- to run the `client.sh` scripts, you need the `psql` tool
  - on MacOS, you can install it with `brew install libpq`
    - it will not be added to your `PATH` by default, read the instructions displayed from the above command to fix that.
- the `gen_certs.sh` scripts needs to refer to the `openssl.conf` file. on MacOS, the system's provided openssl package is not good enough, so the script assumes you have `openssl@3` installed using Homebrew (you probably have it already). If you are on a different platform, please adjust the script to refer to your location of `openssl.conf`
- always run the scripts directly from the directory where they are, otherwise they may not find related files. so:
  - good: `./server.sh`
  - bad: `a/b/c/server.sh`
- before running any of the scripts, please run `gen_certs.sh` to generate the certificates needed for the scenarios.

# scenarios

For every scenario described below we provide two scripts:

- `server.sh`, starts a database server with the given scenario using `docker`
- `client.sh`, connects to the database-server using a command-line tool

## nocrypt

no encryption

grafana:

- Database name: `db`
- Username: `john`
- Password: `password`
- TLS/SSL Mode: `disable`

## ssl

server only allows SSL connections.

grafana:

- Database name: `db`
- Username: `john`
- Password: `password`
- TLS/SSL Mode: `require`

## verify-server-cert-ignore-host

server only allows SSL connections. client verifies the server certificate's certificate chain. it does not verify the hostname in the certificate.

grafana:

- Database name: `db`
- Username: `john`
- Password: `password`
- TLS/SSL Mode: `verify-ca`
- TLS/SSL Root Certificate: paste the content from `certs/ca_server.crt`

## verify-server-cert

server only allows SSL connections. client verifies the server certificate (both the certificate chain, and the hostname in the certificate)

NOTE: you need to connect to the database with the url `localhost`

grafana:

- Database name: `db`
- Username: `john`
- Password: `password`
- TLS/SSL Mode: `verify-full`
- TLS/SSL Root Certificate: paste the content from `certs/ca_server.crt`

## verify-client-cert

server only allows SSL connections, with client certificates provided.

grafana:

- Database name: `db`
- Username: `john`
- Password: `password`
- TLS/SSL Mode: `require`
- TLS/SSL Client Certificate: paste content from `certs/client.crt`
- TLS/SSL Client Key: paste content from `certs/client.key`

## verify-both-certs

server only allows SSL connections, with client certificates provided. client verifies the server certificate (both the certificate chain, and the hostname in the certificate)

NOTE: you need to connect to the database with the url `localhost`

grafana:

- Database name: `db`
- Username: `john`
- Password: `password`
- TLS/SSL Mode: `verify-full`
- TLS/SSL Root Certificate: paste the content from `certs/ca_server.crt`
- TLS/SSL Client Certificate: paste content from `certs/client.crt`
- TLS/SSL Client Key: paste content from `certs/client.key`

# docs

- https://www.postgresql.org/docs/current/libpq-ssl.html
- https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
- https://www.postgresql.org/docs/current/ssl-tcp.html
- https://www.postgresql.org/docs/14/libpq-connect.html#LIBPQ-PARAMKEYWORDS
