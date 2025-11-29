

# 🧠 Neural Code Analyzer

**Plataforma SaaS de análisis de código Python con IA**  
*Gemini 2.5 Flash · FastAPI · Streamlit · PostgreSQL*

---

## 🚀 Comenzar en 60 Segundos

```bash
# 1. Clonar y configurar
git clone https://github.com/Ponce1969/sas_con_agentes.git
cd project_saas
cp .env.example .env

# 2. Configurar API Key (obtener en: https://aistudio.google.com/)
echo "GEMINI_API_KEY=tu_api_key_aqui" >> .env

# 3. Ejecutar
docker compose up -d

# 4. ¡Listo!
# 🌐 App: http://localhost:8502
# 📚 API Docs: http://localhost:8001/docs

✨ ¿Qué Puede Hacer?
🔍 Análisis Inteligente

    🐛 Bugs potenciales - Detecta errores antes de producción

    👃 Code smells - Identifica malas prácticas

    ⚡ Optimizaciones - Sugiere mejoras de rendimiento

    📊 Score 0-100 - Calificación automática de calidad

📈 Dashboard Interactivo

    📊 Métricas en tiempo real - Tus estadísticas de uso

    🏆 Sistema de logros - Gamificación para desarrolladores

    💡 Insights automáticos - Tips personalizados para mejorar

    📥 Exportar datos - CSV/JSON para análisis externo

🔒 Seguridad Empresarial

    🔐 Autenticación JWT - Login seguro con Argon2

    🔒 Encriptación AES-128 - API keys protegidas

    📏 Límites configurables - 800 líneas por análisis

    🛡️ Rate limiting - Protección contra abuso

🏗️ Arquitectura


project_saas/
├── backend/app/          # FastAPI + PostgreSQL
│   ├── core/            # Configuración y seguridad
│   ├── domain/          # Modelos de datos
│   ├── application/     # Lógica de negocio
│   └── web/routers/     # Endpoints API
├── frontend/app/        # Streamlit Dashboard
│   ├── main.py          # Aplicación principal
│   └── pages/           # Vistas (login, dashboard)
├── deploy/              # Scripts de deployment
└── docker-compose.yml   # Orquestación containers

Stack Tecnológico: Python 3.12, FastAPI, Streamlit, Gemini 2.5 Flash, PostgreSQL, Redis, Docker
⚙️ Configuración Rápida
Variables Esenciales (.env)
bash

# Obtener en: https://aistudio.google.com/
GEMINI_API_KEY=tu_clave_gemini_aqui

# Generar con:
# python -c "import secrets; print(secrets.token_urlsafe(64))"
JWT_SECRET_KEY=clave_jwt_super_secreta

# Generar con:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
ENCRYPTION_KEY=clave_encriptacion_32_chars

# Base de datos (automático con Docker)
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/neuraldb

Comandos Diarios
bash

# Iniciar toda la aplicación
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f frontend

# Detener servicios
docker compose down

# Backup de base de datos
docker compose exec db pg_dump -U postgres neuraldb > backup.sql

📊 Planes y Límites
Característica	Free 🆓	Pro 💎	Enterprise 🏢
Análisis por día	5	50	Ilimitado
Líneas por análisis	800	800	2000
Historial	30 días	1 año	Ilimitado
Soporte	Comunidad	Email prioritario	24/7 dedicado
Precio	Gratis	$9.99/mes	Personalizado
🔌 Uso de la API
Análisis de Código
python

import requests

url = "http://localhost:8001/api/analysis"
headers = {"Authorization": "Bearer tu_jwt_token"}
data = {"code": "def ejemplo(): pass"}

response = requests.post(url, json=data, headers=headers)
print(response.json())

Endpoints Principales

    POST /api/analysis - Analizar código Python

    GET /api/analysis/history - Obtener historial

    POST /api/auth/login - Iniciar sesión

    GET /api/auth/me - Perfil de usuario

📚 Ver documentación completa de la API
🚀 Deployment
Opción 1: Docker (Recomendado para Desarrollo)
bash

# Desarrollo local
docker compose up -d

# Producción
docker compose -f docker-compose.prod.yml up -d

Opción 2: OrangePi + Cloudflare (Auto-hosting)
bash

# Configuración automática para OrangePi 5+
sudo bash deploy/setup-orangepi.sh

🚀 Guía completa de deployment en OrangePi
❓ Preguntas Frecuentes

¿Necesito tarjeta de crédito?
No, el plan free es completamente gratuito sin requerir tarjeta.

¿Qué lenguajes soporta?
Actualmente solo Python. JavaScript/Go en desarrollo.

¿Mis códigos se almacenan?
Solo métricas y scores, nunca el código fuente.

¿Puedo usar en mi empresa?
Sí, el plan Enterprise incluye soporte corporativo.
📚 Documentación Adicional

    🏗️ Arquitectura del Sistema

    🔧 Configuración Avanzada

    🚀 Deployment OrangePi

    🐛 Reportar Issues

🛠️ Estado del Proyecto

✅ Listo para Producción - v1.0.0
✅ Completado	🚧 Próximamente
Análisis Python con Gemini 2.5	Panel administrativo
Dashboard interactivo	Soporte JavaScript/Go
Auth JWT + Security	Sistema de facturación
Deployment OrangePi	API más lenguajes
📄 Licencia

MIT License - Neural Code Analyzer
¿Preguntas? ✉️ gompatri@gmail.com

¿Te gusta el proyecto? ⭐ Dale una estrella en GitHub
