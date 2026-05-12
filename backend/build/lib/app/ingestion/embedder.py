from dataclasses import dataclass

from openai import APIConnectionError, AsyncOpenAI, RateLimitError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.ingestion.chunker import Chunk

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


@dataclass(frozen=True)
class EmbeddedChunk:
    document_id: int
    chunk_index: int
    page_number: int
    text: str
    vector: list[float]


@retry(
    wait=wait_exponential(min=1, max=60),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
    reraise=True,
)
async def _embed_batch(client: AsyncOpenAI, texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [list(item.embedding) for item in response.data]


async def embed_chunks(
    chunks: list[Chunk],
    api_key: str,
    batch_size: int = 100,
) -> list[EmbeddedChunk]:
    if not chunks:
        return []

    client = AsyncOpenAI(api_key=api_key)
    embedded_chunks: list[EmbeddedChunk] = []

    for index in range(0, len(chunks), batch_size):
        batch = chunks[index : index + batch_size]
        vectors = await _embed_batch(client, [chunk.text for chunk in batch])
        for chunk, vector in zip(batch, vectors, strict=True):
            embedded_chunks.append(
                EmbeddedChunk(
                    document_id=chunk.document_id,
                    chunk_index=chunk.chunk_index,
                    page_number=chunk.page_number,
                    text=chunk.text,
                    vector=vector,
                )
            )

    return embedded_chunks
