# Infraestructura AWS ECS Fargate con CloudFormation

Este directorio contiene la plantilla de CloudFormation `CreaEntornoECS_FargateBasico.yaml` diseñada para desplegar una infraestructura completa y segura en AWS para ejecutar aplicaciones contenedorizadas utilizando Amazon ECS con Fargate.

## 🏗️ Arquitectura Desplegada

La plantilla crea los siguientes recursos y configuraciones:

### 🌐 Red (Networking)
*   **VPC (Virtual Private Cloud):** Red aislada para el proyecto (`10.113.0.0/16` por defecto).
*   **Subredes Públicas (2):** Alojadas en diferentes zonas de disponibilidad. Utilizadas por el Balanceador de Carga (ALB) y el NAT Gateway.
*   **Subredes Privadas (2):** Alojadas en diferentes zonas de disponibilidad. Aquí se ejecutan de forma segura los contenedores (ECS Tasks) y la base de datos (RDS), sin acceso directo desde internet.
*   **Internet Gateway (IGW):** Proporciona salida a internet para las subredes públicas.
*   **NAT Gateway:** Permite que los recursos en las redes privadas tengan salida a internet (para descargar imágenes Docker, actualizaciones, etc.) sin exponerse a conexiones entrantes.

### 💻 Computación (Compute & Containers)
*   **Amazon ECS Cluster:** Orquestador de contenedores configurado para usar **AWS Fargate** (Serverless).
*   **Capacity Providers:** Configurado para usar `FARGATE` y `FARGATE_SPOT` (para optimización de costes).
*   **ECR Repository:** Registro privado para almacenar las imágenes Docker de la aplicación.
*   **Task Definition:** Define cómo se ejecuta la aplicación (CPU, Memoria, Imagen, Puertos, Logs).
*   **ECS Service:** Mantiene la aplicación en ejecución con la cantidad deseada de réplicas, gestiona el despliegue y auto-recuperación.
*   **Auto Scaling:** Configurado para escalar el número de tareas basándose en el uso de CPU (Target Tracking al 70%).

### 🗄️ Base de Datos (Database)
*   **Amazon RDS MySQL:** Instancia de base de datos gestionada (MySQL 8.x, clase `db.t3.micro`).
*   **Seguridad:** Desplegada en subredes privadas, sin acceso público. Solo acepta conexiones desde los contenedores ECS.
*   **AWS Secrets Manager:** Almacena de forma segura las credenciales y endpoint de la base de datos, evitando tener contraseñas en texto plano en el código.

### ⚖️ Balanceo de Carga y Seguridad
*   **Application Load Balancer (ALB):** Punto de entrada único desde internet (Puerto 80). Distribuye el tráfico entre los contenedores.
*   **Security Groups (Firewall):**
    *   **ALB SG:** Permite tráfico HTTP (80) desde cualquier lugar.
    *   **ECS SG:** Solo permite tráfico entrante desde el ALB.
    *   **RDS SG:** Solo permite tráfico entrante desde los contenedores ECS (Puerto 3306).

## 🚀 Cómo usar este template

Puedes desplegar esta infraestructura directamente desde la consola de AWS CloudFormation o utilizando AWS CLI.

### Parámetros Principales
| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `DBUser` | Usuario maestro para la base de datos RDS | `dbadmin` |
| `DBPassword` | Contraseña para la base de datos RDS | *(Requerido)* |
| `DBNombre` | Nombre de la base de datos inicial | `AlumnosClases` |
| `ContainerImage`| Imagen Docker inicial para el servicio | `nginx:latest` |
| `DesiredCount` | Número de tareas (contendores) deseados | `2` |

### Outputs (Salidas)
Al finalizar el despliegue, la pila (stack) devolverá:
*   `LoadBalancerURL`: La URL pública para acceder a tu aplicación.
*   `ECSClusterName`: Nombre del cluster creado.
*   `BaseDatosDNS`: Endpoint de conexión a la base de datos.

## 🔐 Notas de Seguridad
*   La base de datos **no es accesible desde internet**.
*   Los contenedores **no tienen IP pública**, lo que reduce drásticamente la superficie de ataque.
*   Las credenciales de base de datos se gestionan automáticamente a través de Secrets Manager.
