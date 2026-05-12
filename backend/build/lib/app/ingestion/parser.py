import re
from dataclasses import dataclass

import fitz


@dataclass(frozen=True)
class PageContent:
    page_number: int
    text: str


class DocumentParsingError(Exception):
    pass


def _clean_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n")
    normalized = re.sub(r"-\n", "", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def parse_pdf(content: bytes) -> list[PageContent]:
    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except (fitz.FileDataError, ValueError) as exc:
        raise DocumentParsingError("Could not parse PDF content") from exc

    pages: list[PageContent] = []
    try:
        for page_index, page in enumerate(doc):
            text = _clean_text(page.get_text("text"))
            if text:
                pages.append(PageContent(page_number=page_index, text=text))
    finally:
        doc.close()

    if not pages:
        raise DocumentParsingError("No extractable text found in document")

    return pages
