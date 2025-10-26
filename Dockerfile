# Dockerfile Unificado - Backend FastAPI + Frontend Streamlit
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    APP_HOME=/app

# Crear directorio de trabajo
WORKDIR $APP_HOME

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar UV usando pip (más confiable en Docker)
RUN pip install --no-cache-dir uv

# Copiar código de la aplicación primero (necesario para pyproject.toml)
COPY . .

# Dar permisos a los scripts ANTES de instalar
RUN chmod +x scripts/*.sh

# Instalar dependencias con UV (mucho más rápido que pip)
RUN uv sync --frozen

# Exponer puertos (FastAPI: 8000, Streamlit: 8501)
EXPOSE 8000 8501

# Comando por defecto: ejecutar script que levanta ambos servicios
CMD ["/bin/bash", "./scripts/start.sh"]
