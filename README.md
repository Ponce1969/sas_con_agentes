# 🧠 Neural Code Analyzer

**Plataforma SaaS de análisis de código Python con IA**

> Gemini 2.5 Flash · FastAPI · Streamlit · PostgreSQL

---

## 🚀 Quick Start

```bash
git clone https://github.com/Ponce1969/sas_con_agentes.git
cd project_saas
cp .env.example .env   # Configurar GEMINI_API_KEY
docker compose up -d
```

- **App:** http://localhost:8502
- **API:** http://localhost:8001/docs

---

## ✨ Features

| Core | Dashboard | Seguridad |
|------|-----------|-----------|
| 🐛 Detección de bugs | 📊 Estadísticas | 🔐 JWT Auth |
| 👃 Code smells | 🏆 Logros/Gamificación | 🔒 API keys encriptadas |
| ⚡ Optimizaciones | 💡 Insights automáticos | 📏 Límite 800 líneas |
| 📊 Score 0-100 | 📥 Exportar CSV | 🛡️ Rate limiting |

---

## 🏗️ Arquitectura

```
project_saas/
├── backend/app/
│   ├── core/              # Config, seguridad
│   ├── domain/            # Modelos SQLAlchemy
│   ├── application/       # Servicios (análisis, auth)
│   ├── infrastructure/    # Gemini client, encriptación
│   └── web/routers/       # API endpoints
├── frontend/app/
│   ├── main.py            # Analizador principal
│   └── pages/             # Dashboard, login
├── deploy/                # Scripts OrangePi + Cloudflare
└── docker-compose.yml
```

---

## 🛠️ Stack

| Capa | Tecnología |
|------|------------|
| Backend | FastAPI + Python 3.12 |
| Frontend | Streamlit |
| IA | Gemini 2.5 Flash |
| DB | PostgreSQL + Redis |
| Auth | JWT + Argon2 |
| Encriptación | Fernet (AES-128) |
| Deploy | Docker + Cloudflare Tunnel |

---

## 📋 Comandos

```bash
docker compose up -d      # Iniciar
docker compose logs -f    # Ver logs
docker compose down       # Detener
```

---

## 🚀 Deploy (OrangePi/Self-hosted)

```bash
sudo bash deploy/setup-orangepi.sh
```

Ver [deploy/DEPLOY_ORANGEPI.md](deploy/DEPLOY_ORANGEPI.md)

---

## 📋 Estado del Proyecto

**90% listo para producción**

| ✅ Implementado | 🚧 Pendiente |
|----------------|--------------|
| Análisis con Gemini 2.5 | Sistema de planes (free/pro) |
| Auth JWT + Argon2 | Panel administrativo |
| Dashboard + Gamificación | Rate limiting con Redis |
| Encriptación API keys | Logs estructurados |
| Deploy OrangePi/Cloudflare | CI/CD GitHub Actions |

---

## 📝 Licencia

MIT · **Neural SaaS Platform**
