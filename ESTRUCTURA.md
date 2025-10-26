# 📁 Estructura del Proyecto - Neural SaaS Platform

## 🎯 Organización General

```
Proyecto_Nueronal/
│
├── AGENTES.md/                    # 📚 Documentación del proyecto
│   ├── Proyecto.md               # Descripción general
│   ├── Arquitectura.md           # Arquitectura hexagonal
│   ├── Diagrama.md               # Diagramas del sistema
│   ├── Practicas_Python.md       # ⭐ Guía de estilo (IMPORTANTE)
│   ├── ROADMAP.md                # Plan de desarrollo 8 semanas
│   ├── MARKET_RESEARCH.md        # Investigación de mercado
│   └── MVP_PLAN.md               # Plan MVP 1 semana
│
├── project_saas/                  # 🚀 Código fuente
│   ├── Dockerfile                # Dockerfile unificado (backend + frontend)
│   ├── docker-compose.yml        # Orquestación de servicios
│   ├── pyproject.toml            # Dependencias Python (UV)
│   ├── uv.lock                   # Lock file de dependencias
│   ├── .env                      # Variables de entorno
│   ├── .env.example              # Plantilla de .env
│   │
│   ├── scripts/                  # 📜 Scripts de utilidad
│   │   ├── README.md             # Documentación de scripts
│   │   ├── start.sh              # Levantar servicios (Docker)
│   │   ├── dev.sh                # Desarrollo local
│   │   └── check-ports.sh        # Verificar puertos
│   │
│   ├── backend/                  # Backend FastAPI
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── main.py           # 🚀 Punto de entrada FastAPI
│   │   │   │
│   │   │   ├── core/             # ⚙️ Configuración y utilidades
│   │   │   │   ├── __init__.py
│   │   │   │   ├── config.py     # Settings con pydantic-settings
│   │   │   │   ├── logger.py     # Logging centralizado
│   │   │   │   └── security.py   # JWT, hashing passwords
│   │   │   │
│   │   │   ├── domain/           # 🎯 Lógica de negocio (sin deps externas)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py     # Entidades SQLAlchemy
│   │   │   │   ├── value_objects.py # Value Objects
│   │   │   │   ├── ports.py      # Interfaces (puertos)
│   │   │   │   └── events.py     # Eventos de dominio
│   │   │   │
│   │   │   ├── application/      # 📋 Casos de uso y servicios
│   │   │   │   ├── __init__.py
│   │   │   │   ├── analysis_service.py # Servicio de análisis de código
│   │   │   │   ├── embeddings_service.py # Servicio de embeddings
│   │   │   │   └── services.py   # Otros servicios
│   │   │   │
│   │   │   ├── infrastructure/   # 🔌 Implementaciones concretas
│   │   │   │   ├── __init__.py
│   │   │   │   ├── database.py   # Conexión DB (SQLAlchemy async)
│   │   │   │   ├── repositories.py # Repositorios concretos
│   │   │   │   ├── gemini_client.py # Cliente Gemini API
│   │   │   │   └── factories.py  # Factories para DI
│   │   │   │
│   │   │   └── web/              # 🌐 Capa de presentación
│   │   │       ├── __init__.py
│   │   │       └── routers/
│   │   │           ├── __init__.py
│   │   │           ├── health_router.py # Health check
│   │   │           ├── analysis_router.py # Análisis de código
│   │   │           └── embeddings_router.py # Embeddings
│   │   │
│   │   ├── start.sh              # Script Docker
│   │   ├── dev.sh                # Script desarrollo
│   │   ├── README.md             # Documentación principal
│   │   ├── CONTRIBUTING.md       # Guía de contribución
│   │   └── ESTRUCTURA.md         # Este archivo
│   │
│   ├── frontend/                 # Frontend Streamlit
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py           # 🎨 Punto de entrada Streamlit
│   │   │   │
│   │   │   ├── pages/            # 📄 Páginas de la app
│   │   │   │   ├── __init__.py
│   │   │   │   ├── login.py      # Página de login
│   │   │   │   ├── dashboard.py  # Dashboard principal
│   │   │   │   └── analysis.py   # Página de análisis
│   │   │   │
│   │   │   ├── components/       # 🧩 Componentes reutilizables
│   │   │   │   ├── __init__.py
│   │   │   │   ├── sidebar.py    # Sidebar
│   │   │   │   ├── code_editor.py # Editor de código
│   │   │   │   └── results_display.py # Visualización de resultados
│   │   │   │
│   │   │   ├── services/         # 🔌 Servicios (API client)
│   │   │   │   ├── __init__.py
│   │   │   │   └── api_client.py # Cliente HTTP para backend
│   │   │   │
│   │   │   ├── utils/            # 🛠️ Utilidades
│   │   │   │   ├── __init__.py
│   │   │   │   └── helpers.py    # Funciones auxiliares
│   │   │   │
│   │   │   └── config.toml       # ⚙️ Configuración Streamlit
│   │   │
│   │   └── ...
│   │
│   └── tests/                    # Tests unitarios
│       ├── __init__.py
│       │
│       ├── unit/                 # Tests unitarios
│       │   ├── __init__.py
│       │   ├── test_analysis_service.py
│       │   ├── test_gemini_client.py
│       │   └── test_repositories.py
│       │
│       ├── integration/          # Tests de integración
│       │   ├── __init__.py
│       │   ├── test_api_endpoints.py
│       │   └── test_database.py
│       │
│       ├── e2e/                  # Tests end-to-end
│       │   ├── __init__.py
│       │   └── test_full_flow.py
│       │
│       ├── fixtures/             # Fixtures compartidos
│       │   ├── __init__.py
│       │   └── sample_code.py
│       │
│       └── conftest.py           # Configuración pytest
│
└── Dockerfile                     # (Obsoleto - usar project_saas/Dockerfile)
```

