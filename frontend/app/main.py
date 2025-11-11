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
# Dentro del contenedor Docker, ambos servicios están en localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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

# Preparar valor inicial del editor (ANTES de renderizar)
valor_inicial = ""

# Cargar ejemplo si existe en session_state
if 'codigo_ejemplo' in st.session_state:
    valor_inicial = st.session_state['codigo_ejemplo']
    del st.session_state['codigo_ejemplo']

# Cargar código mejorado si se aplicó (tiene prioridad)
if 'codigo_aplicado' in st.session_state:
    valor_inicial = st.session_state['codigo_aplicado']
    del st.session_state['codigo_aplicado']

# Layout principal con dos columnas
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📝 Tu Código Python")
    
    # Editor de código
    codigo_input = st.text_area(
        "Pega tu código Python aquí:",
        value=valor_inicial,
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

# Mostrar mensaje de éxito si se aplicó código (al inicio para que sea visible)
if 'mostrar_mensaje_aplicado' in st.session_state:
    st.success("✅ ¡Código mejorado aplicado exitosamente! El editor se ha actualizado con las sugerencias.")
    del st.session_state['mostrar_mensaje_aplicado']

# Mostrar último análisis si existe (después de aplicar sugerencias)
if 'ultimo_analisis' in st.session_state and not analizar_button:
    with results_container:
        data = st.session_state['ultimo_analisis']
        
        # Mostrar resultados
        st.success("✅ Análisis completado!")
        
        # Timestamp
        st.caption(f"🕐 {data.get('timestamp', 'N/A')}")
        
        # Análisis en markdown
        analisis_text = data.get("analisis", "No se recibió análisis")
        
        # Extraer código mejorado del análisis
        codigo_mejorado = None
        import re
        
        # Intentar múltiples patrones para extraer el código
        if "Código Mejorado" in analisis_text or "Codigo Mejorado" in analisis_text:
            patterns = [
                r'##\s*✨\s*Código Mejorado.*?```python\s*(.*?)\s*```',
                r'✨\s*Código Mejorado.*?```python\s*(.*?)\s*```',
                r'Código Mejorado.*?```python\s*(.*?)\s*```',
                r'##\s*✨\s*Codigo Mejorado.*?```python\s*(.*?)\s*```',
                r'✨\s*Codigo Mejorado.*?```python\s*(.*?)\s*```',
                r'Codigo Mejorado.*?```python\s*(.*?)\s*```',
                # Sin especificador python
                r'Código Mejorado.*?```\s*(def .*?)\s*```',
                r'Codigo Mejorado.*?```\s*(def .*?)\s*```',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, analisis_text, re.DOTALL | re.IGNORECASE)
                if match:
                    codigo_mejorado = match.group(1).strip()
                    # Limpiar comentarios iniciales si existen
                    if codigo_mejorado.startswith('#'):
                        lines = codigo_mejorado.split('\n')
                        # Encontrar la primera línea que no es comentario
                        for i, line in enumerate(lines):
                            if line.strip() and not line.strip().startswith('#'):
                                codigo_mejorado = '\n'.join(lines[i:])
                                break
                    break
        
        # Eliminar la sección de código mejorado del análisis para evitar duplicación
        if codigo_mejorado:
            # Eliminar completamente la sección de código mejorado del texto de análisis
            # Patrón principal: desde "✨" seguido de cualquier variación de "Código Mejorado" hasta "📝 Cambios"
            analisis_sin_codigo = re.sub(
                r'#+?\s*✨\s*[CcóÓ].*?(?=📝)',
                '',
                analisis_text,
                flags=re.MULTILINE | re.DOTALL
            )
            
            # Limpiar cualquier línea que solo contenga emoji ✨ con o sin letra
            analisis_sin_codigo = re.sub(r'\n?\s*✨\s*[A-Za-z]?\s*\n?', '\n', analisis_sin_codigo)
            
            # Limpiar líneas vacías múltiples
            analisis_sin_codigo = re.sub(r'\n{3,}', '\n\n', analisis_sin_codigo)
            analisis_sin_codigo = re.sub(r'\s+$', '', analisis_sin_codigo, flags=re.MULTILINE)
            st.markdown(analisis_sin_codigo.strip())
        else:
            st.markdown(analisis_text)
        
        # Mostrar código mejorado en bloque copiable
        if codigo_mejorado:
            st.markdown("---")
            st.markdown("### 💻 Versión Optimizada del Código")
            st.info("💡 **Consejos de uso:**\n- Copia el código usando el icono 📋 (arriba a la derecha)\n- O aplica directamente con el botón '✨ Aplicar Sugerencias' (más abajo)")
            st.code(codigo_mejorado, language="python", line_numbers=True)
            st.success(f"✅ Código optimizado listo ({len(codigo_mejorado)} caracteres)")
        else:
            st.warning("⚠️ No se pudo extraer el código mejorado. Verifica el formato de la respuesta.")
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            st.download_button(
                label="📥 Descargar Análisis",
                data=analisis_text,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col_btn2:
            if codigo_mejorado:
                st.download_button(
                    label="💾 Descargar Código Mejorado",
                    data=codigo_mejorado,
                    file_name=f"improved_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                    mime="text/x-python",
                    use_container_width=True
                )
        
        with col_btn3:
            if codigo_mejorado:
                # Usar key única para evitar conflictos
                aplicar_btn = st.button("✨ Aplicar Sugerencias", type="primary", use_container_width=True, key="aplicar_sugerencias_btn")
        
        # Manejar click fuera del contenedor para evitar conflictos de DOM
        if codigo_mejorado and aplicar_btn:
            st.session_state['codigo_aplicado'] = codigo_mejorado
            st.session_state['mostrar_mensaje_aplicado'] = True
            # Mantener el análisis visible después de aplicar
            # st.rerun() se ejecuta automáticamente al cambiar session_state
            st.rerun()
        
        # Información adicional
        with st.expander("ℹ️ Información del Análisis"):
            st.json({
                "modelo_usado": data.get("modelo_usado", "N/A"),
                "usuario_id": data.get("usuario_id", "Anónimo"),
                "timestamp": data.get("timestamp", "N/A"),
                "codigo_mejorado_disponible": codigo_mejorado is not None
            })

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
                        
                        # Guardar en session_state para que persista después de rerun
                        st.session_state['ultimo_analisis'] = data
                        
                        # Guardar en historial de análisis para estadísticas
                        if 'historial_analisis' not in st.session_state:
                            st.session_state['historial_analisis'] = []
                        
                        # Extraer score del análisis (si está disponible)
                        analisis_text = data.get("analisis", "")
                        score = None
                        import re
                        score_match = re.search(r'Score de Calidad:\s*(\d+)/100', analisis_text)
                        if score_match:
                            score = int(score_match.group(1))
                        
                        # Agregar al historial
                        st.session_state['historial_analisis'].append({
                            "timestamp": data.get("timestamp"),
                            "codigo": codigo_input[:100] + "..." if len(codigo_input) > 100 else codigo_input,
                            "score": score,
                            "modelo": data.get("modelo_usado"),
                            "analisis_completo": analisis_text
                        })
                        
                        # Mostrar resultados
                        st.success("✅ Análisis completado!")
                        
                        # Timestamp
                        st.caption(f"🕐 {data.get('timestamp', 'N/A')}")
                        
                        # Análisis en markdown
                        analisis_text = data.get("analisis", "No se recibió análisis")
                        
                        # Extraer código mejorado del análisis
                        codigo_mejorado = None
                        import re
                        
                        # Intentar múltiples patrones para extraer el código
                        if "Código Mejorado" in analisis_text or "Codigo Mejorado" in analisis_text:
                            patterns = [
                                r'##\s*✨\s*Código Mejorado.*?```python\s*(.*?)\s*```',
                                r'✨\s*Código Mejorado.*?```python\s*(.*?)\s*```',
                                r'Código Mejorado.*?```python\s*(.*?)\s*```',
                                r'##\s*✨\s*Codigo Mejorado.*?```python\s*(.*?)\s*```',
                                r'✨\s*Codigo Mejorado.*?```python\s*(.*?)\s*```',
                                r'Codigo Mejorado.*?```python\s*(.*?)\s*```',
                                # Sin especificador python
                                r'Código Mejorado.*?```\s*(def .*?)\s*```',
                                r'Codigo Mejorado.*?```\s*(def .*?)\s*```',
                            ]
                            
                            for pattern in patterns:
                                match = re.search(pattern, analisis_text, re.DOTALL | re.IGNORECASE)
                                if match:
                                    codigo_mejorado = match.group(1).strip()
                                    # Limpiar comentarios iniciales si existen
                                    if codigo_mejorado.startswith('#'):
                                        lines = codigo_mejorado.split('\n')
                                        # Encontrar la primera línea que no es comentario
                                        for i, line in enumerate(lines):
                                            if line.strip() and not line.strip().startswith('#'):
                                                codigo_mejorado = '\n'.join(lines[i:])
                                                break
                                    break
                        
                        # Eliminar la sección de código mejorado del análisis para evitar duplicación
                        if codigo_mejorado:
                            # Eliminar completamente la sección de código mejorado del texto de análisis
                            # Patrón principal: desde "✨" seguido de cualquier variación de "Código Mejorado" hasta "📝 Cambios"
                            analisis_sin_codigo = re.sub(
                                r'#+?\s*✨\s*[CcóÓ].*?(?=📝)',
                                '',
                                analisis_text,
                                flags=re.MULTILINE | re.DOTALL
                            )
                            
                            # Limpiar cualquier línea que solo contenga emoji ✨ con o sin letra
                            analisis_sin_codigo = re.sub(r'\n?\s*✨\s*[A-Za-z]?\s*\n?', '\n', analisis_sin_codigo)
                            
                            # Limpiar líneas vacías múltiples
                            analisis_sin_codigo = re.sub(r'\n{3,}', '\n\n', analisis_sin_codigo)
                            analisis_sin_codigo = re.sub(r'\s+$', '', analisis_sin_codigo, flags=re.MULTILINE)
                            st.markdown(analisis_sin_codigo.strip())
                        else:
                            st.markdown(analisis_text)
                        
                        # Mostrar código mejorado en bloque copiable
                        if codigo_mejorado:
                            st.markdown("---")
                            st.markdown("### 💻 Versión Optimizada del Código")
                            st.info("💡 **Consejos de uso:**\n- Copia el código usando el icono 📋 (arriba a la derecha)\n- O aplica directamente con el botón '✨ Aplicar Sugerencias' (más abajo)")
                            st.code(codigo_mejorado, language="python", line_numbers=True)
                            st.success(f"✅ Código optimizado listo ({len(codigo_mejorado)} caracteres)")
                        else:
                            st.warning("⚠️ No se pudo extraer el código mejorado. Verifica el formato de la respuesta.")
                        
                        # Botones de acción
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        
                        with col_btn1:
                            st.download_button(
                                label="📥 Descargar Análisis",
                                data=analisis_text,
                                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                        
                        with col_btn2:
                            if codigo_mejorado:
                                st.download_button(
                                    label="💾 Descargar Código Mejorado",
                                    data=codigo_mejorado,
                                    file_name=f"improved_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                                    mime="text/x-python",
                                    use_container_width=True
                                )
                        
                        with col_btn3:
                            if codigo_mejorado:
                                # Usar key única diferente para este botón
                                aplicar_btn_nuevo = st.button("✨ Aplicar Sugerencias", type="primary", use_container_width=True, key="aplicar_sugerencias_nuevo_btn")
                        
                        # Manejar click fuera del contenedor para evitar conflictos de DOM
                        if codigo_mejorado and aplicar_btn_nuevo:
                            st.session_state['codigo_aplicado'] = codigo_mejorado
                            st.session_state['mostrar_mensaje_aplicado'] = True
                            st.rerun()
                        
                        # Información adicional
                        with st.expander("ℹ️ Información del Análisis"):
                            st.json({
                                "modelo_usado": data.get("modelo_usado", "N/A"),
                                "usuario_id": data.get("usuario_id", "Anónimo"),
                                "timestamp": data.get("timestamp", "N/A"),
                                "codigo_mejorado_disponible": codigo_mejorado is not None
                            })
                        
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
