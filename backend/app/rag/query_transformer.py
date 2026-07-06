from dataclasses import dataclass

from openai import AsyncOpenAI

TRANSFORM_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "You rewrite user questions to improve semantic retrieval from technical AI and "
    "machine learning documents.\n\n"
    "Guidelines:\n"
    "- Preserve the original meaning of the question.\n"
    "- Expand abbreviations when appropriate (e.g., RAG → Retrieval-Augmented Generation).\n"
    "- Clarify ambiguous wording without changing the user's intent.\n"
    "- If the question mentions a paper title, method, model, dataset, or algorithm, "
    "preserve its canonical name exactly and, when helpful, include its technical context.\n"
    "- Do NOT reinterpret titles or names into another domain.\n"
    "- Remove conversational filler.\n"
    "- Keep the rewritten question concise (one sentence).\n"
    "- Return only the rewritten question."
)


@dataclass(frozen=True)
class TransformResult:
    original_query: str
    transformed_query: str
    prompt_tokens: int = 0
    completion_tokens: int = 0


async def transform_query(
    query: str,
    *,
    api_key: str,
    model: str = TRANSFORM_MODEL,
) -> TransformResult:
    original_query = query.strip()
    if not original_query:
        return TransformResult(original_query=original_query, transformed_query=original_query)

    client = AsyncOpenAI(api_key=api_key)
    prompt_tokens = 0
    completion_tokens = 0
    try:
        response = await client.chat.completions.create(
            model=model,
            temperature=0.0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": original_query},
            ],
        )
        content = response.choices[0].message.content
        transformed_query = content.strip() if content else original_query
        if not transformed_query:
            transformed_query = original_query
        usage = getattr(response, "usage", None)
        if usage:
            prompt_tokens = usage.prompt_tokens or 0
            completion_tokens = usage.completion_tokens or 0
    except Exception:
        transformed_query = original_query

    return TransformResult(
        original_query=original_query,
        transformed_query=transformed_query,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
