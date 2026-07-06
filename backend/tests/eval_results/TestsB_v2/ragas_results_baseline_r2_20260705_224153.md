# RAGAS Evaluation Results

- Generated at: 2026-07-05T22:45:46.883037+00:00
- Experiment: `baseline_r2`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8258 |
| answer_relevancy | 0.8955 |
| context_precision | 0.9480 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 43851 |
| completion_tokens | 2311 |
| embedding_tokens | 243 |
| total_tokens | 46405 |
| estimated_cost_usd | $0.007969 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 185897 |
| completion_tokens | 24032 |
| embedding_tokens | 0 |
| total_tokens | 209929 |
| estimated_cost_usd | $0.032454 |

### Totals

- Total estimated cost (pipeline + judge): `$0.040423`
- Query latency mean: `5543 ms`
- Query latency p50: `5041 ms`
- Query latency p95: `7857 ms`

