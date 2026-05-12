# Fase 2 — Pipeline de ingestión async

## Resumen ejecutivo
En esta fase se implementó la funcionalidad de **ingestión de documentos** como pipeline: el usuario sube un PDF vía API, el backend lo **valida**, lo **parsea**, lo **divide en chunks**, genera **embeddings** con OpenAI y finalmente **almacena vectores en Qdrant**, aislando por usuario.

El objetivo de Fase 2 no fue solamente "procesar PDFs", sino construir un flujo:
- **modular y testeable** (validator/parser/chunker/embedder desacoplados),
- **asíncrono** para responder rápido en el endpoint de upload,
- con **estado persistido en DB** para trazabilidad operativa,
- y con **aislamiento multi-tenant** tanto en DB como en vector store.

Esta fase habilita directamente la Fase 3 porque ya existe una base de chunks embebidos y persistidos por usuario sobre la que el retriever puede ejecutar búsqueda semántica con garantías de aislamiento.

## Stack de la fase
| Tecnología | Versión en el proyecto | Uso específico en esta fase |
|---|---|---|
| Python | `>=3.12` | Runtime del backend, tipado y funciones async. |
| FastAPI | sin pin explícito | Endpoints `POST /documents/upload` y `GET /documents`. |
| SQLAlchemy | sin pin explícito | Persistencia de `Document`, `UsageLog` y transiciones de estado. |
| Alembic | sin pin explícito (dev dependency) | Migración de esquema para tabla `documents`. |
| PyMuPDF (`pymupdf`, import `fitz`) | sin pin explícito | Parsing de PDF a texto por página. |
| langchain-text-splitters | sin pin explícito | Chunking recursivo por coherencia textual. |
| OpenAI SDK | sin pin explícito | Embeddings con `text-embedding-3-small`. |
| Tenacity | sin pin explícito | Reintentos exponenciales en errores transitorios de embeddings. |
| qdrant-client | sin pin explícito | Creación de colección y `upsert` de vectores. |
| python-multipart | sin pin explícito | Soporte multipart para `UploadFile` en FastAPI. |
| Inngest | sin pin explícito | Dependencia preparada para workflows; en esta implementación no está montado en `main.py`. |
| Pytest | sin pin explícito (dev dependency) | Tests unitarios de ingestión y tests de API/workflow. |
| Ruff | sin pin explícito (dev dependency) | Validación de lint y estilo. |

## Arquitectura de la fase
El flujo completo arranca en `POST /documents/upload`. El endpoint valida el archivo, lo guarda en disco, crea un registro `Document` en estado `pending`, registra uso en `UsageLog` y dispara una tarea asíncrona (`asyncio.create_task`) que procesa el documento en background.

El procesamiento en background vive en `process_document_event` y ejecuta esta secuencia:
1. Marca el documento como `processing`.
2. Relee bytes desde disco y vuelve a validar.
3. Parsea el PDF a texto por página.
4. Divide el texto en chunks con metadatos.
5. Genera embeddings por lotes.
6. Crea colección Qdrant `user_{id}` si no existe.
7. Hace `upsert` de puntos con payload por chunk.
8. Actualiza estado final en DB (`completed` o `failed`).

Diagrama del flujo:

```mermaid
flowchart LR
    Client -->|"POST multipart/form-data"| Upload["POST /documents/upload"]
    Upload -->|"validate + save + create Document(pending)"| DB[(DB)]
    Upload -->|"create_task"| Worker["process_document_event()"]
    Upload -->|"202 Accepted"| Client

    Worker -->|"status=processing"| DB
    Worker --> Validator["validator.py"]
    Worker --> Parser["parser.py"]
    Worker --> Chunker["chunker.py"]
    Worker --> Embedder["embedder.py"]
    Worker --> Qdrant[(Qdrant user_{id})]
    Worker -->|"status=completed/failed"| DB
```

## Archivos y su propósito
### Infraestructura y configuración
`/.env.example` se extendió con variables de Fase 2:
- `INNGEST_EVENT_KEY`
- `INNGEST_SIGNING_KEY`
- `UPLOAD_DIR`
- `MAX_UPLOAD_SIZE_MB`

Además ya estaban `OPENAI_API_KEY`, `QDRANT_URL` y `QDRANT_API_KEY`, que pasan a ser críticas para este pipeline.

`backend/pyproject.toml` incorporó dependencias runtime necesarias para ingestión (`pymupdf`, `openai`, `qdrant-client`, `langchain-text-splitters`, `tenacity`, `python-multipart`, `inngest`).

`backend/app/core/config.py` agregó settings tipados para orquestar el pipeline:
- `openai_api_key`
- `qdrant_url`
- `qdrant_api_key`
- `inngest_event_key`
- `inngest_signing_key`
- `upload_dir`
- `max_upload_size_mb`

