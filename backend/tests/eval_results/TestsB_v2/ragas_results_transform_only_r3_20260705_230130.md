# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:06:58.905774+00:00
- Experiment: `transform_only_r3`
- use_query_transform: `True`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8452 |
| answer_relevancy | 0.8813 |
| context_precision | 0.9600 |
| context_recall | 0.9600 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47452 |
| completion_tokens | 2742 |
| embedding_tokens | 388 |
| total_tokens | 50582 |
| estimated_cost_usd | $0.008771 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 184673 |
| completion_tokens | 24146 |
| embedding_tokens | 0 |
| total_tokens | 208819 |
| estimated_cost_usd | $0.034480 |

### Totals

- Total estimated cost (pipeline + judge): `$0.043251`
- Query latency mean: `8976 ms`
- Query latency p50: `9079 ms`
- Query latency p95: `10896 ms`

