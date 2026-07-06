import html
import re
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import structlog

from app.core.config import Settings
from app.core.langfuse_client import create_rag_trace, get_langfuse, truncate_text
from app.db.database import SessionLocal
from app.db.repositories import get_documents_by_ids
from app.rag.generator import generate_answer
from app.rag.hyde import generate_hypothetical_embedding
from app.rag.query_transformer import TransformResult, transform_query
from app.rag.reranker import rerank
from app.rag.retriever import RetrievedChunk, chunks_to_trace_records, retrieve
from app.rag.usage import PipelineUsage, build_pipeline_usage
from app.schemas.query import Source

HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
logger = structlog.get_logger(__name__)
ANSWER_TRACE_MAX_LENGTH = 500


@dataclass(frozen=True)
class PipelineResult:
    answer: str
    sources: list[Source]
    query_used: str
    hyde_used: bool
    query_transform_used: bool
    usage: PipelineUsage


def sanitize_question(question: str, *, max_length: int = 1000) -> str:
    cleaned = html.unescape(question.strip())
    cleaned = HTML_TAG_PATTERN.sub("", cleaned)
    return cleaned[:max_length]


def _resolve_document_filenames(
    user_id: int,
    chunks: list[RetrievedChunk],
    document_filenames: dict[int, str] | None = None,
) -> dict[int, str]:
    filenames = dict(document_filenames or {})
    missing_ids = sorted({chunk.document_id for chunk in chunks} - set(filenames))
    if not missing_ids:
        return filenames

    with SessionLocal() as db:
        documents = get_documents_by_ids(db, user_id, missing_ids)
        filenames.update({document.id: document.original_filename for document in documents})
    return filenames


def _retriever_metadata(
    chunks: list[RetrievedChunk],
    *,
    document_filenames: dict[int, str],
    max_records: int = 20,
) -> dict[str, Any]:
    return {
        "num_chunks_returned": len(chunks),
        "document_ids": sorted({chunk.document_id for chunk in chunks}),
        "chunks": chunks_to_trace_records(
            chunks,
            document_names=document_filenames,
            max_records=max_records,
        ),
    }


def _reranker_metadata(
    chunks: list[RetrievedChunk],
    *,
    document_filenames: dict[int, str],
) -> dict[str, Any]:
    return {
        "output_chunk_count": len(chunks),
        "chunks": chunks_to_trace_records(
            chunks,
            document_names=document_filenames,
        ),
    }


