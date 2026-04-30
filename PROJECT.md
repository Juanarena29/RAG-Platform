# RAG Platform — Documentación del proyecto

## Índice

1. [Objetivo del proyecto](#1-objetivo-del-proyecto)
2. [Estructura de carpetas](#2-estructura-de-carpetas)
3. [Roadmap por fases](#3-roadmap-por-fases)
4. [Glosario técnico](#4-glosario-técnico)

---

## 1. Objetivo del proyecto

### ¿Qué es?

Una **plataforma API-first de Question & Answering sobre documentos técnicos**, construida con un pipeline RAG (Retrieval-Augmented Generation) production-grade.

El usuario sube documentos (PDFs de papers de ML/AI, documentación técnica) y puede hacerles preguntas en lenguaje natural. El sistema responde citando las fuentes exactas de donde extrajo la información — anclado en los documentos reales, sin alucinaciones.

### ¿Para qué sirve?

- Subir papers de arXiv o documentación técnica y consultarlos en lenguaje natural
- Demostrar un stack de AI Engineering completo en producción
- Base escalable hacia un SaaS multi-tenant en el futuro

### ¿Quién puede usarlo?

**Versión actual:** uso propio únicamente. La autenticación está diseñada desde el inicio como multi-usuario (tabla `api_keys` en DB), pero hoy solo existe un usuario: vos. Escalar a múltiples usuarios es agregar registro, no reescribir la arquitectura.

### ¿Qué demuestra como portfolio?

- Diseño de arquitectura event-driven con workflows durables (Inngest)
- Pipeline RAG con técnicas avanzadas de industria (HyDE, Hybrid Search, Reranking)
- API REST production-grade con autenticación, rate limiting y aislamiento multi-tenant
- Observabilidad real con trazas, costos y métricas de calidad (LangFuse + RAGAS)
- CI/CD con deploy automático en producción (Railway + Vercel + GitHub Actions)

---

## 2. Estructura de carpetas

```
rag-platform/
│
├── backend/                        # Python · FastAPI
│   ├── app/
│   │   ├── api/                    # Capa HTTP — solo recibe y delega
│   │   │   ├── deps.py             # get_current_user: valida API key en cada request
│   │   │   ├── middleware.py       # Rate limiting, CORS, logging de requests
│   │   │   └── routes/
│   │   │       ├── health.py       # GET /health — sin auth, para Railway y monitoreo
│   │   │       ├── documents.py    # POST /documents/upload, GET /documents
│   │   │       ├── query.py        # POST /query — ejecuta el pipeline RAG
│   │   │       └── feedback.py     # POST /feedback — thumbs up/down hacia LangFuse
│   │   │
│   │   ├── auth/                   # Seguridad — módulo propio
│   │   │   ├── hashing.py          # SHA-256 de API keys, nunca texto plano en DB
│   │   │   └── api_key.py          # Genera key segura, valida contra DB
│   │   │
│   │   ├── core/                   # Configuración global
│   │   │   ├── config.py           # pydantic-settings: todas las env vars tipadas
│   │   │   ├── exceptions.py       # Handlers globales: 401, 422, 429, 500
│   │   │   └── logging.py          # structlog: logs estructurados en JSON
│   │   │
│   │   ├── db/                     # Persistencia relacional
│   │   │   ├── database.py         # SQLAlchemy engine — SQLite dev / PostgreSQL prod
│   │   │   ├── models.py           # User, ApiKey, Document, UsageLog
│   │   │   ├── repositories.py     # Queries a DB, nunca SQL crudo en rutas
│   │   │   └── migrations/         # Alembic — versionado de esquema
│   │   │
│   │   ├── ingestion/              # Flujo async de documentos
│   │   │   ├── validator.py        # Magic bytes PDF, tamaño máx, content-type
│   │   │   ├── parser.py           # Extrae texto limpio con pymupdf
│   │   │   ├── chunker.py          # Chunking semántico por coherencia
│   │   │   ├── embedder.py         # OpenAI text-embedding-3-small
│   │   │   └── inngest_functions.py # Workflow: validate→parse→chunk→embed→store
│   │   │
│   │   ├── rag/                    # Pipeline de consulta
│   │   │   ├── query_transformer.py # Reescribe query para mejor retrieval
│   │   │   ├── hyde.py             # Genera doc hipotético para embedear
│   │   │   ├── retriever.py        # Hybrid search en Qdrant (dense + BM25)
│   │   │   ├── reranker.py         # Cross-encoder o Cohere Rerank
│   │   │   ├── generator.py        # Prompt + contexto + citas → LLM
│   │   │   └── pipeline.py         # Orquesta los 5 pasos, instrumentado con LangFuse
│   │   │
│   │   ├── schemas/                # Contratos de datos (Pydantic)
│   │   │   ├── documents.py        # UploadResponse, DocumentList
│   │   │   └── query.py            # QueryRequest, QueryResponse, Source
│   │   │
│   │   └── main.py                 # FastAPI init, routers, Inngest serve, lifespan
│   │
│   ├── tests/
│   │   ├── conftest.py             # Fixtures: test client, DB en memoria, user de prueba
│   │   ├── test_auth/              # Key válida, inválida, expirada
│   │   ├── test_ingestion/         # PDF válido, inválido, oversized
│   │   ├── test_rag/               # Pipeline end-to-end con mocks
│   │   ├── test_api/               # Endpoints, rate limiting, aislamiento multi-tenant
│   │   └── eval_ragas.py           # Métricas de calidad RAG sobre dataset real
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/                       # React · Vite
│   └── src/
│       ├── components/
│       │   ├── UploadPanel.jsx     # Drag & drop, barra de progreso async
│       │   ├── ChatPanel.jsx       # Input + respuesta con citas coloreadas
│       │   ├── SourceCard.jsx      # Fragmento del doc fuente expandible
│       │   └── FeedbackButtons.jsx # Thumbs up/down por respuesta
│       ├── pages/
│       │   └── App.jsx             # Workspace principal
│       ├── api.js                  # Cliente HTTP — inyecta API key desde env
│       └── config.js               # VITE_API_URL, VITE_API_KEY desde .env
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # Lint → test → deploy on push to main
│
├── docker-compose.yml              # Dev local: FastAPI + Qdrant + PostgreSQL + Inngest
├── railway.toml                    # Config de deploy en producción
├── .env.example                    # Nombres de variables, nunca valores reales
├── .gitignore                      # .env, __pycache__, node_modules, *.db
└── README.md                       # Arquitectura, demo link, métricas RAGAS
```

### Principio de diseño

Cada carpeta tiene **una sola responsabilidad**. `ingestion/` no sabe nada del pipeline RAG. `rag/` no sabe cómo llegó el documento. `api/` solo recibe requests y delega. Eso hace que el proyecto sea legible, testeable y modificable sin efectos secundarios.

---

## 3. Roadmap por fases

> Las semanas son orientativas. El orden es estricto: no avanzar a la siguiente fase hasta que la actual tenga tests pasando.

---

### Fase 1 — Base + seguridad desde el día 1 *(semana 1)*

**Output:** repo funcionando, FastAPI con `/health`, DB con auth, CI verde.

La seguridad se construye antes que cualquier lógica de negocio. Si lo hacés al revés, terminás parchando.

- [ ] Monorepo, `.env.example`, `.gitignore`, `docker-compose` con Qdrant + PostgreSQL local
- [ ] `config.py` con pydantic-settings — todas las env vars tipadas y validadas al arrancar
- [ ] `db/models.py`: tablas `User`, `ApiKey` (hash, no plaintext), `UsageLog`
- [ ] `auth/hashing.py` + `auth/api_key.py`: generación y validación de keys hasheadas
- [ ] `api/deps.py`: dependency `get_current_user` — protege todos los endpoints desde el inicio
- [ ] `middleware.py`: CORS solo para localhost en dev, rate limiting base con slowapi
- [ ] Alembic configurado, primera migración corriendo
- [ ] `GET /health` sin auth funcionando
- [ ] Tests de auth: key válida → 200, inválida → 401, sin header → 401
- [ ] GitHub Actions: ruff + pytest en cada push

---

### Fase 2 — Pipeline de ingestión async *(semana 2)*

**Output:** subir un PDF por API → procesado en background → vectores en Qdrant.

- [ ] `validator.py`: magic bytes, content-type, tamaño máximo (20MB)
- [ ] `parser.py`: texto limpio desde PDF con pymupdf
- [ ] `chunker.py`: chunking semántico por coherencia, no por tokens fijos
- [ ] `embedder.py`: `text-embedding-3-small` de OpenAI con manejo de rate limits
- [ ] `inngest_functions.py`: workflow con 5 steps, retry automático por step
- [ ] Colección en Qdrant nombrada `user_{id}` — nunca el cliente elige la colección
- [ ] `POST /documents/upload` — dispara Inngest, responde 202, registra en UsageLog
- [ ] Tests: PDF válido, inválido, oversized, aislamiento entre usuarios

---

### Fase 3 — Pipeline RAG completo *(semana 3)*

**Output:** hacer una pregunta por API → respuesta con citas de los documentos subidos.

- [ ] `query_transformer.py`: reescribe la query para mejorar recall
- [ ] `hyde.py`: genera documento hipotético, lo embeds, lo usa como query vector
- [ ] `retriever.py`: hybrid search en Qdrant — dense + BM25, filtrado por `user_id`
- [ ] `reranker.py`: cross-encoder local o Cohere Rerank API
- [ ] `generator.py`: prompt estructurado con contexto + instrucción de citar fuentes
- [ ] `pipeline.py`: orquesta los 5 pasos, input sanitizado antes de entrar
- [ ] `POST /query` — valida schema con Pydantic, ejecuta pipeline, devuelve respuesta + fuentes
- [ ] Tests del pipeline con mocks de OpenAI y Qdrant

---

### Fase 4 — Observabilidad y evaluación *(semana 4)*

**Output:** LangFuse dashboard con trazas reales, métricas RAGAS documentadas.

- [ ] LangFuse SDK en cada step del pipeline: latencia, tokens, costo estimado por query
- [ ] Traza completa por request: desde `/query` hasta respuesta generada
- [ ] structlog: logs en JSON con user_id, request_id, duración — sin loguear keys ni datos sensibles
- [ ] `POST /feedback`: thumbs up/down registrado en LangFuse y en UsageLog
- [ ] `eval_ragas.py`: dataset de 20-30 pares pregunta/respuesta sobre papers reales de arXiv
- [ ] Métricas baseline documentadas en README: faithfulness, answer relevancy, context precision

---

### Fase 5 — Frontend *(semana 5)*

**Output:** UI funcional conectada al backend, pensada para el video demo.

- [ ] API key del frontend en `VITE_API_KEY` — nunca en el código fuente
- [ ] `UploadPanel`: drag & drop, estado del workflow Inngest (procesando / listo / error)
- [ ] `ChatPanel`: input de query, respuesta con fragmentos de fuente coloreados y expandibles
- [ ] `FeedbackButtons`: thumbs up/down visible por cada respuesta
- [ ] Flujo completo filmable: subir PDF → esperar procesamiento → preguntar → ver respuesta con citas

---

### Fase 6 — Deploy + video demo *(semana 6)*

**Output:** app en producción con URL real, video demostrando el stack completo.

- [ ] Backend en Railway: env vars en el panel, nunca en el repo
- [ ] CORS actualizado a dominio de Vercel solamente — cerrar localhost en prod
- [ ] Frontend en Vercel: `VITE_API_URL` apuntando al backend de Railway
- [ ] GitHub Actions: deploy automático a Railway en push a `main`
- [ ] README final: arquitectura, métricas RAGAS, link al demo, instrucciones para correrlo local
- [ ] Video demo: upload → ingestión → query → citas → LangFuse dashboard con trazas

---

## 4. Glosario técnico

Todo lo que se usa en el proyecto, explicado desde cero.

---

### FastAPI

Framework web de Python para construir APIs REST. Es el punto de entrada de toda la aplicación — recibe las requests HTTP, las valida, y las delega a los módulos correspondientes.

Lo que lo diferencia de otros frameworks: usa **type hints** de Python para validar automáticamente los datos de entrada y salida, y genera documentación interactiva (`/docs`) sin configuración extra.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

### Pydantic

Librería de validación de datos. Define la "forma" que deben tener los datos que entran y salen de la API. Si algo no cumple el schema, FastAPI rechaza la request automáticamente con un error claro.

```python
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    max_results: int = 5  # valor por defecto

# Si el cliente manda max_results: "hola" → error 422 automático
```

**pydantic-settings** es la extensión que lee variables de entorno con el mismo mecanismo. Define el schema de tu `.env` y falla al arrancar si falta alguna variable obligatoria.

---

### SQLAlchemy

ORM (Object-Relational Mapper) de Python. Permite interactuar con la base de datos usando clases Python en lugar de SQL crudo.

```python
class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

En desarrollo se usa **SQLite** (un archivo `.db`, sin servidor). En producción se swapea por **PostgreSQL** cambiando solo una variable de entorno — el código no cambia.

---

### Alembic

Sistema de migraciones para SQLAlchemy. Resuelve el problema de cómo evolucionar el esquema de la base de datos en producción sin borrar datos.

Cada vez que modificás un modelo, generás una migración:

```bash
# Detecta cambios en models.py y genera el script automáticamente
alembic revision --autogenerate -m "add is_active to users"

# Aplica todos los cambios pendientes
alembic upgrade head
```

Cada migración tiene `upgrade()` para aplicar y `downgrade()` para revertir. Alembic lleva un registro de qué migraciones ya se ejecutaron.

---

### Inngest

Motor de workflows durables. Resuelve el problema de procesar tareas pesadas en background sin perder trabajo si algo falla.

Cuando el usuario sube un PDF, FastAPI no procesa nada — dispara un **evento** a Inngest y responde `202 Accepted` de inmediato. Inngest ejecuta el workflow en background con reintentos automáticos por cada step:

```
POST /upload → evento disparado → 202 inmediato
                    ↓
         Inngest ejecuta en background:
         step 1: validar PDF         ← si falla, reintenta solo
         step 2: parsear texto       ← si falla, reintenta desde acá
         step 3: generar embeddings  ← si falla, reintenta desde acá
         step 4: guardar en Qdrant
```

Sin Inngest, si la llamada a OpenAI falla a mitad del procesamiento, se pierde todo y el usuario no sabe qué pasó.

---

### Qdrant

Base de datos vectorial. Almacena los embeddings (representaciones numéricas del texto) y permite hacer búsquedas por similaridad semántica.

En lugar de buscar por palabras exactas, busca por significado. "¿Cómo funciona la atención en transformers?" encuentra chunks que hablan de attention mechanism aunque no usen esas palabras exactas.

Cada usuario tiene su propia **colección** nombrada `user_{id}`. Esto garantiza que nunca se mezclan documentos entre usuarios.

---

### LangChain

Framework de orquestación para aplicaciones con LLMs. Provee abstracciones para conectar los distintos pasos del pipeline RAG: retrievers, prompts, modelos, parsers de output.

Se usa para armar la cadena: `query → retriever → reranker → prompt → LLM → respuesta`.

---

### LangFuse

Plataforma de observabilidad para aplicaciones LLM. Registra cada llamada al pipeline con:

- Latencia por step (¿cuánto tardó el retrieval vs la generación?)
- Tokens consumidos y costo estimado por query
- Scores de retrieval y reranking
- Feedback del usuario (thumbs up/down)
- Queries que fallaron o tuvieron baja confianza

Permite ver en un dashboard exactamente qué está pasando en producción, cuánto cuesta cada usuario, y dónde está fallando el sistema.

---

### RAGAS

Framework de evaluación específico para pipelines RAG. Mide la calidad del sistema con métricas concretas sobre un dataset de preguntas y respuestas esperadas:

| Métrica | Qué mide |
|---|---|
| `faithfulness` | ¿La respuesta está anclada en los documentos o el LLM inventó? |
| `answer_relevancy` | ¿Respondió lo que se preguntó? |
| `context_precision` | ¿Los chunks recuperados eran los correctos para responder? |
| `context_recall` | ¿Se recuperó toda la información necesaria? |

Tener estas métricas documentadas en el README es la diferencia entre "hice RAG" y "construí un sistema RAG con calidad medible".

---

### HyDE (Hypothetical Document Embeddings)

Técnica de mejora de retrieval. En lugar de buscar en el vector store con el embedding de la pregunta cruda, primero le pide al LLM que genere un documento hipotético que respondería la pregunta, y usa el embedding de ese documento para buscar.

El embedding de una respuesta hipotética es mucho más similar a los chunks relevantes que el embedding de la pregunta, porque está en el mismo "espacio semántico" que los documentos.

```
Pregunta:         "¿Cómo funciona la atención multi-cabeza?"
Doc hipotético:   "La atención multi-cabeza permite al modelo atender
                   simultáneamente a diferentes posiciones..."
                         ↓
                   Ese texto se embeds y se usa para buscar
```

---

### Hybrid Search

Combina dos tipos de búsqueda simultáneamente:

- **Dense search**: búsqueda semántica por embeddings. Encuentra documentos con significado similar aunque usen palabras diferentes.
- **Sparse search (BM25)**: búsqueda por palabras clave clásica. Encuentra documentos que contienen exactamente los términos buscados.

Los resultados se fusionan. Esto captura tanto la intención semántica como los términos técnicos específicos — crítico para documentación técnica donde los nombres exactos importan (ej: "GPT-4", "RLHF", "LoRA").

---

### Reranking

Paso posterior al retrieval. El retriever devuelve los top-K chunks más similares a la query. El reranker los reordena con un modelo más preciso (cross-encoder) que evalúa la relevancia de cada chunk en relación a la pregunta específica.

Es más costoso computacionalmente pero mucho más preciso. Se aplica sobre un conjunto pequeño (top 20) para no impactar la latencia.

---

### Ruff

Linter de Python. Lee el código sin ejecutarlo y detecta problemas: imports sin usar, variables asignadas pero nunca leídas, violaciones de estilo, bugs potenciales.

```bash
ruff check .
```

Es el más rápido del ecosistema — reemplaza a flake8, isort y pycodestyle juntos. Se corre como primer paso del CI para que código con problemas no llegue a los tests ni a producción.

---

### Pytest

Framework de testing de Python. Ejecuta las funciones de test y reporta qué pasó.

```python
def test_invalid_api_key_returns_401(client):
    response = client.get("/documents", headers={"Authorization": "Bearer wrong"})
    assert response.status_code == 401
```

En CI se corre después de ruff. Si algún test falla, el deploy no ocurre.

**conftest.py** es el archivo donde se definen los **fixtures** — funciones que crean el estado necesario para los tests (cliente HTTP de prueba, base de datos en memoria, usuario de prueba con API key válida).

---

### GitHub Actions

Sistema de CI/CD integrado en GitHub. Define workflows que se ejecutan automáticamente ante eventos (push, pull request, etc.).

El workflow del proyecto:

```yaml
on: push to main
jobs:
  ci:
    steps:
      - ruff check .          # lint
      - pytest                # tests
      - deploy to Railway     # solo si todo pasó
```

Si ruff o pytest fallan, Railway no recibe el deploy. Esto garantiza que `main` siempre está en estado deployable.

---

### Railway

Plataforma de deploy para aplicaciones backend. Conecta con el repo de GitHub, detecta el `Dockerfile`, y deploya automáticamente. Incluye dominio gratis, PostgreSQL managed, y variables de entorno seguras.

Las API keys y secrets se cargan en el panel de Railway — nunca en el código ni en el repo.

---

### Vercel

Plataforma de deploy para frontends estáticos (React, Next.js, etc.). Free tier permanente, dominio gratis, deploy automático desde GitHub.

El frontend lee la URL del backend desde `VITE_API_URL` — variable de entorno configurada en el panel de Vercel, no hardcodeada.

---

### structlog

Librería de logging para Python que produce logs en formato JSON estructurado. En lugar de strings libres, cada log es un objeto con campos definidos:

```json
{
  "event": "query_completed",
  "user_id": "usr_abc123",
  "request_id": "req_xyz789",
  "duration_ms": 842,
  "tokens_used": 1240
}
```

Esto permite filtrar y analizar logs en producción. Nunca se loguean API keys, passwords ni datos sensibles.

---

### slowapi

Wrapper de rate limiting para FastAPI. Limita cuántas requests puede hacer un usuario en un período de tiempo. Sin esto, cualquier abuso de la API genera costos en OpenAI.

```python
# Máximo 60 queries por hora por usuario
@limiter.limit("60/hour")
@app.post("/query")
def query(request: Request, ...):
    ...
```

---

### Docker / docker-compose

Docker empaqueta la aplicación y todas sus dependencias en un contenedor — un entorno reproducible que funciona igual en cualquier máquina.

docker-compose define múltiples contenedores que trabajan juntos. En desarrollo local levanta con un solo comando:

```bash
docker-compose up
# Levanta: FastAPI + PostgreSQL + Qdrant + Inngest dev server
```

---

### Variables de entorno (.env)

Mecanismo para separar la configuración del código. Keys de APIs, URLs de bases de datos, secrets — nunca van en el código fuente.

`.env` (nunca se commitea al repo) contiene los valores reales:
```
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
```

`.env.example` (sí se commitea) contiene los nombres sin valores:
```
OPENAI_API_KEY=
QDRANT_URL=
```

Así cualquiera que clone el repo sabe qué variables necesita configurar.

---

### API Key (autenticación)

Cadena única y secreta que identifica a un usuario. Se manda en el header de cada request:

```
Authorization: Bearer rag_abc123xyz789...
```

**Nunca se guarda en texto plano en la base de datos.** Se guarda el hash (SHA-256), igual que las contraseñas. Cuando llega una request, se hashea la key recibida y se compara contra el hash guardado.

---

### Aislamiento multi-tenant

Garantía de que un usuario nunca puede ver ni consultar datos de otro usuario. Se implementa en dos capas:

1. La colección de Qdrant se nombra `user_{id}` — derivado del token, nunca del input del cliente
2. Cada query al retriever incluye un filtro por `user_id` — aunque alguien manipule la request, solo puede ver sus propios documentos

---

*Documento generado como referencia para el desarrollo en Cursor. Actualizar métricas RAGAS y link al demo una vez deployado.*
