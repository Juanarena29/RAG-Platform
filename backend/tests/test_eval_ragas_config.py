import os

import pytest

from tests.eval_ragas import (
    ExperimentConfig,
    TokenUsage,
    _build_eval_usage_summary,
    _env_bool,
    _experiment_config,
    _latency_stats,
)


def test_env_bool_parses_common_values() -> None:
    assert _env_bool("EVAL_USE_HYDE", True) is True
    os.environ["EVAL_USE_HYDE"] = "false"
    try:
        assert _env_bool("EVAL_USE_HYDE", True) is False
    finally:
        del os.environ["EVAL_USE_HYDE"]


def test_experiment_config_reads_flags(monkeypatch) -> None:
    monkeypatch.setenv("EVAL_EXPERIMENT_ID", "baseline")
    monkeypatch.setenv("EVAL_USE_QUERY_TRANSFORM", "false")
    monkeypatch.setenv("EVAL_USE_HYDE", "false")
    monkeypatch.setenv("EVAL_MAX_SOURCES", "5")

    config = _experiment_config()

    assert config == ExperimentConfig(
        experiment_id="baseline",
        use_query_transform=False,
        use_hyde=False,
        max_sources=5,
    )


def test_experiment_config_rejects_invalid_id(monkeypatch) -> None:
    monkeypatch.setenv("EVAL_EXPERIMENT_ID", "Bad-Id")
    with pytest.raises(RuntimeError):
        _experiment_config()


def test_latency_stats_computes_percentiles() -> None:
    stats = _latency_stats([100.0, 200.0, 300.0, 400.0])
    assert stats.count == 4
    assert stats.mean_ms == 250.0
    assert stats.p50_ms == 200.0
    assert stats.p95_ms == 400.0


def test_build_eval_usage_summary_aggregates_pipeline_and_judge() -> None:
    rows = [
        {
            "latency_ms": 100.0,
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "embedding_tokens": 2,
                "estimated_cost_usd": 0.001,
            },
        },
        {
            "latency_ms": 300.0,
            "usage": {
                "prompt_tokens": 20,
                "completion_tokens": 10,
                "embedding_tokens": 3,
                "estimated_cost_usd": 0.002,
            },
        },
    ]
    judge = TokenUsage(prompt_tokens=100, completion_tokens=50, estimated_cost_usd=0.05)
    summary = _build_eval_usage_summary(rows, ragas_judge=judge)

    assert summary.pipeline.prompt_tokens == 30
    assert summary.pipeline.completion_tokens == 15
    assert summary.pipeline.embedding_tokens == 5
    assert summary.pipeline.estimated_cost_usd == 0.003
    assert summary.total_estimated_cost_usd == 0.053
    assert summary.latency.mean_ms == 200.0
