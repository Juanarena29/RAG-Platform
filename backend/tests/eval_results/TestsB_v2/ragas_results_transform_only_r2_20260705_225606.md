# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:01:06.162983+00:00
- Experiment: `transform_only_r2`
- use_query_transform: `True`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8453 |
| answer_relevancy | 0.8758 |
| context_precision | 0.9500 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47239 |
| completion_tokens | 2810 |
| embedding_tokens | 391 |
| total_tokens | 50440 |
| estimated_cost_usd | $0.008781 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 182921 |
| completion_tokens | 29120 |
| embedding_tokens | 0 |
| total_tokens | 212041 |
| estimated_cost_usd | $0.035608 |

### Totals

- Total estimated cost (pipeline + judge): `$0.044389`
- Query latency mean: `7404 ms`
- Query latency p50: `6813 ms`
- Query latency p95: `9535 ms`

