"""RAGAS evaluation against a live /query endpoint with arXiv-style QA pairs."""

from __future__ import annotations

import json
import math
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
from datasets import Dataset
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas import evaluate
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness

from app.core.config import get_settings
from app.rag.usage import estimate_openai_cost_usd

METRIC_NAMES = ("faithfulness", "answer_relevancy", "context_precision", "context_recall")
DEFAULT_FAITHFULNESS_THRESHOLD = 0.7
ANSWER_PREVIEW_LENGTH = 300
CONTEXT_PREVIEW_LENGTH = 200
EXPERIMENT_ID_PATTERN = re.compile(r"^[a-z0-9_]+$")


@dataclass(frozen=True)
class ExperimentConfig:
    experiment_id: str
    use_query_transform: bool
    use_hyde: bool
    max_sources: int = 5


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    embedding_tokens: int = 0
    estimated_cost_usd: float = 0.0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens + self.embedding_tokens

    @classmethod
    def from_payload(cls, payload: dict[str, Any] | None) -> TokenUsage:
        if not payload:
            return cls()
        return cls(
            prompt_tokens=int(payload.get("prompt_tokens", 0)),
            completion_tokens=int(payload.get("completion_tokens", 0)),
            embedding_tokens=int(payload.get("embedding_tokens", 0)),
            estimated_cost_usd=float(payload.get("estimated_cost_usd", 0.0)),
        )

    def __add__(self, other: TokenUsage) -> TokenUsage:
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            embedding_tokens=self.embedding_tokens + other.embedding_tokens,
            estimated_cost_usd=round(self.estimated_cost_usd + other.estimated_cost_usd, 6),
        )


@dataclass(frozen=True)
class LatencyStats:
    count: int
    total_ms: float
    mean_ms: float
    p50_ms: float
    p95_ms: float


@dataclass(frozen=True)
class EvalUsageSummary:
    pipeline: TokenUsage
    ragas_judge: TokenUsage
    total_estimated_cost_usd: float
    latency: LatencyStats

