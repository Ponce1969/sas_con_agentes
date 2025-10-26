#!/bin/bash

echo "🚀 Iniciando Neural SaaS Platform..."

# Activar el entorno virtual
source /app/.venv/bin/activate

# Levantar FastAPI en background
echo "📡 Levantando Backend FastAPI en puerto 8000..."
cd /app/backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Esperar un poco para que FastAPI inicie
sleep 5

# Levantar Streamlit en foreground
echo "🎨 Levantando Frontend Streamlit en puerto 8501..."
cd /app && python -m streamlit run frontend/app/main.py --server.port 8501 --server.address 0.0.0.0 --server.headless true

# Si Streamlit termina, matar FastAPI también
kill $(jobs -p)
