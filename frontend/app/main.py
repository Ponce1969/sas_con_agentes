# frontend/app/main.py

import streamlit as st
import requests
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="Neural Code Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL del backend (desde variable de entorno o default)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")

# Título principal
st.title("🧠 Neural Code Analyzer")
st.markdown("### Analiza tu código Python con IA")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # URL del backend (editable)
    backend_url = st.text_input(
        "URL del Backend",
        value=BACKEND_URL,
        help="URL de la API FastAPI"
    )
    
    st.markdown("---")
    
    # Estadísticas (placeholder)
    st.markdown("### 📊 Estadísticas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Análisis Hoy", "0")
    with col2:
        st.metric("Score Promedio", "0")
    
    st.markdown("---")
    
    # Información
    st.markdown("### ℹ️ Información")
    st.markdown("""
    **Neural Code Analyzer** usa IA para:
    - 🐛 Detectar bugs potenciales
    - 👃 Identificar code smells
    - ⚡ Sugerir mejoras de rendimiento
    - 📊 Calcular score de calidad
    """)
    
    st.markdown("---")
    st.markdown("**Versión:** 0.1.0 MVP")

# Layout principal con dos columnas
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📝 Tu Código Python")
    
    # Editor de código
    codigo_input = st.text_area(
        "Pega tu código Python aquí:",
        height=400,
        placeholder="""def ejemplo():
    # Tu código aquí
    pass""",
        help="Escribe o pega el código Python que quieres analizar"
    )
    
    # Botón de análisis
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        analizar_button = st.button(
            "🔍 Analizar Código",
            type="primary",
            use_container_width=True
        )
    
    with col_btn2:
        limpiar_button = st.button(
            "🗑️ Limpiar",
            use_container_width=True
        )
    
    with col_btn3:
        ejemplo_button = st.button(
            "📄 Ejemplo",
            use_container_width=True
        )
    
    # Información del código
    if codigo_input:
        lineas = len(codigo_input.split('\n'))
        caracteres = len(codigo_input)
        st.caption(f"📏 {lineas} líneas | {caracteres} caracteres")

with col_right:
    st.subheader("📊 Resultados del Análisis")
    
    # Contenedor para resultados
    results_container = st.container()

# Lógica de botones
if limpiar_button:
    st.rerun()

if ejemplo_button:
    codigo_ejemplo = """def calcular_promedio(numeros):
    suma = 0
    for num in numeros:
        suma = suma + num
    return suma / len(numeros)

# Uso
lista = [1, 2, 3, 4, 5]
resultado = calcular_promedio(lista)
print(resultado)"""
    st.session_state['codigo_ejemplo'] = codigo_ejemplo
    st.rerun()

# Cargar ejemplo si existe en session_state
if 'codigo_ejemplo' in st.session_state:
    codigo_input = st.session_state['codigo_ejemplo']
    del st.session_state['codigo_ejemplo']

# Análisis
if analizar_button:
    if not codigo_input or not codigo_input.strip():
        with results_container:
            st.error("⚠️ Por favor ingresa código para analizar")
    else:
        with results_container:
            with st.spinner("🤖 Analizando tu código..."):
                try:
                    # Llamar al backend
                    response = requests.post(
                        f"{backend_url}/api/analysis/",
                        json={"codigo": codigo_input},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Mostrar resultados
                        st.success("✅ Análisis completado!")
                        
                        # Timestamp
                        st.caption(f"🕐 {data.get('timestamp', 'N/A')}")
                        
                        # Análisis en markdown
                        st.markdown(data.get("analisis", "No se recibió análisis"))
                        
                        # Información adicional
                        with st.expander("ℹ️ Información del Análisis"):
                            st.json({
                                "modelo_usado": data.get("modelo_usado", "N/A"),
                                "usuario_id": data.get("usuario_id", "Anónimo"),
                                "timestamp": data.get("timestamp", "N/A")
                            })
                        
                        # Botón para descargar
                        st.download_button(
                            label="📥 Descargar Análisis",
                            data=data.get("analisis", ""),
                            file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                        
                    else:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏱️ Timeout: El análisis tomó demasiado tiempo. Intenta con código más corto.")
                    
                except requests.exceptions.ConnectionError:
                    st.error(f"❌ No se pudo conectar al backend en {backend_url}")
                    st.info("💡 Asegúrate de que el backend esté corriendo en el puerto correcto")
                    
                except Exception as e:
                    st.error(f"❌ Error inesperado: {str(e)}")

# Footer
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([1, 1, 1])

with col_footer1:
    st.markdown("Made with ❤️ by **Neural SaaS Platform**")

with col_footer2:
    st.markdown(f"Backend: `{backend_url}`")

with col_footer3:
    if st.button("🔄 Verificar Backend"):
        try:
            response = requests.get(f"{backend_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend conectado")
            else:
                st.error("❌ Backend no responde")
        except:
            st.error("❌ Backend no disponible")
