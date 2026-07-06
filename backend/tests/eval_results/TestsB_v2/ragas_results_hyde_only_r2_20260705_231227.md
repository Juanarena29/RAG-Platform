# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:16:58.777717+00:00
- Experiment: `hyde_only_r2`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8298 |
| answer_relevancy | 0.9196 |
| context_precision | 0.9947 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47411 |
| completion_tokens | 4793 |
| embedding_tokens | 2306 |
| total_tokens | 54510 |
| estimated_cost_usd | $0.010033 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 187950 |
| completion_tokens | 27073 |
| embedding_tokens | 0 |
| total_tokens | 215023 |
| estimated_cost_usd | $0.035038 |

### Totals

- Total estimated cost (pipeline + judge): `$0.045071`
- Query latency mean: `7198 ms`
- Query latency p50: `6929 ms`
- Query latency p95: `9003 ms`

