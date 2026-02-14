# Crear dockers publicos en el puerto 3306
docker run -d --name mysqlalumnosclases -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password mysql:latest

#Verificar si está el docker funcionando
# docker exec -it mysqlalumnosclases bash

# Conectarme al mysql
sudo mysql -u root -ppassword -P 3306 -h 0.0.0.0

# Crear la base de datos y el usuario
create database AlumnosClases;

CREATE USER 'usuario'@'172.17.0.1' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON AlumnosClases.* TO 'usuario'@'172.17.0.1';

# Salir del mysql y volver a entrar con el usuario creado para verificar que funciona
mysql -u usuario -ppassword -h 0.0.0.0

# Crear las tablase de la bases de datos
mysql -u usuario -ppassword -h 0.0.0.0 AlumnosClases < database.sql
