# Práctica 05: Docker Compose y MariaDB

## 1. Descripción del proyecto

Esta práctica consiste en desplegar una aplicación web Flask conectada a una base de datos MariaDB mediante Docker Compose, utilizando Nginx como proxy inverso.

También se comprueba la persistencia de los datos y se realizan operaciones de copia de seguridad y restauración.

## 2. Tecnologías utilizadas

- **AWS EC2:** servidor Ubuntu donde se despliega el proyecto.
- **Docker:** ejecución de aplicaciones mediante contenedores.
- **Docker Compose:** gestión de los tres servicios.
- **Flask:** aplicación web desarrollada en Python.
- **Gunicorn:** servidor de aplicaciones Python.
- **MariaDB:** almacenamiento de las tareas.
- **Nginx:** proxy inverso que recibe las peticiones HTTP.

## 3. Arquitectura

El proyecto utiliza tres contenedores:

1. **Nginx:** recibe las peticiones del navegador por el puerto 8080 del servidor y las reenvía a Flask.
2. **Flask:** consulta las tareas almacenadas en MariaDB y genera una tabla HTML.
3. **MariaDB:** almacena los datos en un volumen persistente de Docker.

Los servicios se comunican mediante una red interna de Docker Compose.

## 4. Estructura del proyecto

- `app/`: aplicación Flask, dependencias y Dockerfile.
- `nginx/`: configuración del proxy inverso.
- `database/`: scripts SQL para crear la tabla e insertar los datos iniciales.
- `backups/`: copia de seguridad `backup.sql`.
- `capturas/`: evidencias del desarrollo de la práctica.
- `docs/`: diagrama de arquitectura.
- `docker-compose.yml`: definición de los servicios, red y volumen.

## 5. Despliegue en AWS EC2

El proyecto se comprimió en un archivo ZIP y se transfirió a la instancia EC2 mediante SCP.

Después se descomprimió en `/opt/practica05`.

Para construir y arrancar los servicios se ejecutó:

`sudo docker compose up -d --build`

Para comprobar el estado de los contenedores:

`sudo docker compose ps`

Se verificó que MariaDB estaba en estado `healthy` y que Flask y Nginx estaban funcionando.

## 6. Acceso a la aplicación

La aplicación se publicó mediante Nginx en el puerto **8080**, para evitar conflictos con el servidor Nginx instalado en la práctica anterior.

Dirección utilizada:

`http://44.208.21.231:8080`

Se configuró una regla de entrada en el grupo de seguridad de AWS para permitir el acceso al puerto 8080.

La aplicación muestra las tareas almacenadas en la base de datos.

## 7. Persistencia de datos

MariaDB utiliza el volumen de Docker `datos_mariadb`, que permite conservar la información incluso al eliminar y volver a crear los contenedores.

Para comprobarlo, se insertó una tarea adicional llamada **Prueba de persistencia**.

Después se detuvieron los contenedores mediante:

`sudo docker compose down`

Y se volvieron a iniciar:

`sudo docker compose up -d`

Al consultar nuevamente la base de datos, se comprobó que las **6 tareas** seguían almacenadas.

## 8. Copia de seguridad

Se generó un archivo `backup.sql` utilizando `mariadb-dump`.

Esta copia contiene la estructura y los datos de la base de datos `practica05javier`.

El archivo se guardó en la carpeta `backups/` y también se descargó al ordenador local.

## 9. Simulación de pérdida y restauración

Para simular una pérdida de información, se eliminaron los registros de la tabla `tareas`.

Después se restauró la base de datos utilizando el archivo `backup.sql`.

Finalmente, se realizó una consulta SQL y se comprobó que las **6 tareas** habían sido recuperadas correctamente.

## 10. Conclusiones

La práctica permite comprobar cómo Docker Compose facilita el despliegue de una aplicación formada por varios servicios.

Se ha verificado que:

- Nginx puede actuar como proxy inverso de Flask.
- Flask puede consultar datos de MariaDB.
- Los volúmenes permiten mantener los datos entre reinicios.
- Las copias de seguridad permiten recuperar la información ante una pérdida de datos.

En un entorno de producción sería recomendable proteger las contraseñas mediante secretos o variables de entorno gestionadas de forma segura y configurar HTTPS con un certificado válido.