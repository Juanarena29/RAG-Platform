import asyncio
from dataclasses import dataclass

from app.core.config import Settings
from app.rag.pipeline import (
    PipelineResult,
    _retriever_metadata,
    run_pipeline,
    sanitize_question,
)
from app.rag.query_transformer import TransformResult
from app.rag.retriever import RetrievedChunk
from app.rag.usage import PipelineUsage


@dataclass(frozen=True)
class _FakeHydeResult:
    query_vector: list[float]
    hyde_used: bool
    hypothetical_document: str | None = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    embedding_tokens: int = 0


@dataclass(frozen=True)
class _FakeGeneratorResult:
    answer: str
    cited_indices: list[int]
    prompt_tokens: int = 0
    completion_tokens: int = 0


def test_sanitize_question_strips_html() -> None:
    assert sanitize_question("  <b>What is RLHF?</b>  ") == "What is RLHF?"


def test_run_pipeline_orchestrates_all_steps(monkeypatch) -> None:
    async def _fake_transform(query: str, *, api_key: str, model: str = "gpt-4o-mini"):
        return TransformResult(original_query=query, transformed_query=f"transformed: {query}")

    async def _fake_hyde(
        query: str,
        *,
        api_key: str,
        use_hyde: bool = True,
        model: str = "gpt-4o-mini",
    ):
        return _FakeHydeResult(query_vector=[0.1] * 1536, hyde_used=use_hyde)

    async def _fake_retrieve(**kwargs):  # noqa: ANN003
        return [
            RetrievedChunk(
                document_id=1,
                chunk_index=0,
                page_number=1,
                text="chunk text",
                user_id=kwargs["user_id"],
                score=0.8,
            )
        ]

    def _fake_rerank(query, chunks, **kwargs):  # noqa: ANN001, ANN003
        return chunks

    async def _fake_generate(query, chunks, *, api_key: str, model: str = "gpt-4o-mini"):
        return _FakeGeneratorResult(answer="Final answer [1]", cited_indices=[1])

    monkeypatch.setattr("app.rag.pipeline.transform_query", _fake_transform)
    monkeypatch.setattr("app.rag.pipeline.generate_hypothetical_embedding", _fake_hyde)
    monkeypatch.setattr("app.rag.pipeline.retrieve", _fake_retrieve)
    monkeypatch.setattr("app.rag.pipeline.rerank", _fake_rerank)
    monkeypatch.setattr("app.rag.pipeline.generate_answer", _fake_generate)

    settings = Settings(openai_api_key="test-key")
    result = asyncio.run(
        run_pipeline(
            question="What is attention?",
            user_id=42,
            settings=settings,
            document_filenames={1: "paper.pdf"},
        )
    )

    assert isinstance(result, PipelineResult)
    assert result.answer == "Final answer [1]"
    assert result.query_used == "transformed: What is attention?"
    assert result.hyde_used is True
    assert len(result.sources) == 1
    assert result.sources[0].original_filename == "paper.pdf"
    assert isinstance(result.usage, PipelineUsage)
    assert result.usage.total_tokens == 0


def test_run_pipeline_skips_query_transform_when_disabled(monkeypatch) -> None:
    transform_called = False

    async def _fake_transform(query: str, *, api_key: str, model: str = "gpt-4o-mini"):
        nonlocal transform_called
        transform_called = True
        return TransformResult(original_query=query, transformed_query=f"transformed: {query}")

    async def _fake_hyde(
        query: str,
        *,
        api_key: str,
        use_hyde: bool = True,
        model: str = "gpt-4o-mini",
    ):
        assert query == "What is attention?"
        return _FakeHydeResult(query_vector=[0.1] * 1536, hyde_used=use_hyde)

    async def _fake_retrieve(**kwargs):  # noqa: ANN003
        return [
            RetrievedChunk(
                document_id=1,
                chunk_index=0,
                page_number=1,
                text="chunk text",
                user_id=kwargs["user_id"],
                score=0.8,
            )
        ]

    def _fake_rerank(query, chunks, **kwargs):  # noqa: ANN001, ANN003
        return chunks

    async def _fake_generate(query, chunks, *, api_key: str, model: str = "gpt-4o-mini"):
        return _FakeGeneratorResult(answer="Final answer [1]", cited_indices=[1])

    monkeypatch.setattr("app.rag.pipeline.transform_query", _fake_transform)
    monkeypatch.setattr("app.rag.pipeline.generate_hypothetical_embedding", _fake_hyde)
    monkeypatch.setattr("app.rag.pipeline.retrieve", _fake_retrieve)
    monkeypatch.setattr("app.rag.pipeline.rerank", _fake_rerank)
    monkeypatch.setattr("app.rag.pipeline.generate_answer", _fake_generate)

    settings = Settings(openai_api_key="test-key")
    result = asyncio.run(
        run_pipeline(
            question="What is attention?",
            user_id=42,
            settings=settings,
            use_query_transform=False,
            use_hyde=False,
        )
    )

    assert transform_called is False
    assert result.query_used == "What is attention?"
    assert result.query_transform_used is False
    assert result.hyde_used is False


def test_retriever_metadata_includes_chunk_records() -> None:
    chunks = [
        RetrievedChunk(
            document_id=1,
            chunk_index=17,
            page_number=3,
            text="Large language models often struggle with long contexts.",
            user_id=42,
            score=0.01639,
        )
    ]

    metadata = _retriever_metadata(
        chunks,
        document_filenames={1: "Lost in the Middle.pdf"},
    )

    assert metadata["num_chunks_returned"] == 1
    assert metadata["document_ids"] == [1]
    assert metadata["chunks"][0]["document"] == "Lost in the Middle.pdf"
    assert metadata["chunks"][0]["chunk_id"] == 17
    assert metadata["chunks"][0]["page"] == 3


def test_run_pipeline_rejects_short_questions() -> None:
    settings = Settings(openai_api_key="test-key")
    result = asyncio.run(
        run_pipeline(
            question="ab",
            user_id=1,
            settings=settings,
        )
    )

    assert result.sources == []
    assert "at least 3 characters" in result.answer
    assert result.usage.total_tokens == 0
