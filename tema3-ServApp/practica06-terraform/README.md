# Práctica 06: Terraform + AWS EC2

## 1. Introducción

En esta práctica se ha automatizado la creación de una instancia EC2 en AWS utilizando Terraform, una herramienta de infraestructura como código (*Infrastructure as Code*, IaC).

El objetivo ha sido comprobar cómo Terraform permite crear, modificar y administrar recursos en la nube mediante archivos de configuración, sin tener que configurarlos manualmente desde la consola de AWS.

## 2. Tecnologías utilizadas

- **Terraform:** herramienta para gestionar infraestructura mediante código.
- **AWS:** plataforma de servicios en la nube.
- **Amazon EC2:** servicio de máquinas virtuales.
- **Ubuntu Server:** sistema operativo de la instancia.
- **SSH:** protocolo de conexión remota segura.
- **Security Groups:** reglas de seguridad para controlar el tráfico de red.

## 3. Estructura del proyecto

```text
practica06-terraform/
├── requisitos-practica06-terraform.md
├── README.md
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
├── capturas/
│   └── 18 capturas del proceso
└── docs/
    └── arquitectura-practica06.png
```

## 4. Configuración de Terraform

Se crearon cuatro archivos:

- `main.tf`: define el proveedor de AWS, la instancia EC2 y el Security Group.
- `variables.tf`: declara la región, la AMI, el tipo de instancia y el nombre de la clave SSH.
- `outputs.tf`: muestra la IP pública y el identificador de la instancia.
- `terraform.tfvars`: establece los valores de configuración de la infraestructura.

Se utilizó la región `us-east-1` y una instancia de tipo `t2.micro`.

## 5. Creación de la infraestructura

Primero se ejecutaron los comandos:

```bash
terraform init
terraform validate
terraform plan
terraform apply
```

Terraform creó una instancia EC2 automáticamente.

Después se verificó en la consola de AWS que la instancia estaba funcionando y se consultaron su IP pública y su identificador mediante `terraform output`.

## 6. Limitaciones iniciales

La primera versión de la infraestructura tenía dos limitaciones importantes:

- No disponía de una clave SSH asociada.
- Utilizaba el grupo de seguridad predeterminado, sin reglas que permitieran conexiones SSH, HTTP o HTTPS desde Internet.

Por ello, aunque Terraform había creado la instancia correctamente, no era posible administrarla por SSH desde el ordenador local.

## 7. Mejoras de la infraestructura

Se modificó `main.tf` para añadir un Security Group con las siguientes reglas:

| Servicio | Puerto | Función |
|---|---|---|
| SSH | 22 | Administración remota |
| HTTP | 80 | Acceso web |
| HTTPS | 443 | Acceso web seguro |

También se incorporó la clave SSH existente `practica04` mediante la variable `nombre_clave`.

Tras ejecutar `terraform validate`, `terraform plan` y `terraform apply`, Terraform reemplazó la instancia inicial y creó una nueva con la configuración actualizada.

Finalmente, se comprobó que era posible conectarse al servidor mediante SSH.

## 8. Análisis final

### ¿Qué significa Infrastructure as Code (IaC)?

Es una metodología que permite definir y administrar infraestructura informática mediante archivos de código, en lugar de configurar los recursos manualmente.

### ¿Qué ventajas aporta Terraform?

Terraform permite automatizar procesos, reutilizar configuraciones, reducir errores humanos y reproducir la misma infraestructura en diferentes entornos.

### ¿Qué función tienen los Security Groups?

Actúan como cortafuegos virtuales que controlan el tráfico permitido hacia y desde los recursos de AWS.

### ¿Por qué son necesarias las Key Pairs?

Permiten autenticar de forma segura las conexiones SSH a una instancia EC2 mediante una clave privada y una clave pública.

### ¿Para qué sirve `terraform init`?

Inicializa el proyecto Terraform y descarga los proveedores necesarios.

### ¿Para qué sirve `terraform plan`?

Muestra los cambios que Terraform propone realizar en la infraestructura, sin aplicarlos todavía.

### ¿Para qué sirve `terraform apply`?

Ejecuta los cambios definidos en los archivos de Terraform, creando, modificando o eliminando los recursos necesarios.

### ¿Para qué sirve `terraform destroy`?

Elimina los recursos administrados por la configuración de Terraform. Es útil para desmontar infraestructuras que ya no se necesitan y evitar costes innecesarios.

No se ha ejecutado durante esta práctica porque se necesitaba conservar temporalmente la instancia para verificar la conexión SSH.

### ¿Qué ventajas presenta Terraform para equipos DevOps?

Permite compartir configuraciones, integrar la infraestructura en sistemas de control de versiones, automatizar despliegues y mantener entornos consistentes.

### ¿Qué ventajas tiene la automatización frente a la creación manual de recursos?

La automatización permite ahorrar tiempo, repetir despliegues, reducir errores de configuración y facilitar el mantenimiento de la infraestructura.

## 9. Problemas encontrados y soluciones

Durante la práctica surgieron varios problemas:

1. **Terraform no estaba instalado:** se descargó manualmente desde HashiCorp y se configuró para utilizarlo desde PowerShell.
2. **Las credenciales de AWS Academy eran temporales:** se configuraron mediante variables de entorno.
3. **La instancia inicial no admitía conexión SSH:** se añadió una Key Pair y un Security Group mediante Terraform.
4. **Terraform no detectaba los cambios esperados:** se comprobó el contenido de `main.tf`, se guardaron las modificaciones y se ejecutó de nuevo `terraform plan`.

## 10. Conclusiones

Esta práctica ha permitido comprender cómo funciona la infraestructura como código y cómo Terraform automatiza la creación y administración de recursos en AWS.

Se ha comprobado que es posible definir una instancia EC2 mediante archivos de configuración, modificar sus opciones de seguridad y conectarse por SSH después de aplicar los cambios.

Terraform facilita la reproducción de infraestructuras y reduce la necesidad de realizar configuraciones manuales desde la consola de AWS.

En un entorno real sería recomendable limitar el acceso SSH a direcciones IP autorizadas y gestionar las credenciales de forma segura.