"""
Página de Dashboard - Estadísticas y métricas del usuario.
"""

import streamlit as st
import pandas as pd
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

# Obtener historial de análisis
historial = st.session_state.get('historial_analisis', [])

# Sidebar
with st.sidebar:
    st.header("⚙️ Filtros")
    
    # Selector de período
    periodo = st.selectbox(
        "Período",
        ["Todo el Tiempo", "Hoy", "Esta Semana", "Este Mes"]
    )
    
    st.markdown("---")
    
    # Botón de actualizar
    if st.button("🔄 Actualizar Datos", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    # Info
    st.info(f"📊 **Total de análisis:** {len(historial)}")
    
    if st.button("🗑️ Limpiar Historial", use_container_width=True):
        st.session_state['historial_analisis'] = []
        st.rerun()

# Calcular métricas desde el historial
total_analisis = len(historial)

if total_analisis > 0:
    # Calcular score promedio
    scores = [h['score'] for h in historial if h['score'] is not None]
    score_promedio = round(sum(scores) / len(scores), 1) if scores else 0
    
    # Contar bugs y mejoras en los análisis
    bugs_detectados = sum(1 for h in historial if '🐛' in h.get('analisis_completo', ''))
    mejoras_sugeridas = sum(1 for h in historial if '⚡' in h.get('analisis_completo', ''))
else:
    score_promedio = 0
    bugs_detectados = 0
    mejoras_sugeridas = 0

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📝 Análisis Totales",
        value=total_analisis,
        delta=None,
        help="Total de análisis realizados"
    )

with col2:
    st.metric(
        label="📊 Score Promedio",
        value=f"{score_promedio}/100",
        delta=None,
        help="Score promedio de calidad de código"
    )

with col3:
    st.metric(
        label="🐛 Análisis con Bugs",
        value=bugs_detectados,
        delta=None,
        help="Análisis donde se detectaron bugs"
    )

with col4:
    st.metric(
        label="⚡ Análisis con Mejoras",
        value=mejoras_sugeridas,
        delta=None,
        help="Análisis con mejoras de rendimiento"
    )

st.markdown("---")

# Gráficos y tablas
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Análisis en el Tiempo")
    
    if total_analisis > 0:
        # Crear DataFrame con el historial
        df = pd.DataFrame(historial)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['fecha'] = df['timestamp'].dt.date
        
        # Gráfico de línea de scores
        if 'score' in df.columns and df['score'].notna().any():
            scores_df = df[df['score'].notna()].copy()
            scores_df = scores_df.sort_values('timestamp')
            
            st.line_chart(
                data=scores_df.set_index('timestamp')['score'],
                use_container_width=True,
                height=200
            )
        else:
            st.info("📊 Realiza más análisis para ver el gráfico de evolución")
    else:
        st.info("📊 Aún no hay análisis. Ve a la página principal para analizar código.")
    
    st.markdown("---")
    
    # Tabla de análisis recientes
    st.subheader("📋 Análisis Recientes")
    
    if total_analisis > 0:
        # Mostrar últimos 10 análisis
        df_recientes = pd.DataFrame(historial[-10:][::-1])  # Últimos 10, más reciente primero
        df_recientes['timestamp'] = pd.to_datetime(df_recientes['timestamp'])
        df_recientes['Fecha'] = df_recientes['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        df_recientes['Score'] = df_recientes['score'].fillna(0).astype(int)
        df_recientes['Código'] = df_recientes['codigo'].str[:50] + '...'
        
        st.dataframe(
            df_recientes[['Fecha', 'Código', 'Score', 'modelo']].rename(columns={'modelo': 'Modelo'}),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("📝 No hay análisis recientes. Comienza analizando código en la página principal.")

with col_right:
    st.subheader("📊 Estadísticas de Score")
    
    if total_analisis > 0 and scores:
        # Distribución de scores
        score_ranges = {
            "🟢 Excelente (90-100)": sum(1 for s in scores if s >= 90),
            "🟡 Bueno (70-89)": sum(1 for s in scores if 70 <= s < 90),
            "🟠 Regular (50-69)": sum(1 for s in scores if 50 <= s < 70),
            "🔴 Mejorable (<50)": sum(1 for s in scores if s < 50)
        }
        
        for rango, cantidad in score_ranges.items():
            if cantidad > 0:
                st.metric(rango, cantidad)
    else:
        st.info("📊 Realiza análisis para ver estadísticas de calidad")
    
    st.markdown("---")
    
    st.subheader("💡 Recomendaciones")
    
    if total_analisis > 0:
        if score_promedio >= 90:
            st.success("🎉 ¡Excelente trabajo! Tu código tiene alta calidad.")
        elif score_promedio >= 70:
            st.info("👍 Buen trabajo. Sigue mejorando tu código.")
        else:
            st.warning("⚠️ Hay margen de mejora. Revisa las sugerencias de los análisis.")
    
    st.markdown("""
    **Tips para mejorar tu código:**
    - ✅ Usa nombres descriptivos
    - ✅ Divide funciones grandes
    - ✅ Agrega type hints
    - ✅ Documenta tu código
    - ✅ Maneja excepciones
    """)

# Footer
st.markdown("---")
col_footer1, col_footer2 = st.columns(2)

with col_footer1:
    if total_analisis > 0:
        st.success(f"✅ Has realizado **{total_analisis}** análisis. ¡Sigue así!")
    else:
        st.info("💡 **Tip:** Ve a la página principal para comenzar a analizar tu código")

with col_footer2:
    if st.button("🏠 Ir a Análisis", use_container_width=True):
        st.switch_page("main.py")
