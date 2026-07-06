# RAGAS Evaluation Results

- Generated at: 2026-07-05T22:55:51.830186+00:00
- Experiment: `transform_only_r1`
- use_query_transform: `True`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8290 |
| answer_relevancy | 0.8770 |
| context_precision | 0.9480 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47247 |
| completion_tokens | 2854 |
| embedding_tokens | 395 |
| total_tokens | 50496 |
| estimated_cost_usd | $0.008812 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 184483 |
| completion_tokens | 22815 |
| embedding_tokens | 0 |
| total_tokens | 207298 |
| estimated_cost_usd | $0.033806 |

### Totals

- Total estimated cost (pipeline + judge): `$0.042618`
- Query latency mean: `7127 ms`
- Query latency p50: `6666 ms`
- Query latency p95: `9779 ms`

