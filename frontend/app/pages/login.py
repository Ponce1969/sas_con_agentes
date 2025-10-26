"""
Página de Login - Autenticación de usuarios (placeholder para MVP).
"""

import streamlit as st
import os
import time

# Configuración
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")

st.set_page_config(
    page_title="Login - Neural Code Analyzer",
    page_icon="🔐",
    layout="centered"
)

# Centrar contenido
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Logo y título
    st.title("🧠 Neural Code Analyzer")
    st.markdown("### Iniciar Sesión")
    st.markdown("---")
    
    # Formulario de login
    with st.form("login_form"):
        email = st.text_input(
            "📧 Email",
            placeholder="tu@email.com",
            help="Ingresa tu email registrado"
        )
        
        password = st.text_input(
            "🔒 Contraseña",
            type="password",
            placeholder="••••••••",
            help="Ingresa tu contraseña"
        )
        
        remember_me = st.checkbox("Recordarme")
        
        submit_button = st.form_submit_button(
            "🚀 Iniciar Sesión",
            use_container_width=True,
            type="primary"
        )
        
        if submit_button:
            if not email or not password:
                st.error("⚠️ Por favor completa todos los campos")
            else:
                # TODO: Implementar autenticación real con JWT
                st.success("✅ Login exitoso! (placeholder)")
                st.info("🔄 Redirigiendo al dashboard...")
                time.sleep(1)  # Pequeño delay para que el usuario vea el mensaje
                st.switch_page("pages/dashboard.py")
    
    st.markdown("---")
    
    # Enlaces adicionales
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("📝 Crear Cuenta", use_container_width=True):
            st.info("Funcionalidad de registro próximamente")
    
    with col_b:
        if st.button("🔑 Olvidé mi Contraseña", use_container_width=True):
            st.info("Funcionalidad de recuperación próximamente")
    
    st.markdown("---")
    
    # Modo demo
    st.markdown("### 🎯 Modo Demo")
    st.markdown("Prueba la aplicación sin registrarte")
    
    if st.button("🚀 Continuar sin Login", use_container_width=True, type="secondary"):
        st.info("Redirigiendo a la página principal...")
        time.sleep(0.5)  # Pequeño delay
        st.switch_page("main.py")
    
    st.markdown("---")
    
    # Información
    with st.expander("ℹ️ Información"):
        st.markdown("""
        **Neural Code Analyzer** es una plataforma SaaS que usa IA para:
        
        - 🐛 Detectar bugs potenciales
        - 👃 Identificar code smells
        - ⚡ Sugerir mejoras de rendimiento
        - 📊 Calcular score de calidad
        
        **Versión:** 0.1.0 MVP
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>Made with ❤️ by Neural SaaS Platform</div>",
    unsafe_allow_html=True
)

# Nota de desarrollo
st.warning("⚠️ **Nota:** La autenticación está en desarrollo. Por ahora usa el modo demo.")

