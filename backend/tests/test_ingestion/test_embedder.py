import asyncio
from types import SimpleNamespace

import app.ingestion.embedder as embedder_module
from app.ingestion.chunker import Chunk
from app.ingestion.embedder import embed_chunks


class _FakeAsyncOpenAI:
    calls: list[list[str]] = []

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.embeddings = SimpleNamespace(create=self._create)

    async def _create(self, model: str, input: list[str]):  # noqa: A002
        _FakeAsyncOpenAI.calls.append(input)
        data = [SimpleNamespace(embedding=[0.1] * 1536) for _ in input]
        return SimpleNamespace(data=data)


def _make_chunks(total: int) -> list[Chunk]:
    return [
        Chunk(
            document_id=1,
            chunk_index=index,
            page_number=0,
            text=f"chunk-{index}",
        )
        for index in range(total)
    ]


def test_embed_chunks_batches_requests(monkeypatch) -> None:
    _FakeAsyncOpenAI.calls = []
    monkeypatch.setattr(embedder_module, "AsyncOpenAI", _FakeAsyncOpenAI)

    chunks = _make_chunks(150)
    embedded = asyncio.run(embed_chunks(chunks, api_key="test-key", batch_size=100))

    assert len(_FakeAsyncOpenAI.calls) == 2
    assert len(_FakeAsyncOpenAI.calls[0]) == 100
    assert len(_FakeAsyncOpenAI.calls[1]) == 50
    assert len(embedded) == 150
    assert all(len(item.vector) == 1536 for item in embedded)
