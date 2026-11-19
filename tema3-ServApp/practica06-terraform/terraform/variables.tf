variable "region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI de Ubuntu Server 24.04"
  type        = string
}

variable "tipo_instancia" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t2.micro"
}
variable "nombre_clave" {
  description = "Nombre del par de claves SSH existente en AWS"
  type        = string
  default     = "practica04"
}