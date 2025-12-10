docker run --name postgres --rm -p 5432:5432 --stop-timeout 1\
	-e POSTGRES_USER=john\
	-e POSTGRES_PASSWORD=password\
	-e POSTGRES_DB=db\
	-v "./pg_hba.conf":/etc/postgres/pg_hba.conf\
	postgres:16-alpine\
	postgres\
	-c hba_file=/etc/postgres/pg_hba.conf
