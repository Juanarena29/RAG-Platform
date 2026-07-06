import asyncio
import json
from types import SimpleNamespace

import app.rag.generator as generator_module
from app.rag.generator import generate_answer
from app.rag.retriever import RetrievedChunk


class _FakeAsyncOpenAI:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    async def _create(self, **kwargs):  # noqa: ANN003
        payload = {
            "answer": "Attention allows models to focus on relevant tokens [1].",
            "cited_indices": [1],
        }
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))],
            usage=SimpleNamespace(prompt_tokens=100, completion_tokens=25),
        )


def test_generate_answer_parses_json_response(monkeypatch) -> None:
    monkeypatch.setattr(generator_module, "AsyncOpenAI", _FakeAsyncOpenAI)

    chunks = [
        RetrievedChunk(
            document_id=1,
            chunk_index=0,
            page_number=1,
            text="Attention mechanism details",
            user_id=1,
            score=0.9,
        )
    ]

    result = asyncio.run(generate_answer("What is attention?", chunks, api_key="test-key"))

    assert "Attention allows models" in result.answer
    assert result.cited_indices == [1]


def test_generate_answer_without_chunks_returns_safe_message() -> None:
    result = asyncio.run(generate_answer("What is attention?", [], api_key="test-key"))

    assert "enough information" in result.answer.lower()
    assert result.cited_indices == []
