from types import SimpleNamespace

from app.rag.retriever import (
    RetrievedChunk,
    _dense_search,
    _fulltext_search,
    _merge_with_rrf,
    chunk_to_trace_record,
    reciprocal_rank_fusion,
)


def _make_point(
    *,
    document_id: int,
    chunk_index: int,
    page_number: int,
    text: str,
    user_id: int,
    score: float | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        score=score,
        payload={
            "document_id": document_id,
            "chunk_index": chunk_index,
            "page_number": page_number,
            "text": text,
            "user_id": user_id,
        },
    )


class _FakeQdrantClient:
    def __init__(self) -> None:
        self.collection_exists_result = True
        self.query_points_calls: list[dict] = []
        self.scroll_calls: list[dict] = []

    def collection_exists(self, collection_name: str) -> bool:
        return self.collection_exists_result

    def create_payload_index(self, **kwargs):  # noqa: ANN003
        return None

    def query_points(self, **kwargs):  # noqa: ANN003
        self.query_points_calls.append(kwargs)
        query_filter = kwargs["query_filter"]
        user_id = query_filter.must[0].match.value
        is_dense = isinstance(kwargs.get("query"), list)
        return SimpleNamespace(
            points=[
                _make_point(
                    document_id=1 if is_dense else 2,
                    chunk_index=0,
                    page_number=1 if is_dense else 2,
                    text="dense chunk" if is_dense else "keyword chunk",
                    user_id=user_id,
                    score=0.91 if is_dense else None,
                )
            ]
        )

    def scroll(self, **kwargs):  # noqa: ANN003
        self.scroll_calls.append(kwargs)
        scroll_filter = kwargs["scroll_filter"]
        user_id = scroll_filter.must[0].match.value
        return (
            [
                _make_point(
                    document_id=2,
                    chunk_index=0,
                    page_number=2,
                    text="keyword chunk",
                    user_id=user_id,
                )
            ],
            None,
        )


def test_reciprocal_rank_fusion_orders_top_ranked_item_first() -> None:
    scores = reciprocal_rank_fusion(
        [
            ["2:0", "1:0"],
            ["2:0", "1:0"],
        ]
    )

    assert scores["2:0"] > scores["1:0"]


def test_dense_search_applies_user_filter() -> None:
    client = _FakeQdrantClient()

    chunks = _dense_search(
        client,
        collection_name="user_7",
        query_vector=[0.1] * 1536,
        user_id=7,
        top_k=5,
    )

    assert len(chunks) == 1
    assert client.query_points_calls[0]["query_filter"].must[0].match.value == 7
    assert chunks[0].document_id == 1


def test_fulltext_search_applies_user_filter() -> None:
    client = _FakeQdrantClient()

    chunks = _fulltext_search(
        client,
        collection_name="user_7",
        query_text="attention mechanism",
        user_id=7,
        top_k=5,
    )

    assert len(chunks) == 1
    assert client.query_points_calls[0]["query_filter"].must[0].match.value == 7
    assert chunks[0].document_id == 2


def test_merge_with_rrf_combines_legs() -> None:
    dense = [
        RetrievedChunk(
            document_id=1,
            chunk_index=0,
            page_number=1,
            text="dense",
            user_id=1,
            score=0.9,
        )
    ]
    fulltext = [
        RetrievedChunk(
            document_id=2,
            chunk_index=0,
            page_number=2,
            text="keyword",
            user_id=1,
            score=0.5,
        )
    ]

    merged = _merge_with_rrf(dense, fulltext)

    assert len(merged) == 2
    assert merged[0].score >= merged[1].score


def test_chunk_to_trace_record_includes_document_metadata() -> None:
    chunk = RetrievedChunk(
        document_id=7,
        chunk_index=17,
        page_number=3,
        text="Large language models often struggle with long contexts.",
        user_id=1,
        score=0.01639,
    )

    record = chunk_to_trace_record(
        chunk,
        document_name="Lost in the Middle.pdf",
    )

    assert record == {
        "document": "Lost in the Middle.pdf",
        "document_id": 7,
        "chunk_id": 17,
        "page": 3,
        "score": 0.0164,
        "text": "Large language models often struggle with long contexts.",
    }
