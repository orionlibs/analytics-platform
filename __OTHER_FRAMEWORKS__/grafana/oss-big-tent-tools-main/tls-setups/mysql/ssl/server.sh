docker run --name mysql --rm -p 3306:3306 --stop-timeout 1\
	-e MYSQL_ROOT_PASSWORD=p4ssw0rd\
	-e MYSQL_USER=john\
	-e MYSQL_PASSWORD=password\
	-e MYSQL_DATABASE=db\
	-v "$PWD/../../certs/server.crt":/etc/mysql/server.crt\
	-v "$PWD/../../certs/server.key":/etc/mysql/server.key\
	mysql\
	 --require-secure-transport=ON\
	 --ssl-cert=/etc/mysql/server.crt\
	 --ssl-key=/etc/mysql/server.key