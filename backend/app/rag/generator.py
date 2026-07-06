import json
from dataclasses import dataclass

from openai import AsyncOpenAI

from app.rag.retriever import RetrievedChunk

DEFAULT_GENERATOR_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are a document QA assistant. Answer ONLY using the numbered context fragments.\n"
    "Rules:\n"
    "1. Every factual claim MUST have a [N] citation.\n"
    "2. If the context does not contain the answer, respond: "
    '"I do not have enough information in the uploaded documents."\n'
    "3. Do NOT use outside knowledge. Do NOT infer beyond what is explicitly stated.\n"
    "4. If fragments contradict each other, mention the contradiction.\n"
    "5. cited_indices must list every fragment you used.\n"
    'Respond with JSON: {"answer": "...", "cited_indices": [1, 2]}'
)

@dataclass(frozen=True)
class GeneratorResult:
    answer: str
    cited_indices: list[int]
    prompt_tokens: int = 0
    completion_tokens: int = 0


def _build_context(chunks: list[RetrievedChunk]) -> str:
    sections: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        sections.append(f"[{index}] (page {chunk.page_number})\n{chunk.text}")
    return "\n\n".join(sections)


def _parse_response(content: str) -> GeneratorResult:
    try:
        payload = json.loads(content)
        answer = str(payload.get("answer", "")).strip()
        cited_raw = payload.get("cited_indices", [])
        cited_indices = [int(value) for value in cited_raw if isinstance(value, int | float | str)]
        return GeneratorResult(answer=answer, cited_indices=cited_indices)
    except (json.JSONDecodeError, TypeError, ValueError):
        return GeneratorResult(answer=content.strip(), cited_indices=[])


async def generate_answer(
    query: str,
    chunks: list[RetrievedChunk],
    *,
    api_key: str,
    model: str = DEFAULT_GENERATOR_MODEL,
) -> GeneratorResult:
    if not chunks:
        return GeneratorResult(
            answer=(
                "I do not have enough information in the uploaded documents "
                "to answer that question."
            ),
            cited_indices=[],
        )

    context = _build_context(chunks)
    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model=model,
        temperature=0.0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Question:\n{query}\n\nContext:\n{context}",
            },
        ],
    )

    content = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    prompt_tokens = usage.prompt_tokens if usage else 0
    completion_tokens = usage.completion_tokens if usage else 0
    parsed = _parse_response(content)
    return GeneratorResult(
        answer=parsed.answer,
        cited_indices=parsed.cited_indices,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