SAMPLE_QA_PAIRS: list[dict[str, str]] = [
    {
        "question": "What is the attention mechanism in transformers?",
        "ground_truth": (
            "Attention allows each token to weigh information from all other tokens, enabling "
            "the model to capture relationships regardless of their distance in the sequence."
        ),
    },
    {
        "question": "How does multi-head attention work?",
        "ground_truth": (
            "Multi-head attention performs several attention operations in parallel using "
            "different learned projections, then concatenates their outputs to capture "
            "different types of relationships."
        ),
    },
    {
        "question": "What problem does self-attention solve compared to recurrent networks?",
        "ground_truth": (
            "Self-attention reduces sequential computation by allowing every position to attend "
            "directly to every other position with a constant number of sequential operations, "
            "making it easier to model long-range dependencies than recurrent networks."
        ),  
    },
    {
        "question": "Why are positional encodings required in transformers?",
        "ground_truth": (
            "Positional encodings provide information about token order because the attention "
            "mechanism itself is permutation invariant."
        ),
    },
    {
        "question": "What is the purpose of feed-forward networks in transformer blocks?",
        "ground_truth": (
            "Feed-forward networks apply nonlinear transformations independently to each "
            "position after attention, increasing the model's representational capacity."
        ),
    },
    {
        "question": "Why is layer normalization important in transformers?",
        "ground_truth": (
            "Layer normalization is applied together with residual connections around each "
            "sub-layer to stabilize optimization, improve convergence, and enable effective "
            "training of deep transformer models."
        ),
    },
    {
        "question": "What is scaled dot-product attention?",
        "ground_truth": (
            "Scaled dot-product attention computes softmax(QK^T divided by the square root of "
            "the key dimension) multiplied by V to obtain weighted value representations."
        ),
    },
    {
        "question": "Why are transformers more parallelizable than recurrent neural networks?",
        "ground_truth": (
            "Transformers process all sequence positions simultaneously instead of sequentially, "
            "allowing efficient parallel computation during training."
        ),
    },
    {
        "question": "What is retrieval-augmented generation?",
        "ground_truth": (
            "Retrieval-augmented generation combines document retrieval with text generation, "
            "conditioning the model on retrieved evidence to improve factual accuracy."
        ),
    },
    {
        "question": "How does RAG improve factual knowledge?",
        "ground_truth": (
            "RAG retrieves relevant external documents at inference time so generation is "
            "grounded in retrieved evidence instead of relying only on model parameters."
        ),
    },
    {
        "question": "How are retrieved documents used in RAG?",
        "ground_truth": (
            "Retrieved documents are provided as additional context to the generator, allowing "
            "it to produce answers conditioned on external knowledge."
        ),
    },
    {
        "question": "What is top-k retrieval in RAG?",
        "ground_truth": (
            "Top-k retrieval selects the highest-ranked documents for a query and supplies "
            "them to the generation model as supporting context."
        ),
    },
    {
        "question": "What is HyDE in information retrieval?",
        "ground_truth": (
            "HyDE improves retrieval by first generating a hypothetical document and then "
            "embedding that document rather than the original query. This decomposes dense "
            "retrieval into a generation step followed by document-document similarity, "
            "producing embeddings that better match relevant passages."
        ),
    },
    {
        "question": "Why can HyDE improve zero-shot retrieval?",
        "ground_truth": (
            "HyDE transforms the query into an answer-like document whose embedding better "
            "matches relevant passages, improving retrieval without relevance labels."
        ),
    },
    {
        "question": "What is the main advantage of HyDE over directly embedding the query?",
        "ground_truth": (
            "HyDE creates a richer semantic representation of the user's intent by embedding "
            "a generated hypothetical document instead of the short query itself."
        ),
    },
    {
        "question": "What challenge does the 'Lost in the Middle' paper identify?",
        "ground_truth": (
            "The paper shows that long-context language models often fail to use relevant "
            "information effectively when it appears in the middle of the provided context, "
            "performing better when the information is located near the beginning or end."
        ),
    },
    {
        "question": "How does document position affect long-context language models?",
        "ground_truth": (
            "Language models tend to perform better when relevant information appears near "
            "the beginning or end of the context than when it is located in the middle."
        ),
    },
    {
        "question": "Why are long context windows not always sufficient for question answering?",
        "ground_truth": (
            "Simply increasing context length does not guarantee effective use of all "
            "information because models may fail to attend to relevant content in the middle."
        ),
    },
    {
        "question": "What is the main contribution of the Transformer architecture?",
        "ground_truth": (
            "The Transformer replaces recurrence with attention mechanisms, enabling highly "
            "parallel sequence modeling while achieving strong performance on language tasks."
        ),
    },
    {
        "question": "How does attention enable modeling long-range dependencies?",
        "ground_truth": (
            "Attention directly connects every token with every other token, allowing "
            "dependencies to be modeled regardless of sequence distance."
        ),
    },
    {
        "question": "Why is retrieval useful even for very large language models?",
        "ground_truth": (
            "Retrieval provides access to external knowledge at inference time, improving "
            "factual accuracy without requiring all knowledge to be stored in model parameters."
        ),
    },
    {
        "question": "How do transformers enable retrieval-augmented generation systems?",
        "ground_truth": (
            "Transformer architectures can condition generation on retrieved documents using "
            "attention, allowing external evidence to influence generated responses."
        ),
    },
    {
        "question": "What limitation of parametric knowledge motivates retrieval?",
        "ground_truth": (
            "Knowledge stored only in model parameters can become outdated or incomplete, "
            "whereas retrieval provides access to current external information."
        ),
    },
    {
        "question": "Why can retrieval reduce hallucinations?",
        "ground_truth": (
            "Retrieval reduces hallucinations by grounding generation on relevant external "
            "documents instead of relying only on knowledge stored in model parameters, allowing "
            "responses to be supported by retrieved evidence."
        ),
    },
    {
        "question": "How do retrieval and long-context models complement each other?",
        "ground_truth": (
            "Retrieval narrows the search space by selecting the most relevant documents, while "
            "long-context language models reason over that retrieved evidence. Together they "
            "reduce the need to process unnecessarily large contexts while improving access to "
            "relevant information."
        ),
    },
]


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    root_env = Path(__file__).resolve().parents[2] / ".env"
    if root_env.exists():
        load_dotenv(root_env)


