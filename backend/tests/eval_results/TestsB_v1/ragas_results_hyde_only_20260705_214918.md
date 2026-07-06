# RAGAS Evaluation Results

- Generated at: 2026-07-05T21:54:55.110152+00:00
- Experiment: `hyde_only`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8370 |
| answer_relevancy | 0.9194 |
| context_precision | 0.9947 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47655 |
| completion_tokens | 4754 |
| embedding_tokens | 2319 |
| total_tokens | 54728 |
| estimated_cost_usd | $0.010046 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 188625 |
| completion_tokens | 27030 |
| embedding_tokens | 0 |
| total_tokens | 215655 |
| estimated_cost_usd | $0.044195 |

### Totals

- Total estimated cost (pipeline + judge): `$0.054241`
- Query latency mean: `9914 ms`
- Query latency p50: `9494 ms`
- Query latency p95: `12554 ms`