---

## 🏗️ Estructura del Backend (Arquitectura Hexagonal)

```
backend/
└── app/
    ├── __init__.py
    │
    ├── main.py                    # 🚀 Punto de entrada FastAPI
    │
    ├── core/                      # ⚙️ Configuración y utilidades
    │   ├── __init__.py
    │   ├── config.py              # Settings con pydantic-settings
    │   ├── logger.py              # Logging centralizado
    │   └── security.py            # JWT, hashing passwords
    │
    ├── domain/                    # 🎯 Lógica de negocio (sin deps externas)
    │   ├── __init__.py
    │   ├── models.py              # Entidades SQLAlchemy
    │   ├── value_objects.py       # Value Objects
    │   ├── ports.py               # Interfaces (puertos)
    │   └── events.py              # Eventos de dominio
    │
    ├── application/               # 📋 Casos de uso y servicios
    │   ├── __init__.py
    │   ├── analysis_service.py    # Servicio de análisis de código
    │   ├── embeddings_service.py  # Servicio de embeddings
    │   └── services.py            # Otros servicios
    │
    ├── infrastructure/            # 🔌 Implementaciones concretas
    │   ├── __init__.py
    │   ├── database.py            # Conexión DB (SQLAlchemy async)
    │   ├── repositories.py        # Repositorios concretos
    │   ├── gemini_client.py       # Cliente Gemini API
    │   └── factories.py           # Factories para DI
    │
    └── web/                       # 🌐 Capa de presentación
        ├── __init__.py
        └── routers/
            ├── __init__.py
            ├── health_router.py   # Health check
            ├── analysis_router.py # Análisis de código
            └── embeddings_router.py # Embeddings
```

### Flujo de Dependencias (Hexagonal)

```
web/routers → application/services → domain/ports
                                           ↓
                                  infrastructure/adapters
```

**Reglas estrictas:**
- ❌ `domain/` NO puede importar de `infrastructure/` ni `web/`
- ❌ `application/` NO puede importar de `infrastructure/` ni `web/`
- ✅ `infrastructure/` implementa interfaces de `domain/`
- ✅ `web/` usa `application/` vía Dependency Injection

---

## 🎨 Estructura del Frontend (Streamlit)

```
frontend/
└── app/
    ├── __init__.py
    ├── main.py                    # 🎨 Punto de entrada Streamlit
    │
    ├── pages/                     # 📄 Páginas de la app
    │   ├── __init__.py
    │   ├── login.py               # Página de login
    │   ├── dashboard.py           # Dashboard principal
    │   └── analysis.py            # Página de análisis
    │
    ├── components/                # 🧩 Componentes reutilizables
    │   ├── __init__.py
    │   ├── sidebar.py             # Sidebar
    │   ├── code_editor.py         # Editor de código
    │   └── results_display.py     # Visualización de resultados
    │
    ├── services/                  # 🔌 Servicios (API client)
    │   ├── __init__.py
    │   └── api_client.py          # Cliente HTTP para backend
    │
    ├── utils/                     # 🛠️ Utilidades
    │   ├── __init__.py
    │   └── helpers.py             # Funciones auxiliares
    │
    └── config.toml                # ⚙️ Configuración Streamlit
```

---

## 🧪 Estructura de Tests

```
tests/
├── __init__.py
│
├── unit/                          # Tests unitarios
│   ├── __init__.py
│   ├── test_analysis_service.py
│   ├── test_gemini_client.py
│   └── test_repositories.py
│
├── integration/                   # Tests de integración
│   ├── __init__.py
│   ├── test_api_endpoints.py
│   └── test_database.py
│
├── e2e/                          # Tests end-to-end
│   ├── __init__.py
│   └── test_full_flow.py
│
├── fixtures/                      # Fixtures compartidos
│   ├── __init__.py
│   └── sample_code.py
│
└── conftest.py                    # Configuración pytest
```

---

## 📦 Archivos de Configuración

### Raíz del Proyecto

