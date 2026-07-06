# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:41:21.036104+00:00
- Experiment: `full_r1`
- use_query_transform: `True`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8672 |
| answer_relevancy | 0.9058 |
| context_precision | 0.9800 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 50973 |
| completion_tokens | 5145 |
| embedding_tokens | 2370 |
| total_tokens | 58488 |
| estimated_cost_usd | $0.010780 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 176521 |
| completion_tokens | 28794 |
| embedding_tokens | 0 |
| total_tokens | 205315 |
| estimated_cost_usd | $0.036315 |

### Totals

- Total estimated cost (pipeline + judge): `$0.047095`
- Query latency mean: `9110 ms`
- Query latency p50: `8718 ms`
- Query latency p95: `11671 ms`

