from __future__ import annotations

from functools import lru_cache
from typing import Literal

from app.rag.retriever import RetrievedChunk

LOCAL_RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RerankerType = Literal["local", "cohere"]


@lru_cache(maxsize=1)
def _get_cross_encoder():
    from sentence_transformers import CrossEncoder

    return CrossEncoder(LOCAL_RERANKER_MODEL)


def _rerank_local(query: str, chunks: list[RetrievedChunk], top_n: int) -> list[RetrievedChunk]:
    model = _get_cross_encoder()
    pairs = [(query, chunk.text) for chunk in chunks]
    scores = model.predict(pairs)

    ranked = sorted(
        zip(chunks, scores, strict=True),
        key=lambda item: float(item[1]),
        reverse=True,
    )
    return [
        RetrievedChunk(
            document_id=chunk.document_id,
            chunk_index=chunk.chunk_index,
            page_number=chunk.page_number,
            text=chunk.text,
            user_id=chunk.user_id,
            score=float(score),
        )
        for chunk, score in ranked[:top_n]
    ]


def _rerank_cohere(
    query: str,
    chunks: list[RetrievedChunk],
    top_n: int,
    *,
    api_key: str,
) -> list[RetrievedChunk]:
    import cohere

    client = cohere.Client(api_key=api_key)
    documents = [chunk.text for chunk in chunks]
    response = client.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=documents,
        top_n=min(top_n, len(documents)),
    )

    reranked: list[RetrievedChunk] = []
    for item in response.results:
        chunk = chunks[item.index]
        reranked.append(
            RetrievedChunk(
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                page_number=chunk.page_number,
                text=chunk.text,
                user_id=chunk.user_id,
                score=float(item.relevance_score),
            )
        )
    return reranked


def rerank(
    query: str,
    chunks: list[RetrievedChunk],
    *,
    top_n: int = 5,
    reranker_type: RerankerType = "local",
    cohere_api_key: str | None = None,
) -> list[RetrievedChunk]:
    if not chunks:
        return []

    try:
        if reranker_type == "cohere":
            if not cohere_api_key:
                raise ValueError("COHERE_API_KEY is required when RERANKER_TYPE=cohere")
            return _rerank_cohere(
                query,
                chunks,
                top_n,
                api_key=cohere_api_key,
            )
        return _rerank_local(query, chunks, top_n)
    except Exception:
        fallback = sorted(chunks, key=lambda chunk: chunk.score, reverse=True)
        return fallback[:top_n]
