# ⚙️ Gestión de Configuración - Neural SaaS Platform

## 🎯 Principio Fundamental

> **El archivo `.env` es la ÚNICA fuente de verdad para toda la configuración.**

### ✅ Buenas Prácticas

1. **Nunca hardcodear valores** en el código o docker-compose.yml
2. **Siempre usar variables de entorno** desde `.env`
3. **Nunca commitear `.env`** con valores reales
4. **Siempre commitear `.env.example`** como plantilla

---

## 📁 Archivos de Configuración

```
project_saas/
├── .env              # ✅ Configuración real (NO commitear)
├── .env.example      # ✅ Plantilla (SÍ commitear)
└── .gitignore        # ✅ Ignora .env
```

### `.env` - Configuración Real

- Contiene valores reales (passwords, API keys, etc.)
- **NO se commitea a Git**
- Cada desarrollador tiene su propio `.env`
- En producción, se configura en el servidor

### `.env.example` - Plantilla

- Contiene la estructura sin valores sensibles
- **SÍ se commitea a Git**
- Sirve como documentación
- Los nuevos desarrolladores lo copian a `.env`

---

## 🚀 Setup Inicial

### Para Nuevos Desarrolladores

```bash
# 1. Copiar plantilla
cp .env.example .env

# 2. Editar con tus valores
nano .env

# 3. Cambiar valores sensibles:
#    - GEMINI_API_KEY
#    - POSTGRES_PASSWORD
#    - JWT_SECRET_KEY
```

### Verificar Configuración

```bash
# Verificar que .env existe
test -f .env && echo "✅ .env existe" || echo "❌ .env no existe"

# Verificar que tiene las variables necesarias
grep -q "GEMINI_API_KEY" .env && echo "✅ GEMINI_API_KEY configurada" || echo "❌ Falta GEMINI_API_KEY"
```

---

## 📋 Variables de Entorno

### Categorías

#### 1. Configuración General
```bash
ENVIRONMENT=development
PROJECT_NAME=Neural SaaS Platform
PROJECT_VERSION=0.1.0
```

#### 2. Puertos
```bash
# Puertos HOST (los que usas en localhost)
POSTGRES_PORT_HOST=5433
REDIS_PORT_HOST=6380
BACKEND_PORT_HOST=8001
FRONTEND_PORT_HOST=8502

# Puertos internos (no cambiar)
FASTAPI_PORT=8000
STREAMLIT_PORT=8501
```

#### 3. Base de Datos
```bash
POSTGRES_USER=neural_user
POSTGRES_PASSWORD=tu_password_seguro
POSTGRES_DB=neural_saas_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://...
```

#### 4. Seguridad
```bash
JWT_SECRET_KEY=tu_secret_key_muy_seguro
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

#### 5. APIs Externas
```bash
GEMINI_API_KEY=tu_api_key_de_gemini
GEMINI_MODEL=gemini-1.5-flash
```

#### 6. Redis y Celery
```bash
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

#### 7. CORS y Rate Limiting
```bash
ALLOWED_ORIGINS=http://localhost:8502,http://localhost:8501
RATE_LIMIT_PER_MINUTE=60
```

#### 8. Logging
```bash
LOG_LEVEL=INFO
```

---

## 🔒 Seguridad

### Valores que NUNCA deben hardcodearse

❌ **NUNCA hacer esto:**

```python
# ❌ INCORRECTO
password = "mi_password_123"
api_key = "sk-1234567890"
secret_key = "super_secret"
```

```yaml
# ❌ INCORRECTO en docker-compose.yml
environment:
  POSTGRES_PASSWORD: "hardcoded_password"
  JWT_SECRET_KEY: "hardcoded_secret"
```

✅ **SIEMPRE hacer esto:**

```python
# ✅ CORRECTO
import os
password = os.getenv("POSTGRES_PASSWORD")
api_key = os.getenv("GEMINI_API_KEY")
secret_key = os.getenv("JWT_SECRET_KEY")
```