async def run_pipeline(
    *,
    question: str,
    user_id: int,
    settings: Settings,
    use_hyde: bool | None = None,
    use_query_transform: bool | None = None,
    max_sources: int | None = None,
    document_filenames: dict[int, str] | None = None,
    on_step_complete: Callable[[str, Any], None] | None = None,
    trace_id: str | None = None,
) -> PipelineResult:
    sanitized_question = sanitize_question(question)
    effective_trace_id = trace_id or str(uuid.uuid4())
    langfuse = get_langfuse()

    if len(sanitized_question) < 3:
        return PipelineResult(
            answer="Please provide a question with at least 3 characters.",
            sources=[],
            query_used=sanitized_question,
            hyde_used=False,
            query_transform_used=False,
            usage=PipelineUsage.zero(),
        )

    effective_use_hyde = settings.use_hyde_default if use_hyde is None else use_hyde
    effective_use_query_transform = (
        settings.use_query_transform_default if use_query_transform is None else use_query_transform
    )
    top_k = settings.retriever_top_k
    top_n = max_sources if max_sources is not None else settings.reranker_top_n

    trace = create_rag_trace(
        langfuse,
        trace_id=effective_trace_id,
        user_id=user_id,
        metadata={
            "hyde_enabled": effective_use_hyde,
            "query_transform_enabled": effective_use_query_transform,
            "model": settings.generator_model,
            "reranker_type": settings.reranker_type,
        },
    )

    try:
        transform_span = trace.span(
            "query_transformer",
            input_data={"question": truncate_text(sanitized_question)},
        )
        if effective_use_query_transform:
            transform_result = await transform_query(
                sanitized_question,
                api_key=settings.openai_api_key,
            )
            transform_span.end(
                output={"transformed_query": truncate_text(transform_result.transformed_query)},
                metadata={
                    "prompt_tokens": transform_result.prompt_tokens,
                    "completion_tokens": transform_result.completion_tokens,
                    "skipped": False,
                },
            )
        else:
            transform_result = TransformResult(
                original_query=sanitized_question,
                transformed_query=sanitized_question,
            )
            transform_span.end(
                output={"transformed_query": truncate_text(sanitized_question)},
                metadata={"skipped": True},
            )
        if on_step_complete:
            on_step_complete("query_transformer", transform_result)

        hyde_span = trace.span(
            "hyde",
            input_data={"query": truncate_text(transform_result.transformed_query)},
        )
        hyde_result = await generate_hypothetical_embedding(
            transform_result.transformed_query,
            api_key=settings.openai_api_key,
            use_hyde=effective_use_hyde,
        )
        hyde_span.end(
            output={
                "hyde_used": hyde_result.hyde_used,
                "hypothetical_document": (
                    truncate_text(hyde_result.hypothetical_document)
                    if hyde_result.hypothetical_document
                    else None
                ),
            },
            metadata={
                "prompt_tokens": hyde_result.prompt_tokens,
                "completion_tokens": hyde_result.completion_tokens,
                "embedding_tokens": hyde_result.embedding_tokens,
            },
        )
        if on_step_complete:
            on_step_complete("hyde", hyde_result)

        retriever_span = trace.span(
            "retriever",
            input_data={
                "top_k": top_k,
                "user_id": user_id,
            },
        )
        retrieved_chunks = await retrieve(
            user_id=user_id,
            query_vector=hyde_result.query_vector,
            query_text=transform_result.transformed_query,
            qdrant_url=settings.qdrant_url,
            qdrant_api_key=settings.qdrant_api_key,
            top_k=top_k,
        )
        resolved_filenames = _resolve_document_filenames(
            user_id,
            retrieved_chunks,
            document_filenames,
        )
        retriever_span.end(
            output=_retriever_metadata(
                retrieved_chunks,
                document_filenames=resolved_filenames,
                max_records=top_k,
            ),
        )
        if on_step_complete:
            on_step_complete("retriever", retrieved_chunks)

        reranker_span = trace.span(
            "reranker",
            input_data={
                "top_n": top_n,
                "reranker_type": settings.reranker_type,
                "input_chunk_count": len(retrieved_chunks),
            },
        )
        reranked_chunks = rerank(
            transform_result.original_query,
            retrieved_chunks,
            top_n=top_n,
            reranker_type=settings.reranker_type,
            cohere_api_key=settings.cohere_api_key,
        )
        reranker_span.end(
            output=_reranker_metadata(
                reranked_chunks,
                document_filenames=resolved_filenames,
            ),
        )
        if on_step_complete:
            on_step_complete("reranker", reranked_chunks)

        generation_observation = trace.generation(
            "generator",
            input_data={"query": truncate_text(transform_result.original_query)},
            model=settings.generator_model,
        )
        generation_result = await generate_answer(
            transform_result.original_query,
            reranked_chunks,
            api_key=settings.openai_api_key,
            model=settings.generator_model,
        )
        generation_observation.end(
            output={"answer": truncate_text(generation_result.answer, ANSWER_TRACE_MAX_LENGTH)},
            usage_details={
                "prompt_tokens": generation_result.prompt_tokens,
                "completion_tokens": generation_result.completion_tokens,
            },
            metadata={
                "cited_indices": generation_result.cited_indices,
            },
        )
        if on_step_complete:
            on_step_complete("generator", generation_result)

        filenames = resolved_filenames
        sources = _build_sources(
            reranked_chunks,
            cited_indices=generation_result.cited_indices,
            filenames=filenames,
            include_all_when_empty=not generation_result.cited_indices,
        )

        trace.finish(
            output={
                "answer": truncate_text(generation_result.answer, ANSWER_TRACE_MAX_LENGTH),
                "sources_count": len(sources),
                "hyde_used": hyde_result.hyde_used,
            },
        )

        logger.info(
            "pipeline_completed",
            trace_id=effective_trace_id,
            user_id=user_id,
            sources_count=len(sources),
            hyde_used=hyde_result.hyde_used,
            question_preview=truncate_text(sanitized_question, 100),
        )

        usage = build_pipeline_usage(
            transform_prompt=transform_result.prompt_tokens,
            transform_completion=transform_result.completion_tokens,
            hyde_prompt=hyde_result.prompt_tokens,
            hyde_completion=hyde_result.completion_tokens,
            hyde_embedding=hyde_result.embedding_tokens,
            generator_prompt=generation_result.prompt_tokens,
            generator_completion=generation_result.completion_tokens,
            settings=settings,
        )

        return PipelineResult(
            answer=generation_result.answer,
            sources=sources,
            query_used=transform_result.transformed_query,
            hyde_used=hyde_result.hyde_used,
            query_transform_used=effective_use_query_transform,
            usage=usage,
        )
    finally:
        langfuse.flush()


def _build_sources(
    chunks: list[RetrievedChunk],
    *,
    cited_indices: list[int],
    filenames: dict[int, str],
    include_all_when_empty: bool,
) -> list[Source]:
    if not chunks:
        return []

    selected_chunks: list[RetrievedChunk]
    if cited_indices:
        selected: list[RetrievedChunk] = []
        for index in cited_indices:
            if 1 <= index <= len(chunks):
                selected.append(chunks[index - 1])
        selected_chunks = selected or chunks
    elif include_all_when_empty:
        selected_chunks = chunks
    else:
        selected_chunks = chunks

    sources: list[Source] = []
    seen: set[tuple[int, int]] = set()
    for chunk in selected_chunks:
        key = (chunk.document_id, chunk.chunk_index)
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            Source(
                document_id=chunk.document_id,
                original_filename=filenames.get(
                    chunk.document_id,
                    f"document_{chunk.document_id}",
                ),
                page_number=chunk.page_number,
                text=chunk.text,
                score=chunk.score,
            )
        )
    return sources
