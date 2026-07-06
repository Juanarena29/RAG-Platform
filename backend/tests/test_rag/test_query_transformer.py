import asyncio
from types import SimpleNamespace

import app.rag.query_transformer as query_transformer_module
from app.rag.query_transformer import transform_query


class _FakeAsyncOpenAI:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))
        self.should_fail = False

    async def _create(self, **kwargs):  # noqa: ANN003
        if self.should_fail:
            raise RuntimeError("llm unavailable")
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Rewritten technical query"))],
            usage=SimpleNamespace(prompt_tokens=12, completion_tokens=8),
        )


def test_transform_query_returns_rewritten_text(monkeypatch) -> None:
    monkeypatch.setattr(query_transformer_module, "AsyncOpenAI", _FakeAsyncOpenAI)

    result = asyncio.run(transform_query("what is attention?", api_key="test-key"))

    assert result.original_query == "what is attention?"
    assert result.transformed_query == "Rewritten technical query"


def test_transform_query_falls_back_on_llm_error(monkeypatch) -> None:
    class _FailingOpenAI(_FakeAsyncOpenAI):
        async def _create(self, **kwargs):  # noqa: ANN003
            raise RuntimeError("llm unavailable")

    monkeypatch.setattr(query_transformer_module, "AsyncOpenAI", _FailingOpenAI)

    result = asyncio.run(transform_query("what is attention?", api_key="test-key"))

    assert result.transformed_query == "what is attention?"
