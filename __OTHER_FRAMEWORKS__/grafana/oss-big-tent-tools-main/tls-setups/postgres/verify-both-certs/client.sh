psql "host=localhost user=john password=password dbname=db sslmode=verify-full sslrootcert=$PWD/../../certs/ca_server.crt sslcert=$PWD/../../certs/client.crt sslkey=$PWD/../../certs/client.key"
