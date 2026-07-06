# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:35:08.497046+00:00
- Experiment: `hyde_only_r3`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8313 |
| answer_relevancy | 0.9195 |
| context_precision | 0.9980 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47276 |
| completion_tokens | 4751 |
| embedding_tokens | 2323 |
| total_tokens | 54350 |
| estimated_cost_usd | $0.009988 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 184587 |
| completion_tokens | 25099 |
| embedding_tokens | 0 |
| total_tokens | 209686 |
| estimated_cost_usd | $0.042440 |

### Totals

- Total estimated cost (pipeline + judge): `$0.052428`
- Query latency mean: `8305 ms`
- Query latency p50: `7398 ms`
- Query latency p95: `14503 ms`

