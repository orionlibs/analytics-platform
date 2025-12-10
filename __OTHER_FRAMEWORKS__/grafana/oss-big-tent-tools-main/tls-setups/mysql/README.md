# prerequisites:

- to run the `client.sh` scripts, you need the `mysql` tool
  - on MacOS, you can install it with `brew install mysql-client`
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

- Database name `db`
- Username: `john`
- Password: `password`

## ssl

server only allows SSL connections.

grafana: not possible currently, see https://github.com/grafana/grafana/issues/63429

## verify-server-cert

server only allows SSL connections. client verifies the server certificate.

grafana:

- Database name `db`
- Username: `john`
- Password: `password`
- With CA Cert: `on`
- TLS/SSL Root Certificate: paste content from `certs/ca_server.crt`

## verify-client-cert

server only allows SSL connections, with client certificates provided.

grafana: not possible currently, see https://github.com/grafana/grafana/issues/77449

## verify-both-certs

server only allows SSL connections, with client certificates provided. client verifies the server certificate.

grafana:

- Database name `db`
- Username: `john`
- Password: `password`
- Use TLS Client Auth: `on`
- With CA Cert: `on`
- TLS/SSL Client Certificate: paste content from `certs/client.crt`
- TLS/SSL Client Key: paste content from `certs/client.key`
- TLS/SSL Root Certificate: paste content from `certs/ca_server.crt`

# docs

- https://dev.mysql.com/doc/refman/8.0/en/connection-options.html#option_general_ssl
- https://dev.mysql.com/doc/refman/8.0/en/connection-options.html#option_general_ssl-mode
- https://dev.mysql.com/doc/refman/8.0/en/sha256-pluggable-authentication.html
- https://dev.mysql.com/blog-archive/howto-connect-to-mysql-using-a-client-certificate/
