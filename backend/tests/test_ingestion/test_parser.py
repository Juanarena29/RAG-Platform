import fitz
import pytest

from app.ingestion.parser import DocumentParsingError, parse_pdf


def _make_pdf_bytes(texts: list[str]) -> bytes:
    doc = fitz.open()
    for text in texts:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


def test_parse_pdf_returns_page_content() -> None:
    pdf_bytes = _make_pdf_bytes(["hello world"])
    pages = parse_pdf(pdf_bytes)

    assert len(pages) == 1
    assert pages[0].page_number == 0
    assert "hello world" in pages[0].text


def test_parse_pdf_two_pages() -> None:
    pdf_bytes = _make_pdf_bytes(["page-one", "page-two"])
    pages = parse_pdf(pdf_bytes)

    assert len(pages) == 2
    assert [page.page_number for page in pages] == [0, 1]


def test_parse_pdf_raises_on_invalid_pdf() -> None:
    with pytest.raises(DocumentParsingError):
        parse_pdf(b"not-a-real-pdf")
