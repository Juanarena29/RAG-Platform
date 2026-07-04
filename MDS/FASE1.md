# Fase 1 — Base del proyecto y seguridad

## Resumen ejecutivo
En esta fase se construyó la base operativa del backend para una plataforma RAG orientada a producción: inicialización del proyecto Python con FastAPI, configuración tipada por entorno, capa de persistencia con SQLAlchemy, migraciones con Alembic, autenticación por API key hasheada, middleware de CORS y rate limiting, y una suite de tests + pipeline de CI que valida calidad automáticamente. El resultado no es solo "una API que responde", sino una base con contratos claros de configuración, seguridad mínima obligatoria y validación continua.

El problema principal que resuelve esta fase es evitar deuda técnica temprana en tres ejes que después son caros de corregir: seguridad, consistencia de entorno y evolución de base de datos. En lugar de empezar por features de RAG, se establecieron primero los cimientos que permiten crecer sin reescribir (autenticación reutilizable, DB migrable, errores estandarizados, tests repetibles y CI bloqueante).

Esta fase habilita directamente la Fase 2 porque ya existe un backend autenticado, con modelo de usuarios y keys, almacenamiento relacional versionado, healthcheck para operación, y un entorno local con PostgreSQL/Qdrant por Docker Compose. Sobre esta base, la ingestión async puede agregarse como funcionalidad incremental sin rediseñar estructura.

## Stack de la fase
| Tecnología | Versión en el proyecto | Uso específico en esta fase |
|---|---|---|
| Python | `>=3.12` | Runtime del backend y estándar de tipado usado en todo el código. |
| FastAPI | sin pin explícito (`pyproject.toml`) | Framework HTTP para exponer `/health` y `/me`, resolver dependencias y registrar handlers globales. |
| Uvicorn | sin pin explícito (`uvicorn[standard]`) | Servidor ASGI para ejecutar la API localmente y en contenedor. |
| Pydantic Settings | sin pin explícito | Carga y validación tipada de variables de entorno desde `.env`. |
| SQLAlchemy | sin pin explícito | ORM para engine, sesión, modelos `User`/`ApiKey`/`UsageLog`, y consultas de autenticación. |
| Alembic | sin pin explícito (dev dependency) | Migraciones versionadas del esquema y primera revisión inicial. |
| SlowAPI | sin pin explícito | Rate limiting por request IP con respuesta `429` automática. |
| Structlog | sin pin explícito | Logging estructurado JSON para observabilidad básica de la app. |
| Pytest | sin pin explícito (dev dependency) | Validación automática de auth, middleware, config, modelos y health endpoint. |
| Ruff | sin pin explícito (dev dependency) | Linting/estilo y orden de imports, ejecutado local y en CI. |
| PostgreSQL (Docker) | `postgres:16-alpine` | Base relacional de desarrollo avanzada para paridad con producción. |
| SQLite | `sqlite:///./rag_platform.db` (dev default) | DB local simple por default para iteración rápida sin infraestructura extra. |
| Qdrant (Docker) | `qdrant/qdrant:latest` | Servicio vectorial preparado para las fases de ingestión y retrieval. |
| GitHub Actions | `actions/checkout@v4`, `actions/setup-python@v5` | CI bloqueante: `ruff` antes de `pytest` en cada push/PR a `main`. |

## Arquitectura de la fase
El flujo de una request empieza en `app.main` donde se crea la instancia de FastAPI, se cargan settings, se configura logging, se registra middleware y se conectan handlers globales de excepciones. En esta fase, `/health` entra por un router público y `/me` entra por una ruta protegida.

Cuando la request entra, primero pasa por middlewares de Starlette/FastAPI y por `CORSMiddleware`, que controla si el origen está permitido según `cors_allowed_origins`. Si la ruta está decorada con limitador (`/me`), SlowAPI evalúa el contador del cliente (key por IP en esta fase). Si se supera el límite, se corta el flujo con `429` y no se ejecuta lógica de negocio.

Si la request llega a `/me`, FastAPI resuelve la dependency `get_current_user` de `app/api/deps.py`. Esa dependency lee `Authorization`, valida que sea formato `Bearer`, extrae la API key, la hashea con SHA-256 y consulta `api_keys` por hash activo. Si no existe o el usuario no está activo, devuelve `401`. Si todo es válido, retorna el objeto `User` y el endpoint responde con datos básicos del usuario autenticado.

Si ocurre un error de validación (`422`), HTTP (`4xx/5xx` explícito) o excepción no controlada (`500`), `main.py` redirige el manejo a `app/core/exceptions.py`, lo que unifica formato de respuesta y evita respuestas inconsistentes del framework por defecto.

