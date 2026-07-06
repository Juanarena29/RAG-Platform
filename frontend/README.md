# Frontend

UI de demo para el RAG Platform: upload de PDFs y chat con citas.

## Setup

Ver el [README principal](../README.md) para el flujo completo.

```bash
cd frontend
cp .env.example .env
# Completar VITE_API_KEY con la key generada por backend/create_user.py
npm install
npm run dev
```

Variables en `frontend/.env`:

| Variable | Descripción |
|---|---|
| `VITE_API_URL` | URL del backend (default: `http://localhost:8000`) |
| `VITE_API_KEY` | API key `rag_...` del usuario demo |
