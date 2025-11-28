# backend/app/main.py

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import setup_logging
from app.infrastructure.database import AsyncSessionLocal, create_default_roles, init_db
from app.web.routers import analysis_router, auth_router, embeddings_router, health_router

# Inicializar logging
setup_logging()
logger = logging.getLogger(__name__)

# Crear la app FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health_router.router)
app.include_router(auth_router.router)  # Nuevo: Auth
app.include_router(analysis_router.router)
app.include_router(embeddings_router.router)


# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """Inicializar base de datos y roles al arrancar."""
    logger.info(f"🚀 Iniciando {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}...")

    # Inicializar DB
    try:
        await init_db()

        # Crear roles por defecto
        async with AsyncSessionLocal() as session:
            await create_default_roles(session)

        logger.info("✅ Base de datos lista")
    except Exception as e:
        logger.warning(f"⚠️ No se pudo conectar a PostgreSQL: {e}")
        logger.info("💡 Continuando sin DB (modo desarrollo)")

    logger.info(f"✅ {settings.PROJECT_NAME} iniciado correctamente")


# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"🛑 {settings.PROJECT_NAME} detenido")


# Ejecutar localmente con uvicorn si se llama como script
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)

