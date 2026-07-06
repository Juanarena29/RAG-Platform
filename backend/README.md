# Backend

API backend del RAG Platform, construida con FastAPI.

## Quickstart

Ver el [README principal](../README.md) para setup completo con Docker, frontend y variables de entorno.

### Solo backend

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

### Crear usuario y API key

```bash
python create_user.py
```

### Tests

```bash
python -m pytest -v
```