| Archivo | Propósito |
|---------|-----------|
| `pyproject.toml` | Dependencias, configuración de herramientas (Ruff, Black, mypy) |
| `uv.lock` | Lock file de dependencias (generado por UV) |
| `.ruff.toml` | Configuración detallada de Ruff |
| `.python-version` | Versión de Python (3.12) |
| `.gitignore` | Archivos a ignorar en Git |
| `.env` | Variables de entorno (NO commitear) |
| `Makefile` | Comandos útiles (`make dev`, `make test`, etc.) |
| `docker-compose.yml` | Orquestación de servicios |
| `Dockerfile` | Imagen Docker unificada |
| `start.sh` | Script de inicio para Docker |
| `dev.sh` | Script de desarrollo local |

### Frontend

| Archivo | Propósito |
|---------|-----------|
| `config.toml` | Configuración de Streamlit (tema, server, etc.) |

---

## 🔧 Convenciones de Nombres

### Archivos y Carpetas
- **snake_case** para archivos: `analysis_service.py`
- **snake_case** para carpetas: `web/routers/`

### Código Python
- **snake_case** para variables, funciones, métodos: `analizar_codigo()`
- **PascalCase** para clases: `AnalysisService`
- **UPPER_CASE** para constantes: `MAX_TOKENS = 1000`

### Tests
- Prefijo `test_` para archivos: `test_analysis_service.py`
- Prefijo `test_` para funciones: `def test_analyze_code_success():`

---

## 📚 Documentación por Tipo

### Documentación de Arquitectura
📍 Ubicación: `/AGENTES.md/`
- `Arquitectura.md` - Arquitectura hexagonal
- `Diagrama.md` - Diagramas del sistema
- `Practicas_Python.md` - Guía de estilo

### Documentación de Proyecto
📍 Ubicación: `/AGENTES.md/`
- `Proyecto.md` - Descripción general
- `ROADMAP.md` - Plan de desarrollo
- `MARKET_RESEARCH.md` - Investigación de mercado
- `MVP_PLAN.md` - Plan MVP

### Documentación de Código
📍 Ubicación: `/project_saas/`
- `README.md` - Documentación principal
- `CONTRIBUTING.md` - Guía de contribución
- `ESTRUCTURA.md` - Este archivo

### Documentación Inline
📍 Ubicación: En el código
- Docstrings en funciones y clases
- Type hints en todas las funciones

---

## 🎯 Flujo de Datos

### Request Flow (Backend)

```
1. HTTP Request
   ↓
2. web/routers/analysis_router.py
   ↓
3. Dependency Injection (get_analysis_service)
   ↓
4. application/analysis_service.py
   ↓
5. infrastructure/gemini_client.py (API externa)
   ↓
6. infrastructure/repositories.py (DB)
   ↓
7. Response
```

### Frontend → Backend Flow

```
1. Streamlit UI (frontend/app/main.py)
   ↓
2. API Client (frontend/app/services/api_client.py)
   ↓
3. HTTP Request → Backend
   ↓
4. Backend procesa (ver Request Flow)
   ↓
5. HTTP Response → Frontend
   ↓
6. Streamlit muestra resultados
```

---

## 🚀 Comandos Rápidos por Contexto

### Desarrollo
```bash
make dev          # Levantar backend + frontend
make backend      # Solo backend
make frontend     # Solo frontend
```

### Testing
```bash
make test         # Todos los tests
make test-cov     # Tests con cobertura
```

### Calidad de Código
```bash
make format       # Formatear código
make lint         # Linting
make typecheck    # Verificar tipos
```

### Docker
```bash
make docker-up    # Levantar con Docker
make docker-down  # Detener Docker
make docker-logs  # Ver logs
```

### Dependencias
```bash
make install      # Instalar deps
make add PKG=X    # Agregar dependencia
make update       # Actualizar deps
```

---

## 📖 Lectura Recomendada

Para entender mejor el proyecto, lee en este orden:

1. **`README.md`** - Empezar aquí
2. **`../AGENTES.md/Proyecto.md`** - Visión general
3. **`../AGENTES.md/Practicas_Python.md`** - ⭐ MUY IMPORTANTE
4. **`../AGENTES.md/Arquitectura.md`** - Arquitectura hexagonal
5. **`CONTRIBUTING.md`** - Antes de contribuir
6. **`../AGENTES.md/MVP_PLAN.md`** - Plan de desarrollo
7. **`../AGENTES.md/ROADMAP.md`** - Visión a largo plazo

---

## ✅ Checklist de Nuevo Desarrollador

Antes de empezar a codear:

- [ ] Leí `README.md`
- [ ] Leí `Practicas_Python.md` (IMPORTANTE)
- [ ] Instalé UV (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] Cloné el repo y ejecuté `uv sync`
- [ ] Configuré `.env` con mi `GEMINI_API_KEY`
- [ ] Ejecuté `make dev` y funciona
- [ ] Ejecuté `make test` y pasa
- [ ] Entiendo la arquitectura hexagonal
- [ ] Sé usar `make format` y `make lint`

---

**Última actualización:** Enero 2025
