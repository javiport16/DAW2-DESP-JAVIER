# Práctica 04. Despliegue en AWS EC2 con HTTPS

## 1. Introducción

En esta práctica se ha desplegado una aplicación web Flask en una
instancia Amazon EC2 con Ubuntu Server 24.04 LTS. La aplicación se
ejecuta mediante Gunicorn dentro de un contenedor Docker y Nginx actúa
como proxy inverso. Finalmente, se ha configurado HTTPS mediante un
certificado SSL/TLS autofirmado.

## 2. Objetivos

-   Crear y configurar una instancia EC2.
-   Automatizar la preparación inicial mediante User Data.
-   Acceder a la máquina virtual mediante SSH.
-   Desplegar una aplicación Flask en Docker.
-   Ejecutar Flask con Gunicorn.
-   Configurar Nginx como proxy inverso.
-   Habilitar HTTPS con un certificado SSL/TLS.
-   Consultar los registros de Nginx y Gunicorn.

## 3. Arquitectura

El recorrido de una petición es:

**Navegador → Internet → Nginx (HTTPS, puerto 443) → Gunicorn (puerto
5000) → Flask**

Nginx también escucha en el puerto 80 y redirige las peticiones HTTP a
HTTPS. Gunicorn se ejecuta dentro del contenedor Docker `flask-app`.

El diagrama se encuentra en `docs/arquitectura.png`.

## 4. Creación de la instancia EC2

Se creó una instancia con estos parámetros: - Nombre:
`practica04-flask` - Sistema operativo: Ubuntu Server 24.04 LTS - Tipo:
`t2.micro` - Usuario SSH: `ubuntu` - Clave de acceso: `practica04.pem`

El grupo de seguridad debe permitir SSH (22) desde la IP del
administrador, HTTP (80) y HTTPS (443). El puerto 5000 no debe quedar
expuesto públicamente en la configuración final, ya que el acceso web se
realiza a través de Nginx.

## 5. Automatización con User Data

Se proporcionó el script `configuracion/user-data.sh` durante el
lanzamiento de EC2. En esta ejecución, Cloud-init informó de un fallo en
el módulo `scripts_user`. Por ese motivo, Docker, Git y curl se
instalaron y verificaron manualmente después de iniciar sesión por SSH.

La incidencia se comprobó mediante `/var/log/cloud-init-output.log` y
`cloud-init status --long`. La instalación manual permitió continuar con
el despliegue. Por tanto, no se debe afirmar que la instalación
automática de Docker quedó verificada correctamente.

## 6. Aplicación Flask y Docker

Se copiaron `app.py`, `requirements.txt` y `Dockerfile` a
`/opt/practica04/aplicacion`.

La imagen se construyó con:

``` bash
cd /opt/practica04/aplicacion
sudo docker build -t flask-app .
```

El contenedor se inició publicando el puerto 5000 en la propia
instancia:

``` bash
sudo docker run -d -p 5000:5000 --name flask-app flask-app
```

Para comprobar su estado y sus registros:

``` bash
sudo docker ps
sudo docker logs flask-app
```

Se configuró la política de reinicio para que el contenedor vuelva a
arrancar tras reinicios del servicio Docker:

``` bash
sudo docker update --restart unless-stopped flask-app
```

## 7. Gunicorn

Gunicorn sirve la aplicación WSGI Flask en `0.0.0.0:5000` dentro del
contenedor. Los registros muestran el arranque de Gunicorn, la dirección
de escucha y el inicio de un worker.

## 8. Nginx como proxy inverso

Nginx se instaló en Ubuntu y se configuró para recibir las peticiones
web. Las solicitudes HTTPS se reenvían a Gunicorn en `127.0.0.1:5000`.
La configuración utilizada se incluye en `configuracion/nginx.conf`.

Se validó con:

``` bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
```

## 9. HTTPS y certificado SSL/TLS

Se generó un certificado autofirmado con OpenSSL, válido durante 365
días, y se instaló en `/etc/nginx/ssl/`. Nginx utiliza `certificado.crt`
y `clave.key` para atender conexiones en el puerto 443.

Al ser autofirmado, el navegador muestra una advertencia de confianza.
Esto es esperado en esta práctica de laboratorio. No equivale a un
certificado público emitido por una autoridad certificadora.

El puerto 443 debe estar permitido en el grupo de seguridad de EC2.

## 10. Comprobaciones y evidencias

Se recopilan las capturas en `capturas/`. Evidencias recomendadas: -
Inicio de Learner Lab y panel EC2. - Configuración de instancia, clave y
User Data. - Instancia en ejecución y grupo de seguridad. - Conexión SSH
e instalación de Docker. - Archivos de aplicación y construcción de
imagen. - Contenedor y registros de Gunicorn. - Instalación y
configuración de Nginx. - Aplicación accesible mediante HTTPS. -
Registros de Nginx y Gunicorn.

## 11. Incidencias y soluciones

### Fallo de User Data

Cloud-init indicó un fallo en `scripts_user`. Se revisaron
`/var/log/cloud-init-output.log`, `/var/log/cloud-init.log` y el estado
de cloud-init. Docker se instaló manualmente con `apt` y se habilitó
mediante systemd.

### Error 502 Bad Gateway

Nginx devolvió un error 502 porque el contenedor `flask-app` estaba
detenido. Se inició de nuevo con `sudo docker start flask-app` y se
configuró `unless-stopped` como política de reinicio. Tras ello se
comprobó el acceso a la aplicación.

### Advertencia del navegador

Chrome mostró una advertencia porque el certificado es autofirmado. Es
el comportamiento esperado para un certificado de laboratorio no
reconocido por el navegador.

## 12. Conclusiones

La práctica permitió desplegar una aplicación Flask en una instancia
EC2, ejecutarla con Gunicorn dentro de Docker y publicar el servicio
mediante Nginx. También se configuró HTTPS con un certificado
autofirmado y se revisaron los registros de los servicios. Las
incidencias de automatización y del contenedor se diagnosticaron
mediante logs y se resolvieron para completar las pruebas.

## Seguridad y entrega

-   No subir `practica04.pem` a GitHub ni incluirla en la entrega.
-   No publicar ni compartir `clave.key`.
-   No incluir contraseñas, tokens ni otros secretos.
-   Para un servicio real, utilizar un dominio y un certificado emitido
    por una autoridad certificadora, además de restringir el acceso
    administrativo.
-   Antes de finalizar el Learner Lab, guardar todas las capturas y
    archivos de documentación.
