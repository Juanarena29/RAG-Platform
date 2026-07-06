# RAG Platform

Demo de **AI Engineering** sobre documentos técnicos (PDFs): subís papers, hacés preguntas en lenguaje natural y el sistema responde **citando fuentes**, con trazas en LangFuse y evaluación cuantitativa con RAGAS.

Pensado para clonar, pegar tus API keys en `.env` y experimentar localmente.

---

## Qué demuestra este proyecto

No es un template de infraestructura. El foco está en el **ciclo completo de un sistema RAG en desarrollo**:

1. **Ingestión** — PDF → chunks → embeddings → Qdrant  
2. **Retrieval avanzado** — query transformation, HyDE, hybrid search (dense + BM25)  
3. **Reranking** — cross-encoder local (o Cohere opcional)  
4. **Generación** — respuesta anclada en contexto con citas  
5. **Observabilidad** — traza por step en LangFuse (latencia, tokens, costo)  
6. **Evaluación** — métricas RAGAS sobre un dataset fijo de 25 preguntas  

---

## Pipeline RAG

Cada `POST /query` ejecuta esta secuencia (instrumentada en LangFuse):

```
Pregunta del usuario
    ↓
query_transformer   →  reescribe la query para mejor retrieval
    ↓
hyde                →  genera doc hipotético y lo embeds (opcional, default ON)
    ↓
retriever           →  hybrid search en Qdrant (colección user_{id})
    ↓
reranker            →  reordena top-K chunks por relevancia
    ↓
generator           →  LLM con contexto + instrucción de citar fuentes
    ↓
Respuesta + sources + trace_id
```

La ingestión corre en background (`asyncio.create_task`): upload → `202 Accepted` → procesamiento → estado `completed` / `failed` en DB.

---

## Observabilidad (LangFuse)

Con `LANGFUSE_ENABLED=true`, cada query genera una traza `rag_query`:

```
rag_query
├── query_transformer
├── hyde
├── retriever
├── reranker
└── generator
```

El `trace_id` de la respuesta conecta con `POST /feedback` (thumbs up/down → score `user_feedback` en LangFuse).

Variables:

| Variable | Descripción |
|---|---|
| `LANGFUSE_ENABLED` | `true` para activar trazas |
| `LANGFUSE_PUBLIC_KEY` | Public key del dashboard |
| `LANGFUSE_SECRET_KEY` | Secret key del dashboard |
| `LANGFUSE_HOST` | Default: `https://cloud.langfuse.com` |

---

# Evaluación (RAGAS)

Dataset fijo de **25 pares pregunta/respuesta** sobre papers de ML/AI (transformers, attention, RAG, HyDE, long-context). Script: `backend/tests/eval_ragas.py`.

### Scores de referencia (Part B v2, config `full`, n=3, generator temp=0.0)

| Métrica | Qué mide | Score (mean ± std) |
|---|---|---:|
| `faithfulness` | ¿La respuesta está anclada en el contexto? | **0.860 ± 0.005** |
| `answer_relevancy` | ¿Respondió lo que se preguntó? | **0.914 ± 0.006** |
| `context_precision` | ¿Los chunks recuperados eran relevantes? | **0.979 ± 0.001** |
| `context_recall` | ¿Se recuperó la info necesaria? | **1.000 ± 0.000** |

Detalle completo, ablation 2×2 y revisiones v1→v2: [`EXPERIMENT_HISTORY_INDEX.md`](EXPERIMENT_HISTORY_INDEX.md).

Artefactos crudos: `backend/tests/eval_results/TestsB_v2/` (JSON + Markdown por run).

### Prerrequisitos para correr eval

RAGAS evalúa contra el endpoint live `POST /query`. **No incluye PDFs en el repo** — tenés que ingestarlos primero:

1. Backend + Qdrant corriendo.
2. API key creada con `python create_user.py`.
3. Subir vía UI o API los PDFs del corpus de eval (mismos papers que alimentan las 25 preguntas), por ejemplo:
   - Paper de transformers / attention (ej. *Attention Is All You Need*)
   - Paper de RAG
   - Paper de HyDE
   - *Lost in the Middle*
   - GPT-3 / long-context (opcional según cobertura de preguntas)
4. Esperar que todos queden en estado `completed` (`GET /documents`).
5. Subir `QUERY_RATE_LIMIT` en `.env` (ej. `500/hour`) si vas a correr batches — cada eval hace 25 queries.

### Variables de evaluación

| Variable | Descripción | Default |
|---|---|---|
| `EVAL_API_KEY` | API key del usuario con corpus ingestado | — (requerida) |
| `BASE_URL` | URL del backend | `http://localhost:8000` |
| `EVAL_EXPERIMENT_ID` | ID del run (lowercase, `_` ok) | timestamp auto |
| `EVAL_USE_QUERY_TRANSFORM` | `true` / `false` | `true` |
| `EVAL_USE_HYDE` | `true` / `false` | `true` |
| `EVAL_OUTPUT_DIR` | Carpeta de salida relativa a `backend/tests/` | `eval_results/` |
| `EVAL_QUERY_DELAY_SECONDS` | Pausa entre queries (evita 429) | `1` |

También podés poner `EVAL_API_KEY` y `BASE_URL` en el `.env` raíz (el script los carga con `dotenv`).

### Ablation 2×2 (transform × HyDE)

