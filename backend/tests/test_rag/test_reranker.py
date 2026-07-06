import sys
from types import SimpleNamespace

import app.rag.reranker as reranker_module
from app.rag.reranker import rerank
from app.rag.retriever import RetrievedChunk


def _make_chunks() -> list[RetrievedChunk]:
    return [
        RetrievedChunk(
            document_id=1,
            chunk_index=0,
            page_number=1,
            text="low relevance",
            user_id=1,
            score=0.2,
        ),
        RetrievedChunk(
            document_id=1,
            chunk_index=1,
            page_number=2,
            text="high relevance",
            user_id=1,
            score=0.8,
        ),
    ]


class _FakeCrossEncoder:
    def predict(self, pairs):  # noqa: ANN001
        scores = []
        for _, text in pairs:
            scores.append(0.9 if "high" in text else 0.1)
        return scores


def test_rerank_local_orders_by_cross_encoder_score(monkeypatch) -> None:
    monkeypatch.setattr(reranker_module, "_get_cross_encoder", lambda: _FakeCrossEncoder())

    result = rerank("What is attention?", _make_chunks(), top_n=1, reranker_type="local")

    assert len(result) == 1
    assert result[0].text == "high relevance"
    assert result[0].score == 0.9


def test_rerank_falls_back_on_error(monkeypatch) -> None:
    def _broken_encoder():
        raise RuntimeError("model unavailable")

    monkeypatch.setattr(reranker_module, "_get_cross_encoder", _broken_encoder)

    result = rerank("What is attention?", _make_chunks(), top_n=1, reranker_type="local")

    assert len(result) == 1
    assert result[0].text == "high relevance"


def test_rerank_cohere_backend(monkeypatch) -> None:
    class _FakeCohereClient:
        def rerank(self, **kwargs):  # noqa: ANN003
            return SimpleNamespace(
                results=[
                    SimpleNamespace(index=1, relevance_score=0.95),
                    SimpleNamespace(index=0, relevance_score=0.15),
                ]
            )

    fake_cohere = SimpleNamespace(Client=lambda api_key: _FakeCohereClient())
    monkeypatch.setitem(sys.modules, "cohere", fake_cohere)

    result = rerank(
        "What is attention?",
        _make_chunks(),
        top_n=2,
        reranker_type="cohere",
        cohere_api_key="test-key",
    )

    assert result[0].text == "high relevance"
    assert result[1].text == "low relevance"
