#!/bin/bash

echo "🚀 Iniciando Neural SaaS Platform..."

# Levantar FastAPI en background
echo "📡 Levantando Backend FastAPI en puerto 8000..."
cd /app && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &

# Esperar un poco para que FastAPI inicie
sleep 3

# Levantar Streamlit en foreground
echo "🎨 Levantando Frontend Streamlit en puerto 8501..."
streamlit run frontend/app/main.py --server.port 8501 --server.address 0.0.0.0 --server.headless true

# Si Streamlit termina, matar FastAPI también
kill $(jobs -p)
