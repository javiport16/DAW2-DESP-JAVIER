
#!/bin/bash
set -euxo pipefail

exec > >(tee -a /var/log/user-data.log) 2>&1

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    docker.io docker-compose-v2 openssl

systemctl enable --now docker

mkdir -p /opt/proxy-inverso-ssl/app
mkdir -p /opt/proxy-inverso-ssl/nginx
mkdir -p /opt/proxy-inverso-ssl/certs

cd /opt/proxy-inverso-ssl

# Aplicación Flask
cat > app/app.py <<'PY'
from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route("/")
def inicio():
    return f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Práctica Proxy Inverso SSL</title>
    </head>
    <body style="font-family:Arial;margin:40px">
      <h1>Práctica de Proxy Inverso Nginx</h1>
      <p><b>Alumno:</b> Javier Portela Cárdenas</p>
      <p><b>Centro:</b> Pio Baroja</p>
      <p><b>Ciclo:</b> CFGS DAW Bil</p>
      <p><b>Grupo:</b> Segundo</p>
      <p><b>Fecha:</b> {date.today()}</p>
      <p>Flask funcionando detrás de Nginx con HTTPS.</p>
    </body>
    </html>
    """

PY

cat > app/requirements.txt <<'REQ'
Flask>=3.0,<4.0
gunicorn>=22.0,<24.0
REQ

cat > app/Dockerfile <<'DOCKER'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
DOCKER

# Configuración Nginx
cat > nginx/default.conf <<'NGINX'
server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate /etc/nginx/certs/server.crt;
    ssl_certificate_key /etc/nginx/certs/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://flask:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

# Certificado autofirmado para pruebas por IP
openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout certs/server.key \
    -out certs/server.crt \
    -subj "/CN=localhost"

chmod 600 certs/server.key

# Docker Compose
cat > docker-compose.yml <<'YAML'
services:
  flask:
    build: ./app
    restart: unless-stopped
    expose:
      - "5000"
    networks:
      - red_privada

  nginx:
    image: nginx:stable
    restart: unless-stopped
    depends_on:
      - flask
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ./certs:/etc/nginx/certs:ro
    networks:
      - red_privada

networks:
  red_privada:
    driver: bridge
YAML

docker compose up -d --build

echo "Despliegue completado"