def _env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        msg = f"Missing required environment variable: {name}"
        raise RuntimeError(msg)
    return value


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def _experiment_config() -> ExperimentConfig:
    experiment_id = os.getenv("EVAL_EXPERIMENT_ID", "").strip().lower()
    if not experiment_id:
        experiment_id = datetime.now(UTC).strftime("run_%Y%m%d_%H%M%S")
    if not EXPERIMENT_ID_PATTERN.match(experiment_id):
        msg = (
            "EVAL_EXPERIMENT_ID must contain only lowercase letters, numbers, and underscores"
        )
        raise RuntimeError(msg)

    return ExperimentConfig(
        experiment_id=experiment_id,
        use_query_transform=_env_bool("EVAL_USE_QUERY_TRANSFORM", True),
        use_hyde=_env_bool("EVAL_USE_HYDE", True),
        max_sources=_env_int("EVAL_MAX_SOURCES", 5),
    )


def _openai_api_key() -> str:
    api_key = _env("OPENAI_API_KEY")
    if api_key in {"sk-...", "sk-your-key"} or api_key.startswith("sk-...."):
        msg = (
            "OPENAI_API_KEY looks like a placeholder. "
            "Unset it in your shell ($env:OPENAI_API_KEY=$null) so .env is used, "
            "or export the real key."
        )
        raise RuntimeError(msg)
    return api_key


def _metrics_from_result(result: Any) -> dict[str, float]:
    repr_dict = getattr(result, "_repr_dict", None)
    if repr_dict is not None:
        metrics: dict[str, float] = {}
        for name, value in repr_dict.items():
            if value is None or (isinstance(value, float) and math.isnan(value)):
                continue
            metrics[name] = float(value)
        if not metrics:
            msg = (
                "RAGAS returned no metric scores. "
                "This usually means OPENAI_API_KEY is invalid for the evaluator LLM."
            )
            raise RuntimeError(msg)
        return metrics

    if hasattr(result, "items"):
        return {key: float(value) for key, value in result.items()}

    raise TypeError(f"Unexpected evaluation result type: {type(result)!r}")


def _preview_text(text: str, max_length: int) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_length:
        return cleaned
    return f"{cleaned[: max_length - 3]}..."


def _score_or_none(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return float(value)


def _per_row_scores(result: Any) -> list[dict[str, float | None]]:
    scores_dict = getattr(result, "_scores_dict", None)
    if scores_dict is None:
        scores_dict = {name: result[name] for name in METRIC_NAMES if hasattr(result, "__getitem__")}

    row_count = len(next(iter(scores_dict.values()))) if scores_dict else 0
    per_row: list[dict[str, float | None]] = []
    for index in range(row_count):
        per_row.append(
            {
                name: _score_or_none(scores_dict.get(name, [None] * row_count)[index])
                for name in METRIC_NAMES
            }
        )
    return per_row


def _build_detail_records(
    rows: list[dict[str, Any]],
    per_row_scores: list[dict[str, float | None]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (row, scores) in enumerate(zip(rows, per_row_scores, strict=True), start=1):
        records.append(
            {
                "index": index,
                "question": row["question"],
                "answer": row["answer"],
                "ground_truth": row["ground_truth"],
                "trace_id": row.get("trace_id"),
                "latency_ms": row.get("latency_ms"),
                "usage": row.get("usage"),
                "context_count": len(row.get("contexts", [])),
                "scores": scores,
            }
        )
    return records


def _faithfulness_threshold() -> float:
    return float(os.getenv("EVAL_FAITHFULNESS_THRESHOLD", str(DEFAULT_FAITHFULNESS_THRESHOLD)))


def _latency_stats(latencies_ms: list[float]) -> LatencyStats:
    if not latencies_ms:
        return LatencyStats(count=0, total_ms=0.0, mean_ms=0.0, p50_ms=0.0, p95_ms=0.0)

    sorted_latencies = sorted(latencies_ms)
    count = len(sorted_latencies)
    total_ms = sum(sorted_latencies)
    mean_ms = total_ms / count
    p50_index = max(0, int(math.ceil(0.5 * count)) - 1)
    p95_index = max(0, int(math.ceil(0.95 * count)) - 1)
    return LatencyStats(
        count=count,
        total_ms=round(total_ms, 2),
        mean_ms=round(mean_ms, 2),
        p50_ms=round(sorted_latencies[p50_index], 2),
        p95_ms=round(sorted_latencies[p95_index], 2),
    )


def _aggregate_pipeline_usage(rows: list[dict[str, Any]]) -> TokenUsage:
    total = TokenUsage()
    for row in rows:
        total += TokenUsage.from_payload(row.get("usage"))
    return total


def _build_eval_usage_summary(
    rows: list[dict[str, Any]],
    *,
    ragas_judge: TokenUsage,
) -> EvalUsageSummary:
    pipeline = _aggregate_pipeline_usage(rows)
    latencies = [float(row["latency_ms"]) for row in rows if row.get("latency_ms") is not None]
    total_cost = round(pipeline.estimated_cost_usd + ragas_judge.estimated_cost_usd, 6)
    return EvalUsageSummary(
        pipeline=pipeline,
        ragas_judge=ragas_judge,
        total_estimated_cost_usd=total_cost,
        latency=_latency_stats(latencies),
    )


def _usage_to_dict(usage: TokenUsage) -> dict[str, float | int]:
    return {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "embedding_tokens": usage.embedding_tokens,
        "total_tokens": usage.total_tokens,
        "estimated_cost_usd": usage.estimated_cost_usd,
    }


def _eval_usage_to_dict(summary: EvalUsageSummary) -> dict[str, Any]:
    return {
        "pipeline": _usage_to_dict(summary.pipeline),
        "ragas_judge": _usage_to_dict(summary.ragas_judge),
        "total_estimated_cost_usd": summary.total_estimated_cost_usd,
        "latency_ms": {
            "count": summary.latency.count,
            "total": summary.latency.total_ms,
            "mean": summary.latency.mean_ms,
            "p50": summary.latency.p50_ms,
            "p95": summary.latency.p95_ms,
        },
    }


def _usage_markdown_lines(summary: EvalUsageSummary) -> list[str]:
    return [
        "## Usage",
        "",
        "### Pipeline (/query)",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| prompt_tokens | {summary.pipeline.prompt_tokens} |",
        f"| completion_tokens | {summary.pipeline.completion_tokens} |",
        f"| embedding_tokens | {summary.pipeline.embedding_tokens} |",
        f"| total_tokens | {summary.pipeline.total_tokens} |",
        f"| estimated_cost_usd | ${summary.pipeline.estimated_cost_usd:.6f} |",
        "",
        "### RAGAS judge",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| prompt_tokens | {summary.ragas_judge.prompt_tokens} |",
        f"| completion_tokens | {summary.ragas_judge.completion_tokens} |",
        f"| embedding_tokens | {summary.ragas_judge.embedding_tokens} |",
        f"| total_tokens | {summary.ragas_judge.total_tokens} |",
        f"| estimated_cost_usd | ${summary.ragas_judge.estimated_cost_usd:.6f} |",
        "",
        "### Totals",
        "",
        f"- Total estimated cost (pipeline + judge): `${summary.total_estimated_cost_usd:.6f}`",
        f"- Query latency mean: `{summary.latency.mean_ms:.0f} ms`",
        f"- Query latency p50: `{summary.latency.p50_ms:.0f} ms`",
        f"- Query latency p95: `{summary.latency.p95_ms:.0f} ms`",
        "",
    ]


def query_rag(
    client: httpx.Client,
    *,
    base_url: str,
    api_key: str,
    question: str,
    use_hyde: bool,
    use_query_transform: bool,
    max_sources: int,
    max_retries: int = 5,
) -> tuple[dict[str, Any], float]:
    url = f"{base_url.rstrip('/')}/query"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "question": question,
        "use_hyde": use_hyde,
        "use_query_transform": use_query_transform,
        "max_sources": max_sources,
    }

    for attempt in range(max_retries):
        started = time.perf_counter()
        response = client.post(url, headers=headers, json=payload, timeout=120.0)
        latency_ms = (time.perf_counter() - started) * 1000
        if response.status_code != 429:
            response.raise_for_status()
            return response.json(), latency_ms

        retry_after = response.headers.get("Retry-After")
        wait_seconds = float(retry_after) if retry_after else min(60.0 * (attempt + 1), 300.0)
        print(
            f"  Rate limited (429). Waiting {wait_seconds:.0f}s "
            f"before retry {attempt + 1}/{max_retries}..."
        )
        time.sleep(wait_seconds)

    response.raise_for_status()
    return response.json(), latency_ms


def collect_evaluation_rows(
    client: httpx.Client,
    *,
    base_url: str,
    api_key: str,
    qa_pairs: list[dict[str, str]],
    experiment: ExperimentConfig,
) -> list[dict[str, Any]]:
    query_delay = float(os.getenv("EVAL_QUERY_DELAY_SECONDS", "1"))
    rows: list[dict[str, Any]] = []
    for index, pair in enumerate(qa_pairs, start=1):
        print(f"[{index}/{len(qa_pairs)}] Querying: {pair['question'][:80]}...")
        payload, latency_ms = query_rag(
            client,
            base_url=base_url,
            api_key=api_key,
            question=pair["question"],
            use_hyde=experiment.use_hyde,
            use_query_transform=experiment.use_query_transform,
            max_sources=experiment.max_sources,
        )
        if index < len(qa_pairs) and query_delay > 0:
            time.sleep(query_delay)
        contexts = [source["text"] for source in payload.get("sources", []) if source.get("text")]
        rows.append(
            {
                "question": pair["question"],
                "answer": payload.get("answer", ""),
                "contexts": contexts,
                "ground_truth": pair["ground_truth"],
                "trace_id": payload.get("trace_id"),
                "latency_ms": round(latency_ms, 2),
                "usage": payload.get("usage"),
            }
        )
    return rows


def run_ragas_evaluation(rows: list[dict[str, Any]]) -> tuple[dict[str, float], Any, TokenUsage]:
    dataset = Dataset.from_list(
        [
            {
                "question": row["question"],
                "answer": row["answer"],
                "contexts": row["contexts"],
                "ground_truth": row["ground_truth"],
            }
            for row in rows
        ]
    )
    openai_api_key = _openai_api_key()
    evaluator_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key)
    settings = get_settings()

    with get_openai_callback() as callback:
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
            llm=evaluator_llm,
            embeddings=embeddings,
        )

    judge_cost = callback.total_cost or estimate_openai_cost_usd(
        prompt_tokens=callback.prompt_tokens,
        completion_tokens=callback.completion_tokens,
        embedding_tokens=0,
        settings=settings,
    )
    judge_usage = TokenUsage(
        prompt_tokens=callback.prompt_tokens,
        completion_tokens=callback.completion_tokens,
        embedding_tokens=0,
        estimated_cost_usd=round(float(judge_cost), 6),
    )
    return _metrics_from_result(result), result, judge_usage


