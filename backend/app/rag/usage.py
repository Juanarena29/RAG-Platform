from __future__ import annotations

from dataclasses import dataclass

from app.core.config import Settings


@dataclass(frozen=True)
class PipelineUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    embedding_tokens: int = 0
    estimated_cost_usd: float = 0.0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens + self.embedding_tokens

    @classmethod
    def zero(cls) -> PipelineUsage:
        return cls()


def build_pipeline_usage(
    *,
    transform_prompt: int,
    transform_completion: int,
    hyde_prompt: int,
    hyde_completion: int,
    hyde_embedding: int,
    generator_prompt: int,
    generator_completion: int,
    settings: Settings,
) -> PipelineUsage:
    prompt_tokens = transform_prompt + hyde_prompt + generator_prompt
    completion_tokens = transform_completion + hyde_completion + generator_completion
    embedding_tokens = hyde_embedding
    estimated_cost_usd = estimate_openai_cost_usd(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        embedding_tokens=embedding_tokens,
        settings=settings,
    )
    return PipelineUsage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        embedding_tokens=embedding_tokens,
        estimated_cost_usd=estimated_cost_usd,
    )


def estimate_openai_cost_usd(
    *,
    prompt_tokens: int,
    completion_tokens: int,
    embedding_tokens: int,
    settings: Settings,
) -> float:
    prompt_cost = (prompt_tokens / 1_000_000) * settings.openai_chat_input_price_per_1m
    completion_cost = (completion_tokens / 1_000_000) * settings.openai_chat_output_price_per_1m
    embedding_cost = (embedding_tokens / 1_000_000) * settings.openai_embedding_price_per_1m
    return round(prompt_cost + completion_cost + embedding_cost, 6)
