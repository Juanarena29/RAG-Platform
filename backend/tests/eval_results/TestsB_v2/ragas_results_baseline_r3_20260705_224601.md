# RAGAS Evaluation Results

- Generated at: 2026-07-05T22:50:47.061116+00:00
- Experiment: `baseline_r3`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8286 |
| answer_relevancy | 0.8887 |
| context_precision | 0.9500 |
| context_recall | 0.9867 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 43851 |
| completion_tokens | 2441 |
| embedding_tokens | 243 |
| total_tokens | 46535 |
| estimated_cost_usd | $0.008048 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 187956 |
| completion_tokens | 25435 |
| embedding_tokens | 0 |
| total_tokens | 213391 |
| estimated_cost_usd | $0.035890 |

### Totals

- Total estimated cost (pipeline + judge): `$0.043938`
- Query latency mean: `7538 ms`
- Query latency p50: `7402 ms`
- Query latency p95: `8575 ms`

