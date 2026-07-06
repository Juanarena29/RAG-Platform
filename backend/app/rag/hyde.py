from dataclasses import dataclass

from openai import AsyncOpenAI

from app.ingestion.embedder import EMBEDDING_DIMENSIONS, EMBEDDING_MODEL

HYDE_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are generating a hypothetical document for semantic retrieval.\n"
    f"Write a concise technical paragraph (50-80 words) that would likely answer "
    "the user's question if it appeared in an AI, machine learning, NLP, or software "
    "engineering document.\n\n"
    "Requirements:\n"
    "- Stay faithful to the user's question.\n"
    "- Do not invent alternative meanings for titles, names, or terminology.\n"
    "- If the question mentions a paper title, assume it refers to the actual research "
    "paper rather than another domain.\n"
    "- Use precise technical language and avoid speculation.\n"
    "- Do not mention that this is hypothetical.\n"
    "- Return only the paragraph."
)


@dataclass(frozen=True)
class HydeResult:
    query_vector: list[float]
    hyde_used: bool
    hypothetical_document: str | None = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    embedding_tokens: int = 0


async def _embed_text(client: AsyncOpenAI, text: str) -> tuple[list[float], int]:
    response = await client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
    vector = list(response.data[0].embedding)
    if len(vector) != EMBEDDING_DIMENSIONS:
        msg = f"Expected embedding dimension {EMBEDDING_DIMENSIONS}, got {len(vector)}"
        raise ValueError(msg)
    usage = getattr(response, "usage", None)
    embedding_tokens = usage.total_tokens if usage else 0
    return vector, embedding_tokens


async def generate_hypothetical_embedding(
    query: str,
    *,
    api_key: str,
    use_hyde: bool = True,
    model: str = HYDE_MODEL,
) -> HydeResult:
    normalized_query = query.strip()
    if not normalized_query:
        return HydeResult(query_vector=[], hyde_used=False)

    client = AsyncOpenAI(api_key=api_key)
    prompt_tokens = 0
    completion_tokens = 0
    embedding_tokens = 0

    if not use_hyde:
        vector, embedding_tokens = await _embed_text(client, normalized_query)
        return HydeResult(
            query_vector=vector,
            hyde_used=False,
            embedding_tokens=embedding_tokens,
        )

    try:
        response = await client.chat.completions.create(
            model=model,
            temperature=0.0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": normalized_query},
            ],
        )
        content = response.choices[0].message.content
        hypothetical_document = content.strip() if content else ""
        usage = getattr(response, "usage", None)
        if usage:
            prompt_tokens = usage.prompt_tokens or 0
            completion_tokens = usage.completion_tokens or 0
        if not hypothetical_document:
            vector, embed_tokens = await _embed_text(client, normalized_query)
            embedding_tokens += embed_tokens
            return HydeResult(
                query_vector=vector,
                hyde_used=False,
                embedding_tokens=embedding_tokens,
            )

        vector, embed_tokens = await _embed_text(client, hypothetical_document)
        embedding_tokens += embed_tokens
        return HydeResult(
            query_vector=vector,
            hyde_used=True,
            hypothetical_document=hypothetical_document,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            embedding_tokens=embedding_tokens,
        )
    except Exception:
        vector, embed_tokens = await _embed_text(client, normalized_query)
        embedding_tokens += embed_tokens
        return HydeResult(
            query_vector=vector,
            hyde_used=False,
            embedding_tokens=embedding_tokens,
        )
