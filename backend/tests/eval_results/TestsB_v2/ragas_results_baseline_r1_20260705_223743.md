# RAGAS Evaluation Results

- Generated at: 2026-07-05T22:41:37.976595+00:00
- Experiment: `baseline_r1`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8292 |
| answer_relevancy | 0.8895 |
| context_precision | 0.9600 |
| context_recall | 0.9600 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 43851 |
| completion_tokens | 2397 |
| embedding_tokens | 243 |
| total_tokens | 46491 |
| estimated_cost_usd | $0.008022 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 186183 |
| completion_tokens | 25439 |
| embedding_tokens | 0 |
| total_tokens | 211622 |
| estimated_cost_usd | $0.043037 |

### Totals

- Total estimated cost (pipeline + judge): `$0.051059`
- Query latency mean: `5562 ms`
- Query latency p50: `5085 ms`
- Query latency p95: `6241 ms`