Este flujo está respaldado por SQLAlchemy para acceso a datos, por Alembic para evolución de esquema, y por tests que reproducen el ciclo completo (request HTTP real con `TestClient`, override de DB y fixtures de usuario/API key).

Snippet real de inicialización del flujo principal (`backend/app/main.py`):

```python
app = FastAPI(title=settings.app_name, version=settings.app_version)

setup_middleware(app)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(health_router.router)

@app.get("/me")
@limiter.limit(settings.default_rate_limit)
def me(request: Request, current_user: User = Depends(get_current_user)) -> dict[str, str | int]:
    return {"id": current_user.id, "email": current_user.email}
```

## Archivos y su propósito
### Infraestructura raíz
`/.env.example` define el contrato de configuración del proyecto sin exponer secretos. Existe separado para desacoplar configuración del código y evitar que valores sensibles se mezclen con versionado. Si no existiera, cada entorno quedaría implícito y sería más probable romper ejecución por variables faltantes. Se conecta con `Settings` en `app/core/config.py`.

`/.gitignore` evita versionar secretos, basura de Python y artefactos locales (`.env`, `*.db`, caches, `node_modules`). Existe separado porque afecta todo el monorepo, no solo backend. Si no existiera, habría riesgo alto de commitear secretos y ruido de build.

`/docker-compose.yml` levanta `backend`, `postgres` y `qdrant`, y conecta `backend` con PostgreSQL vía `DATABASE_URL`. Existe para reproducir localmente un entorno cercano a producción sin instalación manual de servicios. Sin este archivo, cada developer debería levantar dependencias de forma artesanal.

`/.github/workflows/ci.yml` define CI para backend: instala dependencias, ejecuta `ruff` y luego `pytest`. Existe separado porque la validación automática debe vivir con infraestructura de repositorio. Sin CI, la calidad dependería solo de disciplina manual.

### Backend base y packaging
`backend/pyproject.toml` centraliza dependencias, metadata y config de herramientas (`pytest`, `ruff`). Existe para tener un único punto de verdad del proyecto Python. Sin él, habría configuración dispersa y más difícil de mantener.

`backend/Dockerfile` empaqueta backend en contenedor con `uvicorn`. Existe separado de Compose porque define la imagen de la app, mientras Compose orquesta múltiples servicios. Sin Dockerfile, Compose no podría construir el servicio backend.

`backend/alembic.ini` configura Alembic y apunta a `app/db/migrations`. Existe separado porque Alembic lo requiere como archivo de runtime/config. Sin él, no hay ejecución estándar de migraciones.

`backend/README.md` documenta quickstart operativo del backend. Existe para onboarding rápido y ejecución reproducible.

### Core de aplicación
`backend/app/core/config.py` define clase `Settings` tipada con `pydantic-settings` y `get_settings()` cacheado. Existe separado para evitar hardcodear configuración en módulos funcionales. Sin este archivo, múltiples módulos duplicarían lectura de env vars y crecería el riesgo de inconsistencias.

`backend/app/core/exceptions.py` centraliza handlers HTTP/validación/excepción no controlada. Existe para estandarizar respuestas de error. Sin él, cada endpoint/middleware manejaría errores a su manera.

`backend/app/core/logging.py` configura structlog JSON. Existe separado para desacoplar observabilidad de lógica de negocio. Sin él, no habría formato de logs consistente ni base para trazabilidad.

### API layer
`backend/app/main.py` compone la app: settings, logging, middleware, handlers, routers y endpoint protegido `/me`. Existe como entrypoint único ASGI. Sin este archivo, no hay bootstrap de la aplicación.

`backend/app/api/middleware.py` encapsula CORS y rate limiting. Existe separado porque middleware es una preocupación transversal, no lógica de endpoint. Sin él, esas políticas quedarían dispersas y difíciles de auditar.

`backend/app/api/deps.py` contiene `get_current_user` para autenticación reusable. Existe separado porque auth por dependency debe ser composable entre rutas. Sin él, cada endpoint repetiría validación de headers/keys.

`backend/app/api/routes/health.py` define router público de salud. Existe separado para mantener estructura por rutas y no sobrecargar `main.py`. Sin él, se rompe la separación API bootstrap vs API endpoints.

### Seguridad (auth)
`backend/app/auth/hashing.py` implementa hash SHA-256 de API keys. Existe separado para encapsular primitivas criptográficas. Sin él, hashing se duplicaría en varios módulos.

`backend/app/auth/api_key.py` genera API keys seguras y valida keys activas contra DB por hash. Existe separado porque gestión de credenciales requiere capa propia. Sin él, `deps.py` tendría demasiadas responsabilidades.

