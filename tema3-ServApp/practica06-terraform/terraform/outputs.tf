output "ip_publica" {
  description = "Dirección IP pública de la instancia EC2"
  value       = aws_instance.servidor.public_ip
}

output "id_instancia" {
  description = "Identificador de la instancia EC2"
  value       = aws_instance.servidor.id
}