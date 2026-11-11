#!/bin/bash
apt update -y
apt install -y docker.io git curl
systemctl enable docker
systemctl start docker
mkdir -p /opt/practica04
