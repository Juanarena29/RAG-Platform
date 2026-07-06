# RAGAS Per-Question Details

- Generated at: 2026-07-05T22:03:12.812165+00:00
- Experiment: `full`
- use_query_transform: `True`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 5

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8575 |
| answer_relevancy | 0.9077 |
| context_precision | 0.9947 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 51507 |
| completion_tokens | 5215 |
| embedding_tokens | 2376 |
| total_tokens | 59098 |
| estimated_cost_usd | $0.010905 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 180244 |
| completion_tokens | 27599 |
| embedding_tokens | 0 |
| total_tokens | 207843 |
| estimated_cost_usd | $0.041177 |

### Totals

- Total estimated cost (pipeline + judge): `$0.052082`
- Query latency mean: `12327 ms`
- Query latency p50: `12206 ms`
- Query latency p95: `15200 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for significantly more pa...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `66e4826f-cdca-4cbc-9a88-43c475a73c4c`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #5 — faithfulness 0.5000

**Question:** What is the purpose of feed-forward networks in transformer blocks?

**Answer:** The purpose of feed-forward networks in transformer blocks is to apply a fully connected feed-forward network to each position separately and identically, consisting of two linear transformations with a ReLU activation in between. This allows for additional processing of the representations gener...

**Ground truth:** Feed-forward networks apply nonlinear transformations independently to each position after attention, increasing the model's representational capacity.

**Langfuse trace_id:** `6dc8abe1-9b36-4478-98b2-d7f5804d8d75`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.6667

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize and improve the training of the model by normalizing the outputs of the sub-layers. This process is described as LayerNorm(x + Sublayer(x)), where Sub...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `1f07bdca-6051-4bcd-914c-51eb1cfa5692`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6667

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows HyDE to circumvent the ...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `80bc8bd4-7ee0-4461-92e1-60ed7dfc9e44`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #20 — faithfulness 0.5000

**Question:** How does attention enable modeling long-range dependencies?

**Answer:** Attention mechanisms allow modeling of dependencies without regard to their distance in the input or output sequences, enabling the learning of long-range dependencies more effectively than recurrent layers, which require sequential operations that increase with distance. Self-attention connects ...

**Ground truth:** Attention directly connects every token with every other token, allowing dependencies to be modeled regardless of sequence distance.

**Langfuse trace_id:** `53130879-5cd8-4b27-b944-58a1b8a3f3fd`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.7406 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0.8333 | 0.9629 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.4286 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 1.0000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9285 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.8571 | 0.9897 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8333 | 0.8661 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8396 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.8750 | 0.9515 | 0.8667 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 1.0000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.7500 | 0.6385 | 1.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9896 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 0.5000 | 0.7406 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 1.0000 | 0.9881 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.7778 | 0.7574 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.7500 | 0.9287 | 1.0000 | 0.0000 | How do retrieval and long-context models complement each other? |
