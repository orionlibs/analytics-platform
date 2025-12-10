docker run --name mysql --rm -p 3306:3306 --stop-timeout 1\
	-e MYSQL_ROOT_PASSWORD=p4ssw0rd\
	-e MYSQL_USER=john\
	-e MYSQL_PASSWORD=password\
	-e MYSQL_DATABASE=db\
	mysql --skip-ssl --default-authentication-plugin=mysql_native_password