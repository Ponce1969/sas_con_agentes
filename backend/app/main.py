# backend/app/main.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import setup_logging
from app.web.routers import embeddings_router, health_router

# Inicializar logging
setup_logging()

# Crear la app FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir routers
app.include_router(health_router.router)
app.include_router(embeddings_router.router)

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    print(f"✅ {settings.PROJECT_NAME} v{settings.PROJECT_VERSION} iniciado correctamente.")

# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    print(f"🛑 {settings.PROJECT_NAME} detenido.")

# Ejecutar localmente con uvicorn si se llama como script
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )

