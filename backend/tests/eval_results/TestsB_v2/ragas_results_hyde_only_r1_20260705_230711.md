# RAGAS Evaluation Results

- Generated at: 2026-07-05T23:12:08.857965+00:00
- Experiment: `hyde_only_r1`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25

## Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8367 |
| answer_relevancy | 0.9127 |
| context_precision | 0.9800 |
| context_recall | 0.9600 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47363 |
| completion_tokens | 4725 |
| embedding_tokens | 2288 |
| total_tokens | 54376 |
| estimated_cost_usd | $0.009984 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 179640 |
| completion_tokens | 22006 |
| embedding_tokens | 0 |
| total_tokens | 201646 |
| estimated_cost_usd | $0.031577 |

### Totals

- Total estimated cost (pipeline + judge): `$0.041561`
- Query latency mean: `7622 ms`
- Query latency p50: `7243 ms`
- Query latency p95: `10496 ms`

