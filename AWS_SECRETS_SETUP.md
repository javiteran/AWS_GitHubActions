# 🔐 Configuración de AWS Secrets Manager para ECS

## 📋 Resumen de Cambios

La aplicación Flask está configurada para leer las credenciales de base de datos desde **AWS Secrets Manager** usando la definición de tarea de ECS y el workflow de GitHub Actions. No se usan variables de entorno hardcodeadas.

## 🛠️ Archivos Clave

### 1️⃣ `ecs-task-def.json`

- Define la tarea ECS y el contenedor.
- Configura el contenedor para leer secretos desde AWS Secrets Manager usando la sección `secrets`.
- Los secretos `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` se leen automáticamente.

### 2️⃣ `.github/workflows/aws.yml`

- Obtiene el ARN completo del secreto desde AWS Secrets Manager.
- Reemplaza los placeholders en `ecs-task-def.json` con valores reales durante el deployment.
- Usa variables de GitHub Actions (`vars.AWS_PROYECTO`) para nombrar recursos de AWS de forma dinámica.

## 🔑 Secretos Requeridos en AWS Secrets Manager

### Secreto: `secretos-despliegue-aws`

Debe contener las siguientes claves:

```json
{
  "DB_HOST": "tu-rds-endpoint.amazonaws.com",
  "DB_USER": "tu_usuario_mysql",
  "DB_PASSWORD": "tu_password_seguro",
  "DB_NAME": "AlumnosClases"
}
```

## ⚙️ Permisos IAM Requeridos

### 1️⃣ Rol de Ejecución de Tareas (`LabRole`)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:REGION:ACCOUNT-ID:secret:secretos-despliegue-aws-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🚀 Flujo de Trabajo

1. **GitHub Actions** obtiene el ARN completo del secreto usando AWS CLI.
2. **Reemplaza placeholders** en `ecs-task-def.json` con valores reales (ARN, nombres, etc.).
3. **ECS** lee los secretos automáticamente al iniciar el contenedor.
4. **Flask** recibe las variables de entorno desde los secretos, sin cambios en el código.

## 🔧 Comandos Útiles

### Crear el secreto (si no existe)

Los secretos se están creando con la plantilla de CloudFormation, pero si necesitas crear uno manualmente, puedes usar este comando:

```bash
aws secretsmanager create-secret \
  --name secretos-despliegue-aws \
  --description "Database credentials for Flask app" \
  --secret-string '{
    "DB_HOST": "tu-rds-endpoint.amazonaws.com",
    "DB_USER": "tu_usuario",
    "DB_PASSWORD": "tu_password",
    "DB_NAME": "AlumnosClases"
  }'
```

### Verificar el secreto

```bash
aws secretsmanager get-secret-value \
  --secret-id secretos-despliegue-aws \
  --query SecretString --output text | jq .
```

### Obtener el ARN del secreto

```bash
aws secretsmanager describe-secret \
  --secret-id secretos-despliegue-aws \
  --query ARN --output text

```bash
aws secretsmanager describe-secret \
  --secret-id secretos-despliegue-aws \
  --query ARN --output text
```

## 📝 Variables y Secrets en GitHub Actions

Asegúrate de tener estas variables y secretos configurados en GitHub:

| Nombre                | Tipo    | Descripción                                      |
|-----------------------|---------|--------------------------------------------------|
| AWS_ACCESS_KEY_ID     | Secret  | Access key de AWS para autenticación              |
| AWS_SECRET_ACCESS_KEY | Secret  | Secret key de AWS para autenticación              |
| AWS_SESSION_TOKEN     | Secret  | Token temporal de sesión (si aplica)              |
| AWS_REGION            | Secret/Var | Región AWS donde se despliega la infraestructura |
| AWS_PROYECTO          | Var     | Nombre base para recursos (ECR, ECS, TASK, etc.)        |

## 🛡️ Beneficios de Seguridad

✅ **Secretos centralizados** en AWS Secrets Manager  
✅ **Rotación automática** de credenciales  
✅ **Auditoría** de acceso a secretos  
✅ **Encriptación** en tránsito y en reposo  
✅ **Permisos granulares** IAM  
✅ **Sin credenciales** en el código fuente  

## ⚠️ Notas Importantes

- El ARN del secreto incluye un sufijo aleatorio (ej: `-AbCdEf`).
- El workflow detecta automáticamente este ARN completo.
- Las credenciales nunca aparecen en logs de GitHub Actions.
- ECS inyecta las variables de entorno de forma segura.
