from app.core.config import Settings
from app.rag.usage import PipelineUsage, build_pipeline_usage, estimate_openai_cost_usd


def test_pipeline_usage_total_tokens() -> None:
    usage = PipelineUsage(prompt_tokens=100, completion_tokens=50, embedding_tokens=25)
    assert usage.total_tokens == 175


def test_estimate_openai_cost_usd_uses_settings_pricing() -> None:
    settings = Settings(
        openai_chat_input_price_per_1m=0.15,
        openai_chat_output_price_per_1m=0.60,
        openai_embedding_price_per_1m=0.02,
    )
    cost = estimate_openai_cost_usd(
        prompt_tokens=1_000_000,
        completion_tokens=1_000_000,
        embedding_tokens=1_000_000,
        settings=settings,
    )
    assert cost == 0.77


def test_build_pipeline_usage_aggregates_stages() -> None:
    settings = Settings()
    usage = build_pipeline_usage(
        transform_prompt=10,
        transform_completion=5,
        hyde_prompt=20,
        hyde_completion=15,
        hyde_embedding=100,
        generator_prompt=200,
        generator_completion=80,
        settings=settings,
    )
    assert usage.prompt_tokens == 230
    assert usage.completion_tokens == 100
    assert usage.embedding_tokens == 100
    assert usage.total_tokens == 430
    assert usage.estimated_cost_usd > 0