### Persistencia y migraciones
`backend/app/db/database.py` crea engine SQLAlchemy, sesión y dependency `get_db`. Existe separado para centralizar acceso a DB. Sin él, cada módulo configuraría engine/sesión por su cuenta.

`backend/app/db/models.py` define entidades `User`, `ApiKey`, `UsageLog` y relaciones. Existe separado para que ORM y negocio de datos estén versionados y reutilizables. Sin él, no hay contrato relacional para auth/auditoría.

`backend/app/db/migrations/env.py` conecta Alembic con `Base.metadata` y `Settings`. Existe porque Alembic lo usa para autogenerar y aplicar migraciones con contexto real de app.

`backend/app/db/migrations/versions/3ae23d52ebea_initial_schema.py` es la primera migración de esquema. Existe para versionar estado inicial de DB de forma reproducible. Sin este archivo, no hay forma segura de recrear esquema en otros entornos.

### Testing
`backend/tests/conftest.py` aporta fixtures reutilizables (`db_session`, `client`, `test_user_with_key`). Existe para evitar duplicación de setup. Sin él, tests quedan acoplados y frágiles.

`backend/tests/test_health.py` valida endpoint público de salud.

`backend/tests/test_config.py` valida defaults y caching de settings.

`backend/tests/test_models.py` valida nombres de tablas como smoke test de mapping ORM.

`backend/tests/test_auth_api_key.py` valida hashing y generación de API keys.

`backend/tests/test_auth_http.py` valida auth HTTP real en `/me` (válida/ inválida/ sin header).

`backend/tests/test_middleware.py` valida comportamiento CORS y rate limit.

## Decisiones de diseño
### SQLite en desarrollo y PostgreSQL en producción
Se decidió usar SQLite como default local (`database_url` en config) porque reduce fricción inicial y acelera iteración. Se preparó PostgreSQL en Docker Compose porque el entorno objetivo de producción es PostgreSQL y se necesitaba paridad funcional para detectar incompatibilidades temprano. Esta decisión permite avanzar rápido en local sin sacrificar camino de producción.

### Hashear API keys y no guardarlas en texto plano
Se eligió persistir solo `key_hash` y `key_prefix`, nunca la key completa. Si la base se compromete, no se exponen credenciales reutilizables. La validación se hace por hash (`get_active_api_key`) y la key cruda solo vive en memoria al momento de creación/uso.

Snippet real (`backend/app/auth/api_key.py`):

```python
token = secrets.token_urlsafe(API_KEY_TOKEN_BYTES)
raw_key = f"{API_KEY_PREFIX}{token}"
key_prefix = raw_key[:KEY_PREFIX_VISIBLE_CHARS]
key_hash = hash_api_key(raw_key)
```

### `/health` sin autenticación
Se decidió dejar `/health` público para que plataformas de despliegue y monitoreo puedan verificar liveness/readiness sin depender de credenciales de usuario. Si este endpoint exigiera auth, los health checks operativos serían más complejos y frágiles.

### `pydantic-settings` para variables de entorno
Se eligió por tipado, validación y fallback declarativo en un solo lugar (`Settings`). La alternativa manual con `os.getenv` dispersa la configuración y oculta errores de tipo hasta runtime tardío.

### Alembic para migraciones
Se eligió Alembic porque permite evolucionar esquema con historial versionado y reproducible. En fases siguientes habrá cambios frecuentes en modelos; sin migraciones, mantener coherencia entre entornos sería riesgoso.

### Dependency-based auth con `get_current_user`
Se decidió encapsular auth como dependency FastAPI para que cualquier endpoint nuevo pueda protegerse con `Depends(get_current_user)` sin reescribir validaciones. Esta decisión reduce duplicación y evita divergencia de reglas de seguridad.

### Rate limiting temprano
Se activó SlowAPI en Fase 1 para evitar abuso/costos desde el inicio, incluso antes de integrar OpenAI. La implicancia positiva para Fase 2+ es que ingestión y query ya nacerán en un sistema con control de tráfico.

## Seguridad implementada
La validación de autenticación por bearer token previene acceso anónimo a endpoints protegidos. Está implementada en `app/api/deps.py`, donde faltas de header, esquema inválido o key inexistente retornan `401` explícito.

El hash SHA-256 de API key previene exposición directa de credenciales en caso de fuga de base. Vive en `app/auth/hashing.py` y se usa en `app/auth/api_key.py`.

La generación de keys con `secrets.token_urlsafe(32)` previene claves predecibles y ataques de fuerza bruta triviales por baja entropía. Vive en `app/auth/api_key.py`.

