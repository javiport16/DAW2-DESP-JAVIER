terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "servidor" {
  ami                    = var.ami
  instance_type          = var.tipo_instancia
  key_name               = var.nombre_clave
  vpc_security_group_ids = [aws_security_group.practica06.id]

  tags = {
    Name = "practica06-terraform"
  }
}
resource "aws_security_group" "practica06" {
  name        = "practica06-security-group"
  description = "Acceso SSH HTTP y HTTPS para la practica 06"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "practica06-security-group"
  }
}