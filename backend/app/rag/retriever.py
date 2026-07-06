import asyncio
from dataclasses import dataclass
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchText,
    MatchValue,
    TextIndexParams,
    TextIndexType,
)

DEFAULT_RRF_K = 60
DEFAULT_TRACE_TEXT_MAX_LENGTH = 200


@dataclass(frozen=True)
class RetrievedChunk:
    document_id: int
    chunk_index: int
    page_number: int
    text: str
    user_id: int
    score: float


def collection_name_for_user(user_id: int) -> str:
    return f"user_{user_id}"


def chunk_key(document_id: int, chunk_index: int) -> str:
    return f"{document_id}:{chunk_index}"


def chunk_to_trace_record(
    chunk: RetrievedChunk,
    *,
    document_name: str | None = None,
    text_max_length: int = DEFAULT_TRACE_TEXT_MAX_LENGTH,
) -> dict[str, Any]:
    text = chunk.text
    if len(text) > text_max_length:
        text = f"{text[: text_max_length - 3]}..."

    return {
        "document": document_name or f"document_{chunk.document_id}",
        "document_id": chunk.document_id,
        "chunk_id": chunk.chunk_index,
        "page": chunk.page_number,
        "score": round(chunk.score, 4),
        "text": text,
    }


def chunks_to_trace_records(
    chunks: list[RetrievedChunk],
    *,
    document_names: dict[int, str] | None = None,
    max_records: int | None = None,
    text_max_length: int = DEFAULT_TRACE_TEXT_MAX_LENGTH,
) -> list[dict[str, Any]]:
    names = document_names or {}
    selected = chunks if max_records is None else chunks[:max_records]
    return [
        chunk_to_trace_record(
            chunk,
            document_name=names.get(chunk.document_id),
            text_max_length=text_max_length,
        )
        for chunk in selected
    ]


def reciprocal_rank_fusion(
    rankings: list[list[str]],
    *,
    k: int = DEFAULT_RRF_K,
) -> dict[str, float]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item_id in enumerate(ranking, start=1):
            scores[item_id] = scores.get(item_id, 0.0) + (1.0 / (k + rank))
    return scores


def _user_filter(user_id: int) -> Filter:
    return Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id),
            )
        ]
    )


def _point_to_chunk(point: object, *, score: float) -> RetrievedChunk | None:
    payload = getattr(point, "payload", None) or {}
    if not payload:
        return None

    try:
        return RetrievedChunk(
            document_id=int(payload["document_id"]),
            chunk_index=int(payload["chunk_index"]),
            page_number=int(payload["page_number"]),
            text=str(payload["text"]),
            user_id=int(payload["user_id"]),
            score=score,
        )
    except (KeyError, TypeError, ValueError):
        return None


def _ensure_text_index(client: QdrantClient, collection_name: str) -> None:
    if not client.collection_exists(collection_name):
        return

    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name="text",
            field_schema=TextIndexParams(
                type=TextIndexType.TEXT,
                tokenizer="word",
                min_token_len=2,
                lowercase=True,
            ),
        )
    except Exception:
        # Index may already exist or collection may be empty.
        pass


def _dense_search(
    client: QdrantClient,
    *,
    collection_name: str,
    query_vector: list[float],
    user_id: int,
    top_k: int,
) -> list[RetrievedChunk]:
    if not query_vector or not client.collection_exists(collection_name):
        return []

    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=_user_filter(user_id),
        limit=top_k,
        with_payload=True,
    )

    chunks: list[RetrievedChunk] = []
    for point in response.points:
        chunk = _point_to_chunk(point, score=float(point.score or 0.0))
        if chunk is not None:
            chunks.append(chunk)
    return chunks


def _fulltext_search(
    client: QdrantClient,
    *,
    collection_name: str,
    query_text: str,
    user_id: int,
    top_k: int,
) -> list[RetrievedChunk]:
    if not query_text.strip() or not client.collection_exists(collection_name):
        return []

    _ensure_text_index(client, collection_name)

    text_filter = Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id),
            ),
            FieldCondition(
                key="text",
                match=MatchText(text=query_text),
            ),
        ]
    )

    try:
        response = client.query_points(
            collection_name=collection_name,
            query_filter=text_filter,
            limit=top_k,
            with_payload=True,
        )
        points = response.points
    except Exception:
        records, _ = client.scroll(
            collection_name=collection_name,
            scroll_filter=text_filter,
            limit=top_k,
            with_payload=True,
        )
        points = records

    chunks: list[RetrievedChunk] = []
    for rank, point in enumerate(points, start=1):
        chunk = _point_to_chunk(point, score=1.0 / rank)
        if chunk is not None:
            chunks.append(chunk)
    return chunks


def _merge_with_rrf(
    dense_chunks: list[RetrievedChunk],
    fulltext_chunks: list[RetrievedChunk],
    *,
    rrf_k: int = DEFAULT_RRF_K,
) -> list[RetrievedChunk]:
    dense_ranking = [
        chunk_key(chunk.document_id, chunk.chunk_index) for chunk in dense_chunks
    ]
    fulltext_ranking = [
        chunk_key(chunk.document_id, chunk.chunk_index) for chunk in fulltext_chunks
    ]
    fused_scores = reciprocal_rank_fusion([dense_ranking, fulltext_ranking], k=rrf_k)

    chunk_lookup: dict[str, RetrievedChunk] = {}
    for chunk in dense_chunks + fulltext_chunks:
        key = chunk_key(chunk.document_id, chunk.chunk_index)
        chunk_lookup[key] = chunk

    sorted_keys = sorted(
        fused_scores.keys(),
        key=lambda key: fused_scores[key],
        reverse=True,
    )
    merged: list[RetrievedChunk] = []
    for key in sorted_keys:
        base = chunk_lookup[key]
        merged.append(
            RetrievedChunk(
                document_id=base.document_id,
                chunk_index=base.chunk_index,
                page_number=base.page_number,
                text=base.text,
                user_id=base.user_id,
                score=fused_scores[key],
            )
        )
    return merged


async def retrieve(
    *,
    user_id: int,
    query_vector: list[float],
    query_text: str,
    qdrant_url: str,
    qdrant_api_key: str | None,
    top_k: int = 20,
    rrf_k: int = DEFAULT_RRF_K,
) -> list[RetrievedChunk]:
    if not query_vector:
        return []

    collection_name = collection_name_for_user(user_id)
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    dense_chunks, fulltext_chunks = await asyncio.gather(
        asyncio.to_thread(
            _dense_search,
            client,
            collection_name=collection_name,
            query_vector=query_vector,
            user_id=user_id,
            top_k=top_k,
        ),
        asyncio.to_thread(
            _fulltext_search,
            client,
            collection_name=collection_name,
            query_text=query_text,
            user_id=user_id,
            top_k=top_k,
        ),
    )

    merged = _merge_with_rrf(dense_chunks, fulltext_chunks, rrf_k=rrf_k)
    return merged[:top_k]
