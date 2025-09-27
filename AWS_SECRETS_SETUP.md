# 🔐 Configuración de AWS Secrets Manager para ECS

## 📋 Resumen de Cambios

Se ha configurado tu aplicación Flask para leer las credenciales de base de datos desde **AWS Secrets Manager** en lugar de usar variables de entorno hardcodeadas.

## 🛠️ Archivos Creados/Modificados

### 1️⃣ `ecs-task-def.json`
- **Nuevo archivo** con la definición de tarea de ECS
- Configura el contenedor para leer secretos desde AWS Secrets Manager
- Los secretos `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` se leen automáticamente

### 2️⃣ `.github/workflows/aws.yml`
- **Modificado** para obtener el ARN completo del secreto
- Reemplaza los placeholders con valores reales durante el deployment
- Usa el archivo de task definition renderizado

## 🔑 Secretos Requeridos en AWS Secrets Manager

### Secreto: `flask-app-prod-secrets`
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

### 1️⃣ Rol de Ejecución de Tareas (`ecsTaskExecutionRole`)
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
        "arn:aws:secretsmanager:REGION:ACCOUNT-ID:secret:flask-app-prod-secrets-*"
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

### 2️⃣ Usuario/Rol de GitHub Actions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:DescribeSecret"
      ],
      "Resource": [
        "arn:aws:secretsmanager:REGION:ACCOUNT-ID:secret:flask-app-prod-secrets-*"
      ]
    }
  ]
}
```

## 🚀 Cómo Funciona

1. **GitHub Actions** obtiene el ARN completo del secreto
2. **Reemplaza placeholders** en `ecs-task-def.json` con valores reales
3. **ECS** lee los secretos automáticamente al iniciar el contenedor
4. **Flask** recibe las variables de entorno sin cambios en el código

## 🔧 Comandos Útiles

### Crear el secreto (si no existe):
```bash
aws secretsmanager create-secret \
  --name flask-app-prod-secrets \
  --description "Database credentials for Flask app" \
  --secret-string '{
    "DB_HOST": "tu-rds-endpoint.amazonaws.com",
    "DB_USER": "tu_usuario",
    "DB_PASSWORD": "tu_password",
    "DB_NAME": "AlumnosClases"
  }'
```

### Verificar el secreto:
```bash
aws secretsmanager get-secret-value \
  --secret-id flask-app-prod-secrets \
  --query SecretString --output text | jq .
```

### Obtener el ARN del secreto:
```bash
aws secretsmanager describe-secret \
  --secret-id flask-app-prod-secrets \
  --query ARN --output text
```

## 📝 Variables en GitHub Secrets

Asegúrate de tener estos secretos configurados en GitHub:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` (si usas credenciales temporales)
- `AWS_REGION`
- `ECR_REPOSITORY`
- `ECS_SERVICE`
- `ECS_CLUSTER`

## 🛡️ Beneficios de Seguridad

✅ **Secretos centralizados** en AWS Secrets Manager  
✅ **Rotación automática** de credenciales  
✅ **Auditoría** de acceso a secretos  
✅ **Encriptación** en tránsito y en reposo  
✅ **Permisos granulares** IAM  
✅ **Sin credenciales** en el código fuente  

## ⚠️ Notas Importantes

- El ARN del secreto incluye un sufijo aleatorio (ej: `-AbCdEf`)
- El workflow detecta automáticamente este ARN completo
- Las credenciales nunca aparecen en logs de GitHub Actions
- ECS inyecta las variables de entorno de forma segura