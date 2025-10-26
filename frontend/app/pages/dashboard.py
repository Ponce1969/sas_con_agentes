"""
Página de Dashboard - Estadísticas y métricas del usuario.
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# Configuración
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")

st.set_page_config(
    page_title="Dashboard - Neural Code Analyzer",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Dashboard")
st.markdown("### Estadísticas de tus análisis de código")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Filtros")
    
    # Selector de período
    periodo = st.selectbox(
        "Período",
        ["Hoy", "Esta Semana", "Este Mes", "Todo el Tiempo"]
    )
    
    # Usuario ID (temporal - hasta implementar auth)
    usuario_id = st.number_input(
        "Usuario ID",
        min_value=1,
        value=1,
        help="ID del usuario (temporal)"
    )
    
    st.markdown("---")
    
    # Botón de actualizar
    if st.button("🔄 Actualizar Datos", use_container_width=True):
        st.rerun()

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📝 Análisis Totales",
        value="0",
        delta=None,
        help="Total de análisis realizados"
    )

with col2:
    st.metric(
        label="📊 Score Promedio",
        value="0.0",
        delta=None,
        help="Score promedio de calidad de código"
    )

with col3:
    st.metric(
        label="🐛 Bugs Detectados",
        value="0",
        delta=None,
        help="Total de bugs potenciales detectados"
    )

with col4:
    st.metric(
        label="⚡ Mejoras Sugeridas",
        value="0",
        delta=None,
        help="Total de mejoras de rendimiento sugeridas"
    )

st.markdown("---")

# Gráficos y tablas
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Análisis en el Tiempo")
    
    # Placeholder para gráfico
    st.info("📊 Gráfico de análisis por día (próximamente)")
    
    # Tabla de análisis recientes
    st.subheader("📋 Análisis Recientes")
    
    # Datos de ejemplo (reemplazar con datos reales)
    st.dataframe(
        {
            "Fecha": ["2025-01-26", "2025-01-25", "2025-01-24"],
            "Código": ["función_suma.py", "clase_usuario.py", "api_handler.py"],
            "Score": [85, 72, 90],
            "Bugs": [2, 5, 1],
            "Mejoras": [3, 7, 2]
        },
        use_container_width=True
    )

with col_right:
    st.subheader("🏆 Top Problemas")
    
    # Problemas más comunes
    st.markdown("""
    **Bugs más frecuentes:**
    1. 🐛 Variables no definidas
    2. 🐛 División por cero
    3. 🐛 Imports faltantes
    
    **Code Smells:**
    1. 👃 Funciones muy largas
    2. 👃 Nombres poco descriptivos
    3. 👃 Código duplicado
    """)
    
    st.markdown("---")
    
    st.subheader("💡 Recomendaciones")
    st.info("""
    - Usa nombres descriptivos
    - Divide funciones grandes
    - Agrega type hints
    - Documenta tu código
    """)

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Realiza análisis regulares para mantener la calidad de tu código")

# Nota de desarrollo
st.warning("⚠️ **Nota:** Esta página está en desarrollo. Las estadísticas se cargarán desde la API próximamente.")
