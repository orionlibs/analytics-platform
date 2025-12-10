docker run --name postgres --rm -p 5432:5432 --stop-timeout 1\
	-e POSTGRES_USER=john\
	-e POSTGRES_PASSWORD=password\
	-e POSTGRES_DB=db\
	-v "./pg_hba.conf":/etc/postgres/pg_hba.conf\
	-v "$PWD/../../certs/server_wronghost.crt":/etc/postgres/server.crt\
	-v "$PWD/../../certs/server_wronghost.key":/etc/postgres/server.key\
	postgres:16-alpine\
	postgres\
	-c hba_file=/etc/postgres/pg_hba.conf\
	-c ssl=on\
	-c ssl_cert_file=/etc/postgres/server.crt\
	-c ssl_key_file=/etc/postgres/server.key
