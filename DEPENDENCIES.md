# 📦 Gestión de Dependencias - Neural SaaS Platform

## 🎯 Sistema de Dependencias

Este proyecto usa **UV** como gestor de dependencias, NO pip ni requirements.txt.

### Archivos Importantes:

```
project_saas/
├── pyproject.toml    # ✅ Definición de dependencias
├── uv.lock           # ✅ Lock file (generado automáticamente)
└── .python-version   # ✅ Versión de Python (3.12)
```

### ❌ NO usar:
- `requirements.txt` (obsoleto)
- `pip install` (usar `uv` en su lugar)
- `pip freeze` (usar `uv lock` en su lugar)

---

## 🚀 Comandos Básicos

### Instalar Dependencias

```bash
# Primera vez o después de pull
uv sync

# Con dependencias de desarrollo
uv sync --extra dev

# Forzar reinstalación
uv sync --reinstall
```

### Agregar Dependencias

```bash
# Dependencia de producción
uv add nombre-paquete

# Ejemplo: agregar httpx
uv add httpx

# Dependencia de desarrollo
uv add --dev nombre-paquete

# Ejemplo: agregar pytest
uv add --dev pytest

# Con versión específica
uv add "fastapi==0.109.0"
```

### Remover Dependencias

```bash
# Remover dependencia
uv remove nombre-paquete

# Ejemplo
uv remove httpx
```

### Actualizar Dependencias

```bash
# Actualizar todas las dependencias
uv lock --upgrade

# Actualizar una dependencia específica
uv add nombre-paquete --upgrade

# Ver dependencias desactualizadas
uv pip list --outdated
```

---

## 📋 Estructura de pyproject.toml

```toml
[project]
name = "neural-saas-platform"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    # Backend
    "fastapi==0.109.0",
    "uvicorn[standard]==0.27.0",
    
    # Frontend
    "streamlit==1.30.0",
    
    # IA
    "google-generativeai==0.3.2",
    
    # ... más dependencias
]

[project.optional-dependencies]
dev = [
    "pytest==7.4.3",
    "black==23.12.1",
    "ruff==0.1.9",
    "mypy==1.8.0",
]
```

---

## 🔒 UV Lock File

### ¿Qué es uv.lock?

- **Lock file determinístico**: Asegura que todos instalen las mismas versiones
- **Generado automáticamente**: Se actualiza con `uv lock`
- **Debe commitearse**: Sí, debe estar en Git

### Cuándo se actualiza:

- Cuando ejecutas `uv add` o `uv remove`
- Cuando ejecutas `uv lock`
- Cuando ejecutas `uv lock --upgrade`

### NO editar manualmente:

❌ No edites `uv.lock` a mano  
✅ Edita `pyproject.toml` y ejecuta `uv lock`

---

## 🎯 Flujo de Trabajo

### Agregar Nueva Dependencia

```bash
# 1. Agregar dependencia
uv add nombre-paquete

# 2. UV actualiza automáticamente:
#    - pyproject.toml
#    - uv.lock

# 3. Commit ambos archivos
git add pyproject.toml uv.lock
git commit -m "feat: agregar dependencia nombre-paquete"
```

### Después de Pull

```bash
# Sincronizar dependencias
uv sync

# UV lee uv.lock e instala las versiones exactas
```

### Actualizar Dependencias

```bash
# 1. Actualizar lock file
uv lock --upgrade

# 2. Revisar cambios
git diff uv.lock

# 3. Probar que todo funciona
make test

# 4. Commit
git add uv.lock
git commit -m "chore: actualizar dependencias"
```

---

## 🐳 Docker y UV

### Dockerfile usa UV

```dockerfile
# Instalar UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock* ./

# Instalar con UV (frozen = no actualizar)
RUN uv sync --frozen
```

### ¿Por qué `--frozen`?

- No actualiza `uv.lock`
- Usa versiones exactas del lock file
- Build reproducible

---

## 📊 Comparación: pip vs UV

| Característica | pip + requirements.txt | UV + pyproject.toml |
|----------------|------------------------|---------------------|
| **Velocidad** | Lento | 10-100x más rápido ⚡ |
| **Lock file** | Manual (`pip freeze`) | Automático (`uv.lock`) |
| **Resolución** | Básica | Avanzada (Rust) |
| **Reproducibilidad** | Baja | Alta 🔒 |
| **Instalación paralela** | No | Sí |
| **Cache inteligente** | Limitado | Sí |

---

## 🛠️ Comandos Útiles

### Ver Dependencias Instaladas

```bash
# Listar todas
uv pip list

# Listar solo producción
uv pip list --exclude-editable

# Ver árbol de dependencias
uv pip show nombre-paquete
```

### Verificar Dependencias

```bash
# Ver dependencias desactualizadas
uv pip list --outdated

# Verificar conflictos
uv pip check
```

### Limpiar Cache

```bash
# Limpiar cache de UV
uv cache clean

# Limpiar todo
rm -rf .uv/
```

---

## 🚨 Problemas Comunes

### Error: "No module named 'X'"

```bash
# Solución: Sincronizar dependencias
uv sync
```

### Error: "Conflicto de versiones"

```bash
# Solución: Actualizar lock file
uv lock --upgrade
```

### Error: "uv: command not found"

```bash
# Solución: Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

### Dependencia no se instala

```bash
# Solución: Reinstalar todo
uv sync --reinstall
```

---

## 📚 Dependencias del Proyecto

### Backend (FastAPI)

```toml
# API Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Base de datos
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1

# Seguridad
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# HTTP Client
httpx==0.26.0
requests==2.31.0

# Utilidades
python-dotenv==1.0.0
redis==5.0.1
celery==5.3.6

# IA
google-generativeai==0.3.2

# Logging
loguru==0.7.2
```

### Frontend (Streamlit)

```toml
# UI Framework
streamlit==1.30.0

# Visualización
plotly==5.18.0
pandas==2.1.4
```

### Desarrollo

```toml
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Linting y Formateo
black==23.12.1
ruff==0.1.9
mypy==1.8.0
```

---

## 🎯 Buenas Prácticas

### ✅ DO:

- Usar `uv add` para agregar dependencias
- Commitear `pyproject.toml` y `uv.lock` juntos
- Ejecutar `uv sync` después de pull
- Especificar versiones en producción
- Usar `--frozen` en Docker

### ❌ DON'T:

- No usar `pip install`
- No crear `requirements.txt`
- No editar `uv.lock` manualmente
- No ignorar `uv.lock` en Git
- No usar versiones sin pin en producción

---

## 📖 Referencias

- [UV Documentation](https://github.com/astral-sh/uv)
- [pyproject.toml Specification](https://peps.python.org/pep-0621/)
- [Python Packaging Guide](https://packaging.python.org/)

---

**Última actualización:** Enero 2025
