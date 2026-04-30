# RAG Platform

Plataforma API-first de Question & Answering sobre documentos técnicos. El usuario sube PDFs y puede hacerles preguntas en lenguaje natural. El sistema responde citando las fuentes exactas, anclado en los documentos reales.

> **Estado actual:** Fase 1 completada — base operativa, seguridad y CI. La ingestión de documentos y el pipeline RAG corresponden a la Fase 2 en adelante.

---

## Stack

| Tecnología | Uso |
|---|---|
| Python 3.12 | Runtime del backend |
| FastAPI | Framework HTTP |
| Uvicorn | Servidor ASGI |
| Pydantic Settings | Variables de entorno tipadas |
| SQLAlchemy | ORM y acceso a base de datos |
| Alembic | Migraciones de esquema |
| SlowAPI | Rate limiting |
| Structlog | Logging estructurado JSON |
| PostgreSQL 16 | Base de datos relacional (Docker) |
| SQLite | Base de datos local por defecto (sin Docker) |
| Qdrant | Base de datos vectorial (preparada para Fase 2) |
| Pytest | Tests |
| Ruff | Linter |
| GitHub Actions | CI bloqueante |

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- Python 3.12+ (solo si querés correr sin Docker)
- Git

---

## Setup local

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd RagProject
```

### 2. Crear el archivo de entorno

```bash
# Linux / macOS
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Abrí `.env` y completá las variables necesarias. Para desarrollo local las únicas obligatorias son `POSTGRES_PASSWORD` y opcionalmente `OPENAI_API_KEY` (requerida en Fase 2).

### 3. Levantar con Docker Compose

```bash
docker compose up --build
```

Esto levanta tres servicios:
- `rag_backend` en `http://localhost:8000`
- `rag_postgres` (PostgreSQL 16) en `localhost:5432`
- `rag_qdrant` en `http://localhost:6333`

### 4. Verificar que está funcionando

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{"status": "ok"}
```

---

## Correr sin Docker (backend solo)

```bash
cd backend
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

En este modo el backend usa SQLite local (`rag_platform.db`) por defecto, sin necesidad de PostgreSQL.

---

## Variables de entorno

El archivo `.env.example` define todas las variables necesarias:

| Variable | Descripción | Default |
|---|---|---|
| `ENVIRONMENT` | Entorno de ejecución | `dev` |
| `DEBUG` | Modo debug | `true` |
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///./rag_platform.db` |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos por CORS | `localhost:5173, localhost:3000` |
| `DEFAULT_RATE_LIMIT` | Límite de requests por IP | `60/minute` |
| `POSTGRES_DB` | Nombre de la base PostgreSQL | `rag_platform` |
| `POSTGRES_USER` | Usuario de PostgreSQL | `rag_user` |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL | *(obligatorio completar)* |
| `OPENAI_API_KEY` | API key de OpenAI | *(requerida desde Fase 2)* |
| `QDRANT_URL` | URL de Qdrant | `http://localhost:6333` |
| `QDRANT_API_KEY` | API key de Qdrant | *(opcional en dev)* |

---

## Endpoints disponibles (Fase 1)

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/health` | No | Estado del servidor |
| `GET` | `/me` | Bearer token | Datos del usuario autenticado |
| `GET` | `/docs` | No | Documentación interactiva (Swagger) |

### Autenticación

Los endpoints protegidos requieren API key en el header:

```
Authorization: Bearer <tu_api_key>
```

Las API keys se almacenan hasheadas (SHA-256) en la base de datos. Nunca en texto plano.

---

## Tests

```bash
cd backend
python -m pytest -v
```

Suite de tests de Fase 1:

| Archivo | Qué valida |
|---|---|
| `test_health.py` | Endpoint público `/health` |
| `test_config.py` | Defaults y caché de settings |
| `test_models.py` | Mapping ORM de tablas |
| `test_auth_api_key.py` | Hash y generación de API keys |
| `test_auth_http.py` | Auth HTTP en `/me` (válida / inválida / sin header) |
| `test_middleware.py` | CORS y rate limiting |

---

## Migraciones de base de datos

```bash
cd backend

# Aplicar migraciones pendientes
alembic upgrade head

# Generar nueva migración tras cambiar models.py
alembic revision --autogenerate -m "descripcion del cambio"
```

---

## CI

El pipeline de GitHub Actions corre en cada push o PR a `main`:

1. Instala Python 3.12 y dependencias del backend
2. Ejecuta `ruff check .` — si falla, el pipeline se detiene
3. Ejecuta `pytest` — si algún test falla, bloquea la integración

---

## Estructura del proyecto

```
RagProject/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py          # get_current_user — autenticación reutilizable
│   │   │   ├── middleware.py    # CORS y rate limiting
│   │   │   └── routes/
│   │   │       └── health.py    # GET /health
│   │   ├── auth/
│   │   │   ├── hashing.py       # SHA-256 de API keys
│   │   │   └── api_key.py       # Generación y validación de keys
│   │   ├── core/
│   │   │   ├── config.py        # Settings tipados con pydantic-settings
│   │   │   ├── exceptions.py    # Handlers globales de error
│   │   │   └── logging.py       # Structlog JSON
│   │   ├── db/
│   │   │   ├── database.py      # Engine SQLAlchemy y sesión
│   │   │   ├── models.py        # User, ApiKey, UsageLog
│   │   │   └── migrations/      # Alembic
│   │   └── main.py              # Bootstrap de la app FastAPI
│   ├── tests/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── alembic.ini
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── .env.example
└── .gitignore
```

---

## Roadmap

| Fase | Descripción | Estado |
|---|---|---|
| **1 — Base + seguridad** | FastAPI, auth por API key, DB, CI | Completada |
| 2 — Ingestión async | Upload de PDFs, chunking, embeddings, Qdrant | Pendiente |
| 3 — Pipeline RAG | Query, retrieval, reranking, generación con citas | Pendiente |
| 4 — Observabilidad | LangFuse, RAGAS, feedback de usuario | Pendiente |
| 5 — Frontend | React, drag & drop, chat con citas | Pendiente |
| 6 — Deploy | Railway + Vercel + CI/CD automático | Pendiente |
