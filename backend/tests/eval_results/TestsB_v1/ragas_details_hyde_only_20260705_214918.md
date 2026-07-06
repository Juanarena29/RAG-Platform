# RAGAS Per-Question Details

- Generated at: 2026-07-05T21:54:55.118056+00:00
- Experiment: `hyde_only`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 5

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8370 |
| answer_relevancy | 0.9194 |
| context_precision | 0.9947 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47655 |
| completion_tokens | 4754 |
| embedding_tokens | 2319 |
| total_tokens | 54728 |
| estimated_cost_usd | $0.010046 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 188625 |
| completion_tokens | 27030 |
| embedding_tokens | 0 |
| total_tokens | 215655 |
| estimated_cost_usd | $0.044195 |

### Totals

- Total estimated cost (pipeline + judge): `$0.054241`
- Query latency mean: `9914 ms`
- Query latency p50: `9494 ms`
- Query latency p95: `12554 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.5000

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively compared to recurrent networks. It connects all positions with a constant number of sequentially executed operations, while recurrent layers require O(n) sequential operations, making self-attention faster and ...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `be89a581-b937-4399-9f71-51f672078516`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #5 — faithfulness 0.5000

**Question:** What is the purpose of feed-forward networks in transformer blocks?

**Answer:** The purpose of feed-forward networks in transformer blocks is to apply a fully connected feed-forward network to each position separately and identically, consisting of two linear transformations with a ReLU activation in between. This allows for additional processing of the representations gener...

**Ground truth:** Feed-forward networks apply nonlinear transformations independently to each position after attention, increasing the model's representational capacity.

**Langfuse trace_id:** `99ffaf5d-c1f6-4b66-a44b-ff0a39ae0365`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6000

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows the retrieval task to b...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `c70b2070-e769-4fa0-97ab-01f9bc737b59`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6000 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #21 — faithfulness 0.4286

**Question:** Why is retrieval useful even for very large language models?

**Answer:** Retrieval is useful for very large language models because it helps them access and use relevant information more effectively, especially in tasks that require multi-document understanding. It allows models to leverage document-document similarity and enhances their performance on downstream task...

**Ground truth:** Retrieval provides access to external knowledge at inference time, improving factual accuracy without requiring all knowledge to be stored in model parameters.

**Langfuse trace_id:** `e2102249-1c42-429d-8376-760d85e656df`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.9882 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.6250

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because it allows for the direct revision and expansion of knowledge, which can be accessed, inspected, and interpreted. This contrasts with pre-trained models that do not have access to external memory and may produce hallucinations due to their inability to u...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `2fc359da-6a40-40a3-9b2e-55a9923602aa`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6250 |
| answer_relevancy | 0.8739 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.8592 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.5000 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 0.8000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9285 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.7000 | 0.9648 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8333 | 0.8904 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8273 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 0.8000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.8750 | 0.9717 | 0.8667 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 1.0000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6000 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.7500 | 0.6122 | 1.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9674 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 0.9451 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.8882 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.4286 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.7655 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.6250 | 0.8739 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.7143 | 1.0000 | 1.0000 | 1.0000 | How do retrieval and long-context models complement each other? |
