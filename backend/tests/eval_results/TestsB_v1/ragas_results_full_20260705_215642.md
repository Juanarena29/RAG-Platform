# RAGAS Evaluation Results

- Generated at: 2026-07-05T22:03:12.801654+00:00
- Experiment: `full`
- use_query_transform: `True`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8575 |
| answer_relevancy | 0.9077 |
| context_precision | 0.9947 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 51507 |
| completion_tokens | 5215 |
| embedding_tokens | 2376 |
| total_tokens | 59098 |
| estimated_cost_usd | $0.010905 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 180244 |
| completion_tokens | 27599 |
| embedding_tokens | 0 |
| total_tokens | 207843 |
| estimated_cost_usd | $0.041177 |

### Totals

- Total estimated cost (pipeline + judge): `$0.052082`
- Query latency mean: `12327 ms`
- Query latency p50: `12206 ms`
- Query latency p95: `15200 ms`

