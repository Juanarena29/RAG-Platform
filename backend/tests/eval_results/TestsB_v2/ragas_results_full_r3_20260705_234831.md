# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:54:51.366686+00:00
- Experiment: `full_r3`
- use_query_transform: `True`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8548 |
| answer_relevancy | 0.9203 |
| context_precision | 0.9780 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 51179 |
| completion_tokens | 5226 |
| embedding_tokens | 2357 |
| total_tokens | 58762 |
| estimated_cost_usd | $0.010859 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 181510 |
| completion_tokens | 21962 |
| embedding_tokens | 0 |
| total_tokens | 203472 |
| estimated_cost_usd | $0.031706 |

### Totals

- Total estimated cost (pipeline + judge): `$0.042565`
- Query latency mean: `10537 ms`
- Query latency p50: `10499 ms`
- Query latency p95: `12647 ms`

