from app.ingestion.chunker import chunk_pages
from app.ingestion.parser import PageContent


def test_chunker_returns_single_chunk_for_short_text() -> None:
    pages = [PageContent(page_number=0, text="short text")]
    chunks = chunk_pages(document_id=1, pages=pages, chunk_size=100, chunk_overlap=10)

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].page_number == 0
    assert chunks[0].text == "short text"


def test_chunker_splits_long_text_and_keeps_metadata() -> None:
    long_text = " ".join(["token"] * 1200)
    pages = [PageContent(page_number=3, text=long_text)]
    chunks = chunk_pages(document_id=9, pages=pages, chunk_size=250, chunk_overlap=20)

    assert len(chunks) > 1
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))
    assert all(chunk.page_number == 3 for chunk in chunks)
    assert all(chunk.text.strip() for chunk in chunks)