def write_results(
    output_dir: Path,
    *,
    timestamp: str,
    experiment: ExperimentConfig,
    metrics: dict[str, float],
    row_count: int,
    usage_summary: EvalUsageSummary,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    file_stem = f"ragas_results_{experiment.experiment_id}_{timestamp}"
    json_path = output_dir / f"{file_stem}.json"
    markdown_path = output_dir / f"{file_stem}.md"

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "experiment_id": experiment.experiment_id,
        "use_query_transform": experiment.use_query_transform,
        "use_hyde": experiment.use_hyde,
        "max_sources": experiment.max_sources,
        "sample_size": row_count,
        "metrics": metrics,
        "usage": _eval_usage_to_dict(usage_summary),
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# RAGAS Evaluation Results",
        "",
        f"- Generated at: {payload['generated_at']}",
        f"- Experiment: `{experiment.experiment_id}`",
        f"- use_query_transform: `{experiment.use_query_transform}`",
        f"- use_hyde: `{experiment.use_hyde}`",
        f"- max_sources: `{experiment.max_sources}`",
        f"- Sample size: {row_count}",
        "",
        "## Metrics",
        "",
        "| Metric | Score |",
        "| --- | ---: |",
    ]
    for metric_name, score in metrics.items():
        lines.append(f"| {metric_name} | {score:.4f} |")
    lines.extend(["", *_usage_markdown_lines(usage_summary)])
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, markdown_path


