import asyncio
from types import SimpleNamespace

import app.rag.hyde as hyde_module
from app.rag.hyde import generate_hypothetical_embedding


class _FakeAsyncOpenAI:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create_chat))
        self.embeddings = SimpleNamespace(create=self._create_embedding)
        self.fail_generation = False

    async def _create_chat(self, **kwargs):  # noqa: ANN003
        if self.fail_generation:
            raise RuntimeError("generation failed")
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="Hypothetical document about attention mechanisms."
                    )
                )
            ],
            usage=SimpleNamespace(prompt_tokens=20, completion_tokens=40),
        )

    async def _create_embedding(self, model: str, input: list[str]):  # noqa: A002
        return SimpleNamespace(
            data=[SimpleNamespace(embedding=[0.2] * 1536)],
            usage=SimpleNamespace(total_tokens=10),
        )


def test_generate_hypothetical_embedding_with_hyde(monkeypatch) -> None:
    monkeypatch.setattr(hyde_module, "AsyncOpenAI", _FakeAsyncOpenAI)

    result = asyncio.run(
        generate_hypothetical_embedding(
            "What is attention?",
            api_key="test-key",
            use_hyde=True,
        )
    )

    assert result.hyde_used is True
    assert len(result.query_vector) == 1536
    assert result.hypothetical_document is not None


def test_generate_hypothetical_embedding_without_hyde(monkeypatch) -> None:
    monkeypatch.setattr(hyde_module, "AsyncOpenAI", _FakeAsyncOpenAI)

    result = asyncio.run(
        generate_hypothetical_embedding(
            "What is attention?",
            api_key="test-key",
            use_hyde=False,
        )
    )

    assert result.hyde_used is False
    assert len(result.query_vector) == 1536


def test_generate_hypothetical_embedding_falls_back_on_generation_error(monkeypatch) -> None:
    class _FailingOpenAI(_FakeAsyncOpenAI):
        async def _create_chat(self, **kwargs):  # noqa: ANN003
            raise RuntimeError("generation failed")

    monkeypatch.setattr(hyde_module, "AsyncOpenAI", _FailingOpenAI)

    result = asyncio.run(
        generate_hypothetical_embedding(
            "What is attention?",
            api_key="test-key",
            use_hyde=True,
        )
    )

    assert result.hyde_used is False
    assert len(result.query_vector) == 1536
