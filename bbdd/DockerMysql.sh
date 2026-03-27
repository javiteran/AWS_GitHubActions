# Crear dockers publicos en el puerto 3306
docker run -d --name mysqlalumnosclases -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password mysql:latest

#Verificar si está el docker funcionando
 docker exec -it mysqlalumnosclases bash

#Instalar el cliente mysql para poder ejecutar comandos mysql desde la terminal 
apt update -y
apt install mysql-client -y

# Crear base de datos y usuario en una sola ejecucion no interactiva
mysql -u root -ppassword -P 3306 -h 0.0.0.0 <<'SQL'
CREATE DATABASE IF NOT EXISTS AlumnosClases;
FLUSH PRIVILEGES;
SQL

# Crear el usuario y otorgarle permisos
#CREATE USER IF NOT EXISTS 'usuario'@'%' IDENTIFIED BY 'password';
#GRANT ALL PRIVILEGES ON AlumnosClases.* TO 'usuario'@'%';


# Salir del mysql y volver a entrar con el usuario creado para verificar que funciona
mysql -u usuario -ppassword -h 0.0.0.0

# Crear las tablase de la bases de datos
mysql -u usuario -ppassword -h 0.0.0.0 AlumnosClases < bbdd/database.sql

# La aplicación crea las tablas de la base de datos si no están creadas.