# 🧠 Neural SaaS Platform

Plataforma SaaS de Agentes de IA para análisis de código Python.

## 🚀 Quick Start

### Prerequisitos
- Python 3.12+
- [UV](https://github.com/astral-sh/uv) instalado
- Docker y Docker Compose (opcional)
- API Key de Google Gemini

### Configuración

1. **Clonar el repositorio**
```bash
git clone <tu-repo>
cd project_saas
```

2. **Instalar UV (si no lo tienes)**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Configurar variables de entorno**
```bash
# Editar .env y agregar tu API key de Gemini
nano .env

# Cambiar esta línea:
GEMINI_API_KEY=tu_api_key_real_aqui
```

4. **Instalar dependencias con UV**
```bash
# UV sincroniza automáticamente las dependencias
uv sync

# O instalar manualmente
uv pip install -e .
```

5. **Levantar la aplicación**

**Opción A: Con Docker (recomendado para producción)**
```bash
# Verificar puertos disponibles primero
./check-ports.sh

# Con Docker Compose (verifica puertos automáticamente)
make docker-up

# O manualmente
docker-compose up --build
```

**⚠️ Nota sobre puertos:** Este proyecto usa puertos alternativos para evitar conflictos:
- PostgreSQL: `5433` (en lugar de 5432)
- Redis: `6380` (en lugar de 6379)
- Backend: `8001` (en lugar de 8000)
- Frontend: `8502` (en lugar de 8501)

Puedes cambiar estos puertos editando `.env`

**Opción B: Local con UV (recomendado para desarrollo)**
```bash
# Opción 1: Usando el script dev.sh (levanta ambos servicios)
./scripts/dev.sh

# Opción 2: Usando Makefile
make dev

# Opción 3: Manual (dos terminales)
# Terminal 1: Backend
uv run uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Frontend
uv run streamlit run frontend/app/main.py --server.port 8501
```

6. **Acceder a la aplicación**

**Con Docker (puertos alternativos):**
- **Frontend (Streamlit)**: http://localhost:8502
- **Backend API (FastAPI)**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health
- **PostgreSQL**: localhost:5433
- **Redis**: localhost:6380

**Con desarrollo local (puertos estándar):**
- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API (FastAPI)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Estructura del Proyecto

```
project_saas/
├── Dockerfile              # Dockerfile unificado (backend + frontend)
├── docker-compose.yml      # Orquestación de servicios
├── start.sh               # Script de inicio
├── requirements.txt       # Dependencias Python unificadas
├── .env                   # Variables de entorno
│
├── backend/               # Backend FastAPI
│   └── app/
│       ├── main.py
│       ├── core/          # Config, logger, security
│       ├── domain/        # Modelos de dominio
│       ├── application/   # Lógica de negocio
│       ├── infrastructure/# DB, clientes externos
│       └── web/routers/   # Endpoints API
│
└── frontend/              # Frontend Streamlit
    └── app/
        ├── main.py
        ├── pages/
        └── components/
```

## ✨ Features

- 🐛 **Detección de Bugs**: Identifica errores potenciales en tu código
- 👃 **Code Smells**: Detecta malas prácticas y código que "huele mal"
- ⚡ **Mejoras de Rendimiento**: Sugiere optimizaciones
- 📊 **Score de Calidad**: Calificación de 0-100 de tu código
- 🧠 **Powered by Gemini**: Análisis con IA de última generación

## 🏗️ Arquitectura

- **Backend**: FastAPI con arquitectura hexagonal
- **Frontend**: Streamlit para UI rápida e intuitiva
- **Base de Datos**: PostgreSQL con pgvector
- **Cache**: Redis para Celery
- **IA**: Google Gemini API

## 🛠️ Desarrollo

### Comandos Rápidos con Makefile

```bash
make help          # Ver todos los comandos disponibles
make install       # Instalar dependencias
make dev           # Levantar backend + frontend
make test          # Ejecutar tests
make lint          # Linting con Ruff
make format        # Formatear código
make docker-up     # Levantar con Docker
```

### Levantar en modo desarrollo
```bash
# Backend (puerto 8000)
uv run uvicorn backend.app.main:app --reload --port 8000

# Frontend (puerto 8501)
uv run streamlit run frontend/app/main.py --server.port 8501
```

### Instalar dependencias de desarrollo
```bash
uv sync --extra dev
```

### Tests
```bash
uv run pytest tests/
```

### Linting y Formateo
```bash
# Formatear código con Black
uv run black .

# Linting con Ruff
uv run ruff check .

# Type checking con mypy
uv run mypy .
```

### Agregar nuevas dependencias
```bash
# Agregar dependencia de producción
uv add nombre-paquete

# Agregar dependencia de desarrollo
uv add --dev nombre-paquete

# Actualizar todas las dependencias
uv lock --upgrade
```

## 📚 Documentación

### Documentación del Código (en este directorio):
- [CONFIG.md](CONFIG.md) - ⚙️ Gestión de configuración (.env)
- [DEPENDENCIES.md](DEPENDENCIES.md) - 📦 Gestión de dependencias con UV
- [CONTRIBUTING.md](CONTRIBUTING.md) - 🤝 Guía de contribución
- [ESTRUCTURA.md](ESTRUCTURA.md) - 📁 Estructura del proyecto

### Documentación del Proyecto (en `../AGENTES.md/`):
- [ROADMAP.md](../AGENTES.md/ROADMAP.md) - Plan de desarrollo completo
- [MARKET_RESEARCH.md](../AGENTES.md/MARKET_RESEARCH.md) - Investigación de mercado
- [MVP_PLAN.md](../AGENTES.md/MVP_PLAN.md) - Plan del MVP
- [Practicas_Python.md](../AGENTES.md/Practicas_Python.md) - Guía de estilo y arquitectura
- [Arquitectura.md](../AGENTES.md/Arquitectura.md) - Arquitectura del sistema
- [Proyecto.md](../AGENTES.md/Proyecto.md) - Descripción general

## 🤝 Contribuir

Este proyecto está en fase MVP. Feedback y contribuciones son bienvenidos!

## 📝 Licencia

MIT License

---

**Made with ❤️ by Neural SaaS Platform**