### Persistencia y migraciones
`backend/app/db/models.py` se amplió con:
- relación `User.documents`
- nuevo modelo `Document` con:
  - identidad y ownership (`id`, `user_id`)
  - metadata del archivo (`original_filename`, `filename`, `file_path`, `file_size`)
  - estado del pipeline (`status`, `chunk_count`, `error_message`)
  - timestamps (`created_at`, `processed_at`)

`backend/app/db/migrations/versions/9b1f5a7d2c10_add_documents_table.py` crea tabla `documents` con índices en `id`, `status` y `user_id`.

`backend/app/db/repositories.py` centraliza operaciones de documentos:
- `create_document(...)`
- `get_document(...)`
- `get_documents_by_user(...)`
- `update_document_status(...)`

Esto mantiene la capa HTTP desacoplada de queries concretas.

### Módulo de ingestión
`backend/app/ingestion/validator.py`
- Valida bytes crudos del archivo.
- Reglas:
  - no vacío,
  - firma `%PDF-`,
  - tamaño máximo configurable.
- Usa excepción de dominio `DocumentValidationError` con `error_code`:
  - `EMPTY_FILE`
  - `INVALID_FORMAT`
  - `FILE_TOO_LARGE`

`backend/app/ingestion/parser.py`
- Convierte bytes PDF a `list[PageContent]`.
- Conserva `page_number` por página.
- Limpia texto:
  - normaliza `\r\n`,
  - elimina cortes de palabra por guion (`-\n`),
  - reduce saltos excesivos.
- Si no puede abrir/extraer, lanza `DocumentParsingError`.

`backend/app/ingestion/chunker.py`
- Transforma páginas en `Chunk`.
- Usa `RecursiveCharacterTextSplitter` con separadores:
  - `"\n\n"`, `"\n"`, `". "`, `" "`.
- Config por defecto:
  - `chunk_size=2000`,
  - `chunk_overlap=100`.
- Preserva metadata:
  - `document_id`
  - `chunk_index` secuencial global
  - `page_number`

`backend/app/ingestion/embedder.py`
- Genera embeddings async por lotes.
- Modelo fijo: `text-embedding-3-small`.
- Dimensión esperada: `1536`.
- Lote por defecto: `100`.
- Retry con `tenacity` en:
  - `RateLimitError`
  - `APIConnectionError`
- Backoff exponencial y hasta 3 intentos.

`backend/app/ingestion/inngest_functions.py`
- Contiene `process_document_event`, orquestador real del pipeline de fondo.
- Responsabilidades:
  - transición de estado (`processing` -> `completed/failed`)
  - parse/chunk/embed
  - operación contra Qdrant
  - persistencia de errores
- Multi-tenant vectorial:
  - colección: `user_{user_id}`
- Id de punto determinista por chunk:
  - hash de `document_id:chunk_index`
- Payload por punto:
  - `document_id`, `chunk_index`, `page_number`, `text`, `user_id`

### API y contratos
`backend/app/schemas/documents.py`
- `UploadResponse`
- `DocumentStatus`
- `DocumentListResponse`

`backend/app/api/routes/documents.py`
- `POST /documents/upload`
  - requiere auth
  - rate limit `10/hour`
  - valida PDF
  - guarda en `UPLOAD_DIR/user_{id}/<uuid>.pdf`
  - crea `Document(status="pending")`
  - registra `UsageLog`
  - dispara background task
  - responde `202`
- `GET /documents`
  - requiere auth
  - lista solo documentos del usuario autenticado

`backend/app/main.py`
- incluye el router de documentos:
  - `app.include_router(documents_router.router)`

## Decisiones de diseño clave
### Validar por magic bytes en vez de confiar en content-type
El `content-type` lo controla el cliente y puede ser incorrecto o malicioso. Verificar `%PDF-` en bytes elimina ambigüedad en la detección de formato.

### Estado explícito en DB para operabilidad
Usar `pending/processing/completed/failed` en `Document` permite inspección operativa, troubleshooting y futuras UI/estados de progreso sin inferencias indirectas.

### Separación en módulos especializados
Validator, parser, chunker y embedder son piezas independientes. Esto:
- reduce acoplamiento,
- simplifica test unitario,
- permite reemplazos futuros (otro parser/modelo de embedding) sin reescribir endpoint.

### Chunking recursivo con metadatos de página
Se prioriza coherencia textual y trazabilidad (página origen) para facilitar citas en Fase 3.

### Embeddings por lotes + retry
Batching reduce overhead y retry maneja errores transitorios de red/rate limit, mejorando robustez sin duplicar lógica en endpoint.

