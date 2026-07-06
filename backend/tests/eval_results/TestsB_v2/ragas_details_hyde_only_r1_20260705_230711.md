# RAGAS Per-Question Details

- Generated at: 2026-07-05T23:12:08.859866+00:00
- Experiment: `hyde_only_r1`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 5

## Aggregate Metrics

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

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `dc82d202-9913-4029-8c0d-9b7f834028cd`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.1429

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize and improve the training of the model by normalizing the outputs of the sub-layers. This is done to facilitate the residual connections, ensuring that...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `1a061543-b3ea-4a24-aabc-a0389816935c`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.1429 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6667

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows HyDE to circumvent the ...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `da58bd96-0731-4457-875a-27ca2d1f2fd9`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #21 — faithfulness 0.5000

**Question:** Why is retrieval useful even for very large language models?

**Answer:** Retrieval is useful for very large language models because it allows them to access and use relevant information effectively, especially in tasks that require multi-document understanding. Despite the models having larger context windows, they often struggle to retrieve and utilize relevant infor...

**Ground truth:** Retrieval provides access to external knowledge at inference time, improving factual accuracy without requiring all knowledge to be stored in model parameters.

**Langfuse trace_id:** `619ed796-ea83-4515-a9c1-e8a7c2c565ea`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.9882 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #25 — faithfulness 0.5714

**Question:** How do retrieval and long-context models complement each other?

**Answer:** Retrieval and long-context models complement each other by addressing the limitations of each approach. Retrieval models can effectively gather relevant information, but long-context models struggle to utilize this information effectively, particularly when it is positioned in the middle of long ...

**Ground truth:** Retrieval narrows the search space by selecting the most relevant documents, while long-context language models reason over that retrieved evidence. Together they reduce the need to process unnecessarily large contexts while improving access to relevant information.

**Langfuse trace_id:** `3be91c49-68f2-4786-8f91-c8ee4050dfa1`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 0.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.4286 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 0.8000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.1429 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9458 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.8000 | 0.9648 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8750 | 0.9682 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8306 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 0.8333 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 1.0000 | 0.6760 | 0.5000 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 1.0000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.8000 | 0.5962 | 1.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.8970 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.5000 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 0.9668 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.7642 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.7500 | 0.7574 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.5714 | 1.0000 | 1.0000 | 0.0000 | How do retrieval and long-context models complement each other? |
