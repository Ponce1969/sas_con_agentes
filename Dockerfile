# Dockerfile Unificado - Backend FastAPI + Frontend Streamlit
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    APP_HOME=/app

# Crear directorio de trabajo
WORKDIR $APP_HOME

# Instalar dependencias del sistema y UV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Agregar UV al PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock* ./

# Instalar dependencias con UV (mucho más rápido que pip)
RUN uv sync --frozen

# Copiar código de la aplicación
COPY . .

# Exponer puertos (FastAPI: 8000, Streamlit: 8501)
EXPOSE 8000 8501

# Copiar y dar permisos a los scripts
RUN chmod +x scripts/*.sh

# Comando por defecto: ejecutar script que levanta ambos servicios
CMD ["./scripts/start.sh"]
