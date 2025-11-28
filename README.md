# 🧠 Neural Code Analyzer

**Plataforma SaaS para análisis de código Python con IA (Gemini 2.5 Flash)**

> **Versión:** 1.0.0-beta | **Estado:** MVP Funcional

---

## 🚀 Quick Start

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/Ponce1969/sas_con_agentes.git
cd project_saas

# 2. Configurar API Key de Gemini
cp .env.example .env
nano .env  # Agregar: GEMINI_API_KEY=tu_key

# 3. Instalar dependencias
uv sync

# 4. Levantar servicios
make dev  # O: docker-compose up --build
```

**URLs:**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

---

## ✨ Features

| Feature | Descripción |
|---------|-------------|
| 🐛 **Detección de Bugs** | Identifica errores potenciales |
| 👃 **Code Smells** | Detecta malas prácticas |
| ⚡ **Optimización** | Sugiere mejoras de rendimiento |
| 📊 **Score 0-100** | Calificación de calidad |
| 🧠 **Gemini 2.5 Flash** | IA de última generación |

---

## 📁 Estructura

```
project_saas/
├── backend/app/           # FastAPI (arquitectura hexagonal)
│   ├── core/              # Config, logger
│   ├── domain/            # Modelos
│   ├── application/       # Servicios
│   ├── infrastructure/    # DB, Gemini client
│   └── web/routers/       # Endpoints
├── frontend/app/          # Streamlit UI
├── docker-compose.yml     # Orquestación
└── pyproject.toml         # Dependencias (UV)
```

---

## 🛠️ Comandos

```bash
make dev          # Desarrollo local
make docker-up    # Docker completo
make test         # Tests
make lint         # Linting (Ruff)
make format       # Formateo (Black)
```

---

## 📚 Documentación

| Archivo | Contenido |
|---------|-----------|
| [CONFIG.md](../AGENTES.md/CONFIG.md) | Variables de entorno |
| [ESTRUCTURA.md](../AGENTES.md/ESTRUCTURA.md) | Arquitectura hexagonal |
| [MEJORAS_PROFESIONALES.md](../AGENTES.md/MEJORAS_PROFESIONALES.md) | Roadmap v1 → v2 |

---

## 🎯 Roadmap v1.0

- [x] MVP funcional con Gemini
- [x] Docker optimizado
- [ ] Autenticación JWT
- [ ] PostgreSQL activo
- [ ] Rate limiting
- [ ] Tests (60% cobertura)
- [ ] CI/CD GitHub Actions

---

## 🏗️ Stack

- **Backend:** FastAPI + Python 3.12
- **Frontend:** Streamlit
- **IA:** Google Gemini 2.5 Flash
- **DB:** PostgreSQL + Redis
- **Tools:** UV, Docker, Ruff, Black

---

## 📝 Licencia

MIT License

**Made with ❤️ by Neural SaaS Platform**