| `EVAL_EXPERIMENT_ID` | `EVAL_USE_QUERY_TRANSFORM` | `EVAL_USE_HYDE` |
|---|---|---|
| `baseline` | `false` | `false` |
| `transform_only` | `true` | `false` |
| `hyde_only` | `false` | `true` |
| `full` | `true` | `true` |

```powershell
cd backend

$env:EVAL_OUTPUT_DIR = "eval_results/TestsB_v2"
$env:EVAL_QUERY_DELAY_SECONDS = "3"

# Ejemplo: una corrida full
$env:EVAL_EXPERIMENT_ID = "full_r1"
$env:EVAL_USE_QUERY_TRANSFORM = "true"
$env:EVAL_USE_HYDE = "true"
python tests/eval_ragas.py
```

Outputs: `{EVAL_OUTPUT_DIR}/ragas_results_{experiment_id}_{timestamp}.md` (+ JSON y details).

### Reproducir una sola corrida (default: transform + HyDE)

```bash
cd backend

# Linux / macOS — EVAL_API_KEY y BASE_URL pueden venir del .env raíz
export OPENAI_API_KEY=sk-...

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."

python tests/eval_ragas.py
```

Resultados en `backend/tests/eval_results/` (JSON + Markdown).

---

## Stack

### Core RAG

| Componente | Rol |
|---|---|
| OpenAI | Embeddings (`text-embedding-3-small`) + generación (`gpt-4o-mini`) |
| Qdrant | Vector store + hybrid search |
| HyDE | Mejora de retrieval vía documento hipotético |
| Reranker local | Cross-encoder (`sentence-transformers`) |
| FastAPI | API HTTP |

### Observabilidad y calidad

| Componente | Rol |
|---|---|
| **LangFuse** | Trazas por step, tokens, costos, feedback |
| **RAGAS** | Evaluación offline del pipeline |

### Soporte (no es el foco del repo)

FastAPI, SQLAlchemy + SQLite, React + Vite, auth por API key (`create_user.py`). Docker Compose opcional para levantar Qdrant (+ backend) sin configurar servicios a mano.

---

## Quickstart

### Requisitos

- Python 3.12+
- Node.js 20+ (frontend)
- API key de [OpenAI](https://platform.openai.com/)
- [LangFuse Cloud](https://cloud.langfuse.com) (recomendado para ver trazas)
- Docker (solo para Qdrant, si no tenés uno corriendo)

### 1. Clonar y configurar

```bash
git clone https://github.com/Juanarena29/RAG-Platform.git
cd RAG-Platform
cp .env.example .env   # Windows: Copy-Item .env.example .env
```

Completar en `.env`:

```
OPENAI_API_KEY=sk-...
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

### 2. Levantar Qdrant

Para desarrollo local (SQLite, sin Postgres):

```bash
docker compose up qdrant -d
```

Para el stack completo con Postgres + backend en Docker:

```bash
docker compose up --build
```

> **Nota:** el quickstart de abajo usa **SQLite** (`DATABASE_URL=sqlite:///./rag_platform.db` en `.env.example`). Docker Compose sobreescribe a Postgres — elegí un camino u otro.

### 3. Backend + usuario demo

```bash
cd backend
python -m pip install -e ".[dev]"
python create_user.py    # imprime API key rag_... y crea tablas SQLite
uvicorn app.main:app --reload
```

### 4. Frontend

```bash
cd frontend
cp .env.example .env
# VITE_API_KEY=rag_...  (de create_user.py)
npm install
npm run dev
```

Abrí `http://localhost:5173` → subí PDFs → preguntá → revisá la traza en LangFuse.

---

## Variables clave

| Variable | Requerida | Default |
|---|---|---|
| `OPENAI_API_KEY` | Sí | — |
| `QDRANT_URL` | Sí | `http://localhost:6333` |
| `LANGFUSE_ENABLED` | Recomendada | `false` |
| `USE_HYDE_DEFAULT` | No | `true` |
| `USE_QUERY_TRANSFORM_DEFAULT` | No | `true` |
| `RERANKER_TYPE` | No | `local` (`cohere` opcional) |
| `QUERY_RATE_LIMIT` | No | `200/hour` (subir para batches de eval) |
| `DATABASE_URL` | No | `sqlite:///./rag_platform.db` |
| `EVAL_API_KEY` | Solo eval RAGAS | — (usar key de `create_user.py`) |
| `BASE_URL` | Solo eval RAGAS | `http://localhost:8000` |

Frontend (`frontend/.env`): `VITE_API_URL=http://localhost:8000`, `VITE_API_KEY=rag_...`

---

## API

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/documents/upload` | Sube PDF, ingestión async |
| `GET` | `/documents` | Estado de documentos |
| `POST` | `/query` | Pipeline RAG → `answer`, `sources`, `trace_id` |
| `POST` | `/feedback` | Feedback a LangFuse |
| `GET` | `/docs` | Swagger |

Auth: `Authorization: Bearer <api_key>` (generada con `create_user.py`).

---

## Tests

```bash
cd backend
python -m pytest -v
```

Incluye tests del pipeline RAG, ingestión, LangFuse/feedback y API.

---

## Documentación

- [`PROJECT.md`](PROJECT.md) — decisiones de diseño, glosario (HyDE, hybrid search, reranking)
- [`EXPERIMENT_HISTORY_INDEX.md`](EXPERIMENT_HISTORY_INDEX.md) — log de experimentos RAGAS (Part A: prompts, Part B: ablation, v1 y v2)
