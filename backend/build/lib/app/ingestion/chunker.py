from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ingestion.parser import PageContent


@dataclass(frozen=True)
class Chunk:
    document_id: int
    chunk_index: int
    page_number: int
    text: str


def chunk_pages(
    document_id: int,
    pages: list[PageContent],
    chunk_size: int = 2000,
    chunk_overlap: int = 100,
) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
    )

    chunks: list[Chunk] = []
    chunk_index = 0
    for page in pages:
        page_chunks = splitter.split_text(page.text)
        for chunk_text in page_chunks:
            normalized_text = chunk_text.strip()
            if not normalized_text:
                continue
            chunks.append(
                Chunk(
                    document_id=document_id,
                    chunk_index=chunk_index,
                    page_number=page.page_number,
                    text=normalized_text,
                )
            )
            chunk_index += 1

    return chunks
