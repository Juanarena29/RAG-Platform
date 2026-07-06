# RAGAS Evaluation Results

- Generated at: 2026-07-05T21:39:30.015798+00:00
- Experiment: `transform_only`
- use_query_transform: `True`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8266 |
| answer_relevancy | 0.8646 |
| context_precision | 0.9400 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47360 |
| completion_tokens | 2725 |
| embedding_tokens | 388 |
| total_tokens | 50473 |
| estimated_cost_usd | $0.008749 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 183283 |
| completion_tokens | 27903 |
| embedding_tokens | 0 |
| total_tokens | 211186 |
| estimated_cost_usd | $0.043380 |

### Totals

- Total estimated cost (pipeline + judge): `$0.052129`
- Query latency mean: `6660 ms`
- Query latency p50: `6359 ms`
- Query latency p95: `10627 ms`

