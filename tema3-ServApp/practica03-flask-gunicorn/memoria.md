# Memoria técnica: Práctica 03

## Despliegue de Flask con Gunicorn, Nginx y systemd

**Alumno:** Javier Portela  
**Asignatura:** Despliegue de Aplicaciones Web

## 1. Objetivo de la práctica

El objetivo ha sido aprender a desplegar una aplicación web desarrollada en Python utilizando Flask, Gunicorn y Nginx.

También se ha estudiado el funcionamiento de los servicios systemd y la importancia de los registros para diagnosticar errores.

## 2. Función de los componentes

### Flask

Flask es un framework web de Python que permite desarrollar aplicaciones, definir rutas y generar respuestas HTTP.

En esta práctica se utiliza para mostrar una página de bienvenida y la información del alumno.

### Gunicorn

Gunicorn es un servidor de aplicaciones WSGI que ejecuta el código Flask y atiende las peticiones que recibe.

Su principal ventaja es que permite gestionar procesos de trabajo y utilizar Flask en un entorno más adecuado para producción que su servidor de desarrollo.

### Nginx

Nginx es un servidor web que puede actuar como proxy inverso.

En esta práctica recibe las peticiones del navegador y las reenvía a Gunicorn.

### Docker

Docker permite ejecutar los componentes dentro de contenedores independientes.

Se ha utilizado para levantar Gunicorn y Nginx, conectándolos mediante una red común.

### systemd

systemd es el sistema de gestión de servicios utilizado por numerosas distribuciones Linux.

Permite iniciar, detener, reiniciar y supervisar servicios, además de configurar su inicio automático.

## 3. Flujo de peticiones

La arquitectura principal utilizada es:

```text
Navegador
   |
   v
Nginx
   |
   v
Gunicorn
   |
   v
Flask
```

Flask genera el contenido, Gunicorn ejecuta la aplicación y Nginx gestiona la entrada de las peticiones HTTP.

## 4. Comprobación del funcionamiento

Primero se ha comprobado que Gunicorn ejecutaba correctamente la aplicación Flask mediante el puerto `8003`.

Después se ha configurado Nginx para que pudiera reenviar las peticiones a Gunicorn.

El acceso a través del puerto `8083` ha permitido comprobar el funcionamiento del flujo completo.

De forma adicional, se ha configurado un servicio systemd en Ubuntu sobre WSL 2, ejecutando Gunicorn en el puerto `8013`.

## 5. Gestión con systemd

El servicio creado utiliza una unidad de plantilla llamada:

`practica03-gunicorn@.service`

Se ha configurado para ejecutar Gunicorn desde un entorno virtual de Python.

También se ha establecido el reinicio automático en caso de fallo mediante `Restart=always`.

Se ha comprobado su funcionamiento mediante `systemctl status`.

## 6. Registros de los servicios

Los registros son fundamentales para el diagnóstico de errores.

Se han consultado los logs de Gunicorn mediante `journalctl` y los de Nginx mediante `docker logs`.

En ellos se puede observar información sobre la ejecución de los servicios, las peticiones procesadas y los errores producidos.

## 7. Comparación con Tomcat

| Característica | Tomcat | Gunicorn |
|---|---|---|
| Lenguaje principal | Java | Python |
| Tipo de servidor | Contenedor de servlets | Servidor WSGI |
| Aplicaciones habituales | Servlets, JSP y aplicaciones Java | Flask y aplicaciones Python WSGI |
| Integración con Nginx | Sí | Sí |
| Gestión de procesos | Mediante Tomcat | Mediante trabajadores de Gunicorn |

Ambos permiten ejecutar aplicaciones web y pueden situarse detrás de Nginx.

La principal diferencia es el tipo de aplicaciones que ejecutan y las tecnologías utilizadas.

Tomcat se utiliza principalmente en el ecosistema Java, mientras que Gunicorn está orientado a aplicaciones Python compatibles con WSGI.

## 8. Respuestas a las cuestiones finales

**1. ¿Cuál es la función de Flask?**

Permitir desarrollar aplicaciones web Python, gestionando rutas y respuestas HTTP.

**2. ¿Cuál es la función de Gunicorn?**

Ejecutar aplicaciones web Python mediante WSGI y atender las peticiones recibidas.

**3. ¿Por qué no se utiliza Flask directamente en producción?**

Porque el servidor de desarrollo de Flask no está diseñado para gestionar aplicaciones públicas de producción. Es preferible utilizar un servidor WSGI como Gunicorn.

**4. ¿Qué ventajas proporciona Gunicorn?**

Permite utilizar múltiples trabajadores, gestionar procesos y ejecutar aplicaciones Python de forma más adecuada para producción.

**5. ¿Qué función realiza Nginx?**

Recibir peticiones HTTP y actuar como servidor web o proxy inverso.

**6. ¿Qué es un Reverse Proxy?**

Es un servidor intermediario que recibe solicitudes de los clientes y las reenvía a uno o varios servidores internos.

**7. ¿Qué ventajas aporta systemd?**

Permite iniciar automáticamente servicios, reiniciarlos cuando fallan, consultar su estado y acceder a sus registros.

**8. ¿Qué diferencias existen entre Tomcat y Gunicorn?**

Tomcat ejecuta aplicaciones Java basadas en servlets, mientras que Gunicorn ejecuta aplicaciones Python compatibles con WSGI.

**9. ¿Qué similitudes existen entre Nginx + Tomcat y Nginx + Gunicorn?**

Ambas arquitecturas utilizan Nginx como servidor frontal y otro componente para ejecutar la aplicación.

**10. ¿Qué mejoras podrían realizarse sobre la arquitectura implementada?**

Se podría incorporar HTTPS, configurar un dominio, añadir monitorización, utilizar un sistema de despliegue automático y mejorar la gestión de registros y errores.

## 9. Problemas encontrados

Durante la práctica surgieron varios problemas:

- Un conflicto de puertos al iniciar Gunicorn mediante systemd.
- Una diferencia entre el nombre del servicio creado y el utilizado para activarlo.
- La falta de integración de Docker Desktop en Ubuntu WSL.

Estos problemas se solucionaron modificando el puerto del servicio, corrigiendo el nombre de la unidad systemd y consultando Docker desde PowerShell.

## 10. Conclusión

Esta práctica ha permitido comprender mejor la arquitectura de despliegue de aplicaciones web.

Se ha aprendido a utilizar Flask como framework, Gunicorn como servidor de aplicaciones, Nginx como proxy inverso y systemd para la gestión de servicios.

También se ha comprobado la importancia de los logs y de la separación de responsabilidades entre los componentes.

El resultado es una aplicación Flask accesible a través de Gunicorn y Nginx en un entorno local, junto con una configuración adicional de Gunicorn administrada mediante systemd.
