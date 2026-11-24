# Práctica 03: Despliegue de una aplicación Flask con Gunicorn y Nginx

**Módulo:** Despliegue de Aplicaciones Web (DAW)  
**Alumno:** Javier Portela  
**Tecnologías:** Python, Flask, Gunicorn, Nginx, Docker, Ubuntu, systemd y WSL 2.

## 1. Introducción

El objetivo de esta práctica es desplegar una aplicación web desarrollada con Flask utilizando Gunicorn como servidor de aplicaciones y Nginx como proxy inverso.

Esta arquitectura permite separar la aplicación Python del servidor que recibe las peticiones HTTP, reproduciendo una configuración habitual en entornos de producción.

También se ha configurado un servicio systemd en Ubuntu para gestionar Gunicorn automáticamente.

## 2. Estructura del proyecto

```text
practica03-flask-gunicorn/
├── aplicacion/
│   └── app.py
├── configuracion/
│   ├── Dockerfile
│   └── nginx.conf
├── capturas/
├── requisitos.md
├── README.md
└── memoria.md
```

- **aplicacion/app.py:** código de la aplicación Flask.
- **configuracion/Dockerfile:** construcción de la imagen con Python y Gunicorn.
- **configuracion/nginx.conf:** configuración del proxy inverso.
- **capturas/:** evidencias de funcionamiento.
- **memoria.md:** análisis técnico y conclusiones.

## 3. Arquitectura utilizada

El flujo de comunicación es:

```text
Usuario / Navegador
        |
        | HTTP :8083
        v
      Nginx
  (Reverse Proxy)
        |
        | HTTP :8000
        v
     Gunicorn
        |
        v
      Flask
   (Aplicación)
```

El navegador realiza la petición a Nginx. Nginx la reenvía a Gunicorn, que ejecuta la aplicación Flask y devuelve su respuesta.

## 4. Aplicación Flask

Se ha desarrollado una aplicación web sencilla que muestra una página de bienvenida, identifica al alumno y proporciona información sobre la práctica.

Flask se encarga de gestionar las rutas HTTP y generar las respuestas.

## 5. Configuración de Gunicorn

Gunicorn permite ejecutar aplicaciones Python compatibles con WSGI.

Se ha construido una imagen Docker que incluye la aplicación Flask y sus dependencias.

Para construir la imagen desde la raíz del proyecto:

```powershell
docker build -t practica03-flask -f .\configuracion\Dockerfile .
```

Para iniciar el contenedor:

```powershell
docker run -d --name practica03-gunicorn -p 8003:8000 practica03-flask
```

La aplicación queda accesible directamente desde:

http://localhost:8003

Este acceso permite comprobar el funcionamiento de Gunicorn sin pasar por Nginx.

## 6. Configuración de Nginx

Nginx se ha configurado como proxy inverso mediante el archivo `configuracion/nginx.conf`.

Su función es recibir las peticiones HTTP y reenviarlas al servicio Gunicorn.

Se ha creado una red Docker para comunicar ambos contenedores:

```powershell
docker network create practica03-net
docker network connect --alias flask-app practica03-net practica03-gunicorn
```

Se ha ejecutado Nginx utilizando la configuración del proyecto:

```powershell
docker run -d --name practica03-nginx --network practica03-net -p 8083:80 -v "${PWD}\configuracion\nginx.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine
```

El proxy utiliza el nombre `flask-app` para localizar el servicio Gunicorn dentro de la red Docker.

La aplicación se puede abrir a través de Nginx en:

http://localhost:8083

## 7. Servicio systemd

Para comprobar el funcionamiento de systemd, se ha instalado Ubuntu 24.04 en WSL 2.

Se ha creado un entorno virtual de Python y se han instalado Flask y Gunicorn.

Posteriormente, se ha configurado un servicio denominado:

`practica03-gunicorn@.service`

El servicio permite iniciar Gunicorn mediante systemd y reiniciarlo automáticamente en caso de fallo.

El servicio ejecuta Gunicorn en el puerto local `8013`, separado de los puertos utilizados por Docker.

Para comprobar su estado:

```bash
systemctl status "practica03-gunicorn@$(whoami).service" --no-pager
```

Se ha verificado que el servicio aparece como `active (running)`.

## 8. Análisis de registros

Se han consultado los registros de Gunicorn mediante systemd:

```bash
sudo journalctl -u "practica03-gunicorn@$(whoami).service" -n 20 --no-pager
```

También se han inspeccionado los registros del contenedor Nginx:

```powershell
docker logs --tail 30 practica03-nginx
```

Estos registros permiten estudiar los arranques de los servicios, las peticiones HTTP y los posibles errores.

## 9. Pruebas realizadas

- Construcción de la imagen Docker.
- Ejecución de Gunicorn.
- Acceso directo a Flask mediante `localhost:8003`.
- Configuración de Nginx como proxy inverso.
- Comunicación entre los contenedores mediante una red Docker.
- Acceso a la aplicación mediante `localhost:8083`.
- Configuración y ejecución del servicio Gunicorn con systemd.
- Consulta de registros de Gunicorn y Nginx.

## 10. Problemas encontrados y soluciones

**Conflicto de puertos:** durante la configuración del servicio systemd, el puerto `8003` estaba ocupado. Se solucionó utilizando el puerto `8013`.

**Configuración del servicio systemd:** inicialmente hubo un problema con el nombre del archivo del servicio. Se corrigió utilizando la plantilla `practica03-gunicorn@.service`.

**Acceso a Docker desde Ubuntu:** la distribución WSL no tenía habilitada la integración con Docker Desktop. Para consultar los contenedores se utilizó PowerShell de Windows.

## 11. Evidencias

Las capturas se encuentran en la carpeta `capturas/`:

1. `01-flask-funcionando.png`
2. `02-gunicorn-ejecutandose.png`
3. `03-configuracion-nginx.png`
4. `04-flujo-completo.png`
5. `05-servicio-systemd.png`
6. `06-logs-gunicorn.png`
7. `07-logs-nginx.png`

## 12. Conclusión

Esta práctica ha permitido comprender cómo desplegar una aplicación Flask utilizando Gunicorn y Nginx.

Se ha comprobado el funcionamiento del proxy inverso, la comunicación entre servicios, la gestión de Gunicorn mediante systemd y el análisis de registros.

La práctica demuestra la importancia de separar los componentes de una aplicación web para facilitar su gestión, mantenimiento y despliegue.
