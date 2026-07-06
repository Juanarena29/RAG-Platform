# RAGAS Evaluation Results

- Generated at: 2026-07-05T21:31:24.833983+00:00
- Experiment: `baseline`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8673 |
| answer_relevancy | 0.8833 |
| context_precision | 0.9567 |
| context_recall | 0.9600 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 43851 |
| completion_tokens | 2400 |
| embedding_tokens | 243 |
| total_tokens | 46494 |
| estimated_cost_usd | $0.008023 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 186854 |
| completion_tokens | 23836 |
| embedding_tokens | 0 |
| total_tokens | 210690 |
| estimated_cost_usd | $0.042022 |

### Totals

- Total estimated cost (pipeline + judge): `$0.050045`
- Query latency mean: `7936 ms`
- Query latency p50: `7504 ms`
- Query latency p95: `8835 ms`