```yaml
# ✅ CORRECTO en docker-compose.yml
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  JWT_SECRET_KEY: ${JWT_SECRET_KEY}
```

### Generar Valores Seguros

```bash
# Generar JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generar POSTGRES_PASSWORD
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

---

## 🐳 Docker y Variables de Entorno

### docker-compose.yml

```yaml
services:
  db:
    environment:
      # ✅ CORRECTO - Lee desde .env
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      # ✅ CORRECTO - Puerto configurable
      - "${POSTGRES_PORT_HOST}:5432"

  app:
    # ✅ CORRECTO - Carga todo el .env
    env_file:
      - .env
    ports:
      # ✅ CORRECTO - Puertos configurables
      - "${BACKEND_PORT_HOST}:${FASTAPI_PORT}"
      - "${FRONTEND_PORT_HOST}:${STREAMLIT_PORT}"
```

### Dockerfile

```dockerfile
# ❌ INCORRECTO - No hardcodear
ENV POSTGRES_PASSWORD=hardcoded_password

# ✅ CORRECTO - Las variables vienen del .env vía docker-compose
# No es necesario definirlas en el Dockerfile
```

---

## 🔄 Diferentes Entornos

### Desarrollo Local

```bash
# .env (desarrollo)
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql+asyncpg://localhost:5433/neural_saas_db
```

### Producción

```bash
# .env (producción)
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql+asyncpg://prod-db:5432/neural_saas_db
```

### Testing

```bash
# .env.test
ENVIRONMENT=test
DATABASE_URL=postgresql+asyncpg://localhost:5433/neural_saas_test
```

---

## 📝 Checklist de Configuración

### Antes de Commitear

- [ ] `.env` está en `.gitignore`
- [ ] No hay valores hardcodeados en el código
- [ ] `.env.example` está actualizado
- [ ] Todos los valores sensibles usan variables de entorno
- [ ] docker-compose.yml usa `${VARIABLE}` sin defaults hardcodeados

### Antes de Deploy

- [ ] `.env` configurado en el servidor
- [ ] Valores de producción son diferentes a desarrollo
- [ ] Passwords son seguros (generados aleatoriamente)
- [ ] API keys son válidas
- [ ] Puertos no están en conflicto

---

## 🛠️ Comandos Útiles

### Verificar Variables

```bash
# Ver todas las variables del .env
cat .env | grep -v "^#" | grep -v "^$"

# Verificar una variable específica
grep "GEMINI_API_KEY" .env

# Verificar que no hay valores por defecto
grep -r "password.*=" backend/ | grep -v ".env"
```

### Validar .env

```bash
# Crear script de validación
./scripts/validate-env.sh
```

---

## 🚨 Problemas Comunes

### Error: Variable no definida

```bash
# Error
ERROR: The POSTGRES_PASSWORD variable is not set

# Solución
echo "POSTGRES_PASSWORD=tu_password" >> .env
```

### Error: Puerto en uso

```bash
# Verificar puertos
./check-ports.sh

# Cambiar puerto en .env
nano .env
# Cambiar BACKEND_PORT_HOST=8002
```

### Error: .env no se carga

```bash
# Verificar que existe
ls -la .env

# Verificar permisos
chmod 600 .env

# Verificar que docker-compose lo referencia
grep "env_file" docker-compose.yml
```

---

## 📚 Referencias

- [12 Factor App - Config](https://12factor.net/config)
- [Docker Compose - Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)

---

## ✅ Resumen

### DO ✅

- Usar `.env` para TODA la configuración
- Commitear `.env.example`
- Generar valores seguros para producción
- Verificar puertos antes de levantar servicios
- Documentar cada variable en `.env.example`

### DON'T ❌

- Hardcodear valores en código o docker-compose
- Commitear `.env` con valores reales
- Usar valores por defecto en producción
- Compartir API keys o passwords
- Ignorar conflictos de puertos

---

**Última actualización:** Enero 2025
