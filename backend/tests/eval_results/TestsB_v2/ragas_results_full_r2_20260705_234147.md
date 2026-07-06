# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:48:04.637902+00:00
- Experiment: `full_r2`
- use_query_transform: `True`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8580 |
| answer_relevancy | 0.9169 |
| context_precision | 0.9780 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 51109 |
| completion_tokens | 5248 |
| embedding_tokens | 2428 |
| total_tokens | 58785 |
| estimated_cost_usd | $0.010865 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 177272 |
| completion_tokens | 28909 |
| embedding_tokens | 0 |
| total_tokens | 206181 |
| estimated_cost_usd | $0.037831 |

### Totals

- Total estimated cost (pipeline + judge): `$0.048696`
- Query latency mean: `10017 ms`
- Query latency p50: `9756 ms`
- Query latency p95: `12584 ms`