def write_details(
    output_dir: Path,
    *,
    timestamp: str,
    experiment: ExperimentConfig,
    metrics: dict[str, float],
    detail_records: list[dict[str, Any]],
    faithfulness_threshold: float,
    usage_summary: EvalUsageSummary,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    file_stem = f"ragas_details_{experiment.experiment_id}_{timestamp}"
    json_path = output_dir / f"{file_stem}.json"
    markdown_path = output_dir / f"{file_stem}.md"
    generated_at = datetime.now(UTC).isoformat()

    low_faithfulness = [
        record
        for record in detail_records
        if record["scores"].get("faithfulness") is not None
        and record["scores"]["faithfulness"] < faithfulness_threshold
    ]

    payload = {
        "generated_at": generated_at,
        "experiment_id": experiment.experiment_id,
        "use_query_transform": experiment.use_query_transform,
        "use_hyde": experiment.use_hyde,
        "max_sources": experiment.max_sources,
        "sample_size": len(detail_records),
        "metrics": metrics,
        "faithfulness_threshold": faithfulness_threshold,
        "low_faithfulness_count": len(low_faithfulness),
        "usage": _eval_usage_to_dict(usage_summary),
        "records": detail_records,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# RAGAS Per-Question Details",
        "",
        f"- Generated at: {generated_at}",
        f"- Experiment: `{experiment.experiment_id}`",
        f"- use_query_transform: `{experiment.use_query_transform}`",
        f"- use_hyde: `{experiment.use_hyde}`",
        f"- max_sources: `{experiment.max_sources}`",
        f"- Sample size: {len(detail_records)}",
        f"- Faithfulness threshold: {faithfulness_threshold:.2f}",
        f"- Low faithfulness cases: {len(low_faithfulness)}",
        "",
        "## Aggregate Metrics",
        "",
        "| Metric | Score |",
        "| --- | ---: |",
    ]
    for metric_name, score in metrics.items():
        lines.append(f"| {metric_name} | {score:.4f} |")
    lines.extend(["", *_usage_markdown_lines(usage_summary)])

    lines.extend(
        [
            "## Low Faithfulness Cases",
            "",
        ]
    )
    if low_faithfulness:
        for record in low_faithfulness:
            faithfulness_score = record["scores"]["faithfulness"]
            lines.extend(
                [
                    f"### #{record['index']} — faithfulness {faithfulness_score:.4f}",
                    "",
                    f"**Question:** {record['question']}",
                    "",
                    f"**Answer:** {_preview_text(record['answer'], ANSWER_PREVIEW_LENGTH)}",
                    "",
                    f"**Ground truth:** {_preview_text(record['ground_truth'], ANSWER_PREVIEW_LENGTH)}",
                    "",
                ]
            )
            if record.get("trace_id"):
                lines.append(f"**Langfuse trace_id:** `{record['trace_id']}`")
                lines.append("")
            lines.extend(
                [
                    "| Metric | Score |",
                    "| --- | ---: |",
                ]
            )
            for metric_name in METRIC_NAMES:
                metric_score = record["scores"].get(metric_name)
                formatted = f"{metric_score:.4f}" if metric_score is not None else "n/a"
                lines.append(f"| {metric_name} | {formatted} |")
            lines.append("")
    else:
        lines.append("No questions fell below the faithfulness threshold.")
        lines.append("")

    lines.extend(
        [
            "## All Questions",
            "",
            "| # | faithfulness | answer_relevancy | context_precision | context_recall | question |",
            "| ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for record in detail_records:
        score_cells = []
        for metric_name in METRIC_NAMES:
            metric_score = record["scores"].get(metric_name)
            score_cells.append(f"{metric_score:.4f}" if metric_score is not None else "n/a")
        question_preview = _preview_text(record["question"], 80)
        lines.append(
            f"| {record['index']} | {' | '.join(score_cells)} | {question_preview} |"
        )

    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, markdown_path


def _output_dir() -> Path:
    custom = os.getenv("EVAL_OUTPUT_DIR", "").strip()
    if custom:
        path = Path(custom)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent / path
        return path
    return Path(__file__).resolve().parent / "eval_results"


def main() -> int:
    _load_env()
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    api_key = _env("EVAL_API_KEY")
    experiment = _experiment_config()
    output_dir = _output_dir()
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    faithfulness_threshold = _faithfulness_threshold()

    print(f"Running RAGAS evaluation against {base_url}")
    print(f"Experiment: {experiment.experiment_id}")
    print(f"  use_query_transform={experiment.use_query_transform}")
    print(f"  use_hyde={experiment.use_hyde}")
    print(f"  max_sources={experiment.max_sources}")
    print(f"Dataset size: {len(SAMPLE_QA_PAIRS)} QA pairs")

    with httpx.Client() as client:
        rows = collect_evaluation_rows(
            client,
            base_url=base_url,
            api_key=api_key,
            qa_pairs=SAMPLE_QA_PAIRS,
            experiment=experiment,
        )

    metrics, result, judge_usage = run_ragas_evaluation(rows)
    usage_summary = _build_eval_usage_summary(rows, ragas_judge=judge_usage)
    detail_records = _build_detail_records(rows, _per_row_scores(result))
    json_path, markdown_path = write_results(
        output_dir,
        timestamp=timestamp,
        experiment=experiment,
        metrics=metrics,
        row_count=len(rows),
        usage_summary=usage_summary,
    )
    details_json_path, details_markdown_path = write_details(
        output_dir,
        timestamp=timestamp,
        experiment=experiment,
        metrics=metrics,
        detail_records=detail_records,
        faithfulness_threshold=faithfulness_threshold,
        usage_summary=usage_summary,
    )

    low_faithfulness_count = sum(
        1
        for record in detail_records
        if record["scores"].get("faithfulness") is not None
        and record["scores"]["faithfulness"] < faithfulness_threshold
    )

    print("\nRAGAS metrics:")
    for metric_name, score in metrics.items():
        print(f"  {metric_name}: {score:.4f}")
    print(
        f"\nPipeline tokens: {usage_summary.pipeline.total_tokens} "
        f"(${usage_summary.pipeline.estimated_cost_usd:.6f})"
    )
    print(
        f"RAGAS judge tokens: {usage_summary.ragas_judge.total_tokens} "
        f"(${usage_summary.ragas_judge.estimated_cost_usd:.6f})"
    )
    print(f"Total estimated cost: ${usage_summary.total_estimated_cost_usd:.6f}")
    print(
        f"Query latency mean/p95: "
        f"{usage_summary.latency.mean_ms:.0f} ms / {usage_summary.latency.p95_ms:.0f} ms"
    )
    print(
        f"\nLow faithfulness (< {faithfulness_threshold:.2f}): "
        f"{low_faithfulness_count}/{len(detail_records)} questions"
    )
    print(f"\nSaved JSON: {json_path}")
    print(f"Saved Markdown: {markdown_path}")
    print(f"Saved details JSON: {details_json_path}")
    print(f"Saved details Markdown: {details_markdown_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