### Aislamiento multi-tenant en Qdrant
Cada usuario escribe en colección `user_{id}` derivada del contexto autenticado. El cliente no elige colección, lo que evita filtraciones entre tenants.

### Upsert idempotente por chunk
El `point_id` determinista evita duplicaciones ante reintentos del procesamiento de un mismo documento.

## Seguridad implementada en Fase 2
- **Auth obligatoria** en endpoints de documentos mediante `get_current_user`.
- **Aislamiento de ownership**:
  - en DB: queries de listado filtradas por `user_id`.
  - en Qdrant: colección por usuario.
- **Validación temprana de archivo** (tipo y tamaño) antes de parseo/embedding.
- **No exposición de secretos**:
  - OpenAI/Qdrant por variables de entorno.
- **Rate limiting específico en upload** (`10/hour`) para controlar abuso de endpoints costosos.

## Testing
Se incorporó una suite de tests para cubrir comportamiento de ingestión y API:

### Unit tests de ingestión
`backend/tests/test_ingestion/test_validator.py`
- PDF válido pasa.
- formato inválido falla con `INVALID_FORMAT`.
- archivo grande falla con `FILE_TOO_LARGE`.
- archivo vacío falla con `EMPTY_FILE`.

`backend/tests/test_ingestion/test_parser.py`
- parsea PDF simple y devuelve texto.
- mantiene `page_number` en PDFs multipágina.
- bytes inválidos disparan `DocumentParsingError`.

`backend/tests/test_ingestion/test_chunker.py`
- texto corto produce un chunk.
- texto largo produce varios chunks.
- `chunk_index` secuencial y `page_number` preservado.

`backend/tests/test_ingestion/test_embedder.py`
- mock de cliente OpenAI async.
- valida batching (150 chunks -> 2 llamadas: 100 + 50).
- valida cantidad de embeddings y dimensión esperada.

`backend/tests/test_ingestion/test_inngest.py`
- testea flujo de `process_document_event` con mocks.
- caso exitoso:
  - termina en `completed`
  - setea `chunk_count`.
- caso fallido:
  - termina en `failed`
  - persiste `error_message`.

### Tests de API de documentos
`backend/tests/test_api/test_documents.py`
- upload sin auth -> `401`.
- upload válido -> `202` + documento `pending` persistido.
- upload no PDF -> `400`.
- upload oversized -> `400`.
- `GET /documents`:
  - sin auth -> `401`
  - con auth lista solo documentos propios (aislamiento por usuario).

Además, se agregó cobertura en modelos para relación/defaults de `Document` en `backend/tests/test_models.py`.

## CI/CD y validación
Con esta fase ya integrada, el proyecto mantiene el mismo ciclo de calidad:
- `ruff check .`
- `pytest`

La implementación actual pasó con suite completa:
- **62 tests passing**.

## Cómo ejecutar y validar Fase 2 localmente
1. Instalar dependencias:
```bash
cd backend
python -m pip install -e ".[dev]"
```

2. Configurar `.env` (en raíz) con al menos:
- `OPENAI_API_KEY`
- `QDRANT_URL`
- `UPLOAD_DIR`
- `MAX_UPLOAD_SIZE_MB`

3. Aplicar migraciones:
```bash
cd backend
alembic upgrade head
```

4. Levantar servicios (si usás Docker Compose desde raíz):
```bash
docker compose up --build
```

5. Probar upload:
- `POST /documents/upload` con bearer token válido y archivo PDF.

6. Verificar listado:
- `GET /documents` para confirmar persistencia del documento.

7. Correr tests:
```bash
cd backend
python -m pytest -v
```

## Qué habilita esta fase
Con Fase 2 cerrada, el proyecto ya cuenta con:
- Ingestión end-to-end de PDFs por API.
- Persistencia de estado de procesamiento por documento.
- Vectores almacenados en Qdrant con aislamiento por usuario.
- Base de datos documental lista para retrieval semántico.

Esto permite que Fase 3 se enfoque en query transformation, retrieval híbrido, reranking y generación con citas, reutilizando la infraestructura de documentos ya disponible.

## Dudas y decisiones pendientes
- Aunque existe `inngest` como dependencia y `inngest_functions.py` como módulo, el procesamiento actual se dispara con `asyncio.create_task` y no con un servidor de workflow durable. Si se requiere resiliencia avanzada ante reinicios/caídas, conviene montar Inngest explícitamente.
- El endpoint de upload hoy guarda archivo completo en disco antes de encolar procesamiento. Para escalar volumen, se podría migrar a storage externo (S3/R2) y procesamiento por referencia.
- La estrategia de chunking es efectiva para empezar, pero puede ajustarse (tamaño/overlap/separadores) según métricas de retrieval de Fase 3.
