# 🤝 Guía de Contribución - Neural SaaS Platform

## 📋 Tabla de Contenidos
- [Principios de Código](#principios-de-código)
- [Configuración del Entorno](#configuración-del-entorno)
- [Flujo de Trabajo](#flujo-de-trabajo)
- [Estándares de Código](#estándares-de-código)
- [Testing](#testing)
- [Documentación](#documentación)

---

## 🎯 Principios de Código

Este proyecto sigue las **Prácticas de Python** definidas en [`../AGENTES.md/Practicas_Python.md`](../AGENTES.md/Practicas_Python.md).

### Principios Clave:

1. **Python 3.12+** obligatorio
2. **Tipado estricto** en todas las funciones (`mypy`)
3. **Ruff** como linter principal
4. **snake_case** obligatorio para variables, funciones y métodos
5. **Arquitectura Hexagonal** estricta
6. **Factory + DI** para todas las dependencias

---

## ⚙️ Configuración del Entorno

### 1. Instalar UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clonar y configurar
```bash
git clone <repo>
cd project_saas
uv sync --extra dev
```

### 3. Configurar pre-commit hooks (opcional)
```bash
uv run pre-commit install
```

---

## 🔄 Flujo de Trabajo

### 1. Crear una rama
```bash
git checkout -b feature/nombre-feature
```

### 2. Desarrollar con linting automático
```bash
# Levantar en modo desarrollo
make dev

# En otra terminal, ejecutar linting en watch mode
make lint
```

### 3. Antes de commit
```bash
# Formatear código
make format

# Verificar tipos
make typecheck

# Ejecutar tests
make test

# Verificar todo
make lint && make typecheck && make test
```

### 4. Commit siguiendo Conventional Commits
```bash
git commit -m "feat: agregar análisis de complejidad ciclomática"
git commit -m "fix: corregir bug en gemini_client"
git commit -m "docs: actualizar README con nuevas features"
```

### 5. Push y Pull Request
```bash
git push origin feature/nombre-feature
# Crear PR en GitHub
```

---

## 📏 Estándares de Código

### Naming Conventions

```python
# ✅ CORRECTO - snake_case
def analizar_codigo(codigo_fuente: str) -> dict[str, Any]:
    resultado_analisis = {}
    return resultado_analisis

# ❌ INCORRECTO - camelCase
def analizarCodigo(codigoFuente: str) -> dict[str, Any]:
    resultadoAnalisis = {}
    return resultadoAnalisis
```

### Tipado Estricto

```python
# ✅ CORRECTO - Tipado completo
from typing import Optional

def obtener_usuario(user_id: int) -> Optional[Usuario]:
    """Obtiene un usuario por ID."""
    return db.query(Usuario).filter(Usuario.id == user_id).first()

# ❌ INCORRECTO - Sin tipos
def obtener_usuario(user_id):
    return db.query(Usuario).filter(Usuario.id == user_id).first()
```

### Factory + Dependency Injection

```python
# ✅ CORRECTO - Factory + DI
from typing import AsyncGenerator
from fastapi import Depends

async def get_analysis_service() -> AsyncGenerator[AnalysisService, None]:
    """Factory para AnalysisService."""
    service = AnalysisService(gemini_client=GeminiClient())
    yield service

@router.post("/analyze")
async def analyze(
    code: str,
    service: AnalysisService = Depends(get_analysis_service)
) -> AnalysisResponse:
    return await service.analyze(code)

# ❌ INCORRECTO - Instanciación directa
@router.post("/analyze")
async def analyze(code: str) -> AnalysisResponse:
    service = AnalysisService()  # ❌ No usar instanciación directa
    return await service.analyze(code)
```

### Arquitectura Hexagonal

```
✅ CORRECTO - Separación de capas:

backend/app/
├── core/           # Configuración, logging, seguridad
├── domain/         # Entidades, value objects (sin deps externas)
├── application/    # Casos de uso, servicios
├── infrastructure/ # DB, APIs externas, implementaciones
└── web/           # Routers, schemas FastAPI

❌ INCORRECTO:
- domain/ importando de infrastructure/
- web/ con lógica de negocio
- application/ con queries SQL directas
```

---

## 🧪 Testing

### Estructura de Tests

```python
# tests/test_analysis_service.py
import pytest
from backend.app.application.analysis_service import AnalysisService

@pytest.mark.asyncio
async def test_analyze_code_success() -> None:
    """Test que el análisis de código funciona correctamente."""
    # Arrange
    service = AnalysisService()
    code = "def suma(a, b): return a + b"
    
    # Act
    result = await service.analyze(code)
    
    # Assert
    assert result["success"] is True
    assert "analysis" in result
```

### Ejecutar Tests

```bash
# Todos los tests
make test

# Con cobertura
make test-cov

# Tests específicos
uv run pytest tests/test_analysis_service.py -v

# Tests en watch mode
uv run pytest-watch
```

---

## 🎨 Linting y Formateo

### Comandos Disponibles

```bash
# Formatear código (Black)
make format

# Linting (Ruff)
make lint

# Autofix de linting
uv run ruff check --fix .

# Type checking (mypy)
make typecheck

# Todo junto
make format && make lint && make typecheck
```

### Configuración de Ruff

El proyecto usa `.ruff.toml` con las siguientes reglas activadas:

- **E, F**: pycodestyle y pyflakes (errores básicos)
- **I**: isort (imports ordenados)
- **N**: pep8-naming (snake_case obligatorio)
- **UP**: pyupgrade (Python 3.12+)
- **B**: flake8-bugbear (bugs comunes)
- **C4**: flake8-comprehensions
- **SIM**: flake8-simplify
- **TCH**: flake8-type-checking

---

## 📝 Documentación

### Docstrings

```python
def analizar_codigo(codigo: str, opciones: dict[str, Any]) -> AnalysisResult:
    """
    Analiza código Python y retorna sugerencias de mejora.
    
    Args:
        codigo: Código Python a analizar
        opciones: Opciones de análisis (profundidad, reglas, etc.)
    
    Returns:
        AnalysisResult con bugs, code smells y score de calidad
    
    Raises:
        ValueError: Si el código está vacío
        GeminiAPIError: Si falla la llamada a Gemini
    
    Example:
        >>> result = analizar_codigo("def suma(a, b): return a + b", {})
        >>> result.score
        95
    """
    if not codigo.strip():
        raise ValueError("El código no puede estar vacío")
    
    # ... implementación
```

### Comentarios

```python
# ✅ CORRECTO - Código autoexplicativo, sin comentarios innecesarios
def calcular_score_calidad(metricas: dict[str, float]) -> int:
    peso_bugs = 0.4
    peso_smells = 0.3
    peso_complejidad = 0.3
    
    score = (
        metricas["bugs"] * peso_bugs +
        metricas["smells"] * peso_smells +
        metricas["complejidad"] * peso_complejidad
    )
    return int(score * 100)

# ❌ INCORRECTO - Comentarios obvios
def calcular_score_calidad(metricas: dict[str, float]) -> int:
    # Definir peso de bugs
    peso_bugs = 0.4
    # Definir peso de smells
    peso_smells = 0.3
    # Definir peso de complejidad
    peso_complejidad = 0.3
    
    # Calcular score
    score = (
        metricas["bugs"] * peso_bugs +  # Multiplicar bugs por peso
        metricas["smells"] * peso_smells +  # Multiplicar smells por peso
        metricas["complejidad"] * peso_complejidad  # Multiplicar complejidad por peso
    )
    # Retornar score multiplicado por 100
    return int(score * 100)
```

---

## 🚫 Anti-Patrones a Evitar

### 1. No usar Singleton
```python
# ❌ INCORRECTO
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# ✅ CORRECTO - Usar Factory + DI
async def get_db_connection() -> AsyncGenerator[Connection, None]:
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()
```

### 2. No usar datetime estándar
```python
# ❌ INCORRECTO
from datetime import datetime
now = datetime.now()

# ✅ CORRECTO
from zoneinfo import ZoneInfo
from datetime import datetime
now = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
```

### 3. No usar bcrypt directamente
```python
# ❌ INCORRECTO
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ✅ CORRECTO - Usar Argon2
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
hashed = pwd_context.hash(password)
```

---

## 📚 Recursos

- [Prácticas de Python](../AGENTES.md/Practicas_Python.md) - Guía completa
- [Arquitectura](../AGENTES.md/Arquitectura.md) - Arquitectura hexagonal
- [Ruff Docs](https://docs.astral.sh/ruff/) - Documentación de Ruff
- [mypy Docs](https://mypy.readthedocs.io/) - Documentación de mypy
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/) - FastAPI

---

## ❓ Preguntas Frecuentes

### ¿Por qué UV en lugar de pip?
UV es 10-100x más rápido que pip y tiene mejor resolución de dependencias.

### ¿Por qué Ruff en lugar de flake8/pylint?
Ruff es mucho más rápido (escrito en Rust) y combina múltiples herramientas en una.

### ¿Por qué snake_case si Python permite otros estilos?
Consistencia y legibilidad. Todo el proyecto usa snake_case para mantener uniformidad.

### ¿Puedo usar camelCase para clases?
Sí, las clases usan PascalCase (ej: `AnalysisService`), pero métodos y variables usan snake_case.

---

**¿Dudas?** Abre un issue o pregunta en el canal de desarrollo.