El flag `is_active` en `ApiKey` y `User` permite revocación lógica sin borrar historial y previene uso de credenciales/usuarios desactivados. Vive en `app/db/models.py` y es validado en `deps.py`.

El rate limiting (`60/minute` por IP en esta fase) previene abuso de endpoints y reduce superficie de DoS básico. Está en `app/api/middleware.py` y aplicado en `/me`.

La política CORS restringida a localhost en dev previene consumo desde orígenes arbitrarios de browser durante desarrollo. Está en `app/api/middleware.py` y parametrizada por `config.py`.

La estandarización de errores previene fugas accidentales de detalles internos en respuestas públicas, especialmente para excepciones no manejadas (`500` genérico). Vive en `app/core/exceptions.py`.

## Testing
En esta fase se testea el núcleo de estabilidad y seguridad: configuración (`Settings` y caché), hash y creación de API keys, autenticación HTTP en rutas protegidas, endpoint de salud público, middlewares de CORS/rate limit y contrato mínimo de modelos. Esos casos se eligieron porque validan lo que más puede romper la base de una plataforma: acceso, config y disponibilidad.

No se testea todavía lógica de ingestión de documentos, vectorización, retrieval, orquestación de workflows ni métricas de calidad RAG, porque esas capacidades todavía no existen en la Fase 1 y pertenecen a Fases 2/3/4. Tampoco se testea integración real con servicios externos (Qdrant/OpenAI/Inngest) porque el objetivo de esta fase es consolidar la base, no validar pipeline de negocio.

Para ejecutar tests localmente:

```bash
cd backend
python -m pip install -e ".[dev]"
python -m pytest -v
```

## CI/CD
El pipeline vive en `.github/workflows/ci.yml` y corre en cada `push` o `pull_request` hacia `main`.

Primero hace checkout del repositorio para obtener el estado exacto del código. Luego instala Python 3.12 para asegurar paridad con el runtime definido en `pyproject.toml`. Después instala dependencias del backend con `pip install -e ".[dev]"`, incluyendo herramientas de calidad y test.

Luego ejecuta `ruff` antes que `pytest`. Ese orden es intencional: lint falla más rápido, cuesta menos tiempo de cómputo y evita correr tests cuando el código ya incumple reglas básicas. Si `ruff` falla, el job se detiene y no llega a tests. Si `ruff` pasa, se ejecuta `pytest`; cualquier test fallido marca el pipeline como failed y bloquea integración.

## Cómo levantar el proyecto localmente
Cloná el repositorio y ubicate en la raíz:

```bash
git clone <URL_DEL_REPO>
cd RagProject
```

Creá el archivo de entorno a partir del template:

```bash
cp .env.example .env
```

Levantá infraestructura con Docker Compose (PostgreSQL, Qdrant y backend):

```bash
docker compose up --build
```

Si querés correr backend sin contenedor, usá entorno local de Python:

```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Verificá que está funcionando:

```bash
curl http://localhost:8000/health
```

Correr tests:

```bash
cd backend
python -m pytest -v
```

## Qué habilita esta fase
Con Fase 1 cerrada ya es posible construir funcionalidad de ingestión de Fase 2 sobre una base sólida: existe identidad de usuario por API key, existe DB versionada para registrar documentos/procesamientos, existe entorno local con servicios externos relevantes, existe rate limiting para proteger endpoints costosos y existe CI para evitar regresiones al acelerar desarrollo.

Antes de esta fase, agregar ingestión habría significado construir features sobre un sistema sin contratos de seguridad ni gobernanza de cambios de esquema. Después de esta fase, cada nuevo módulo puede enchufarse a una arquitectura establecida: settings tipados, dependencies reutilizables, sesiones DB estandarizadas y validación automática por test+CI.

## Dudas y decisiones pendientes
La migración inicial fue autogenerada antes del ajuste a `DateTime(timezone=True)` en modelos, por lo que conviene alinear en la próxima migración para evitar drift sutil entre metadata actual y esquema inicial histórico.

El rate limit usa IP como `key_func` en esta fase, decisión válida para arrancar pero provisional para multi-tenant real; más adelante convendrá limitar por identidad de API key/user.

Existe endpoint protegido `/me` como endpoint técnico de validación de auth; en fases siguientes habrá que decidir si se conserva como endpoint operativo o se reemplaza por rutas de dominio reales.

CORS está orientado a localhost para desarrollo. Antes de producción debe cerrarse a dominio frontend real y policy explícita por entorno.

El logging estructurado está configurado, pero todavía no hay instrumentación de eventos de negocio (request_id, user_id bind automático, costos/tiempos de pipeline) porque eso corresponde a fases de observabilidad.
