# RAGAS Per-Question Details

- Generated at: 2026-07-05T23:41:21.046794+00:00
- Experiment: `full_r1`
- use_query_transform: `True`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 5

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8672 |
| answer_relevancy | 0.9058 |
| context_precision | 0.9800 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 50973 |
| completion_tokens | 5145 |
| embedding_tokens | 2370 |
| total_tokens | 58488 |
| estimated_cost_usd | $0.010780 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 176521 |
| completion_tokens | 28794 |
| embedding_tokens | 0 |
| total_tokens | 205315 |
| estimated_cost_usd | $0.036315 |

### Totals

- Total estimated cost (pipeline + judge): `$0.047095`
- Query latency mean: `9110 ms`
- Query latency p50: `8718 ms`
- Query latency p95: `11671 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `134de085-fac6-4e63-b496-b5aadd8cca5c`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.4286

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize and improve the training of the model by normalizing the outputs of the sub-layers. This is done to facilitate the residual connections, ensuring that...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `5ca71173-7f6e-4245-8a6a-c18b0dcaf943`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6667

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows HyDE to circumvent the ...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `a527ddcf-5abb-4619-9249-85e5b4af50fc`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.6667

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because hybrid models that combine parametric memory with non-parametric (i.e., retrieval-based) memories allow for direct revision and expansion of knowledge, and the accessed knowledge can be inspected and interpreted, addressing some of the issues that lead ...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `8abeb71f-baf0-4d96-be10-9f8df8cc4bcc`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 0.7574 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #25 — faithfulness 0.3750

**Question:** How do retrieval and long-context models complement each other?

**Answer:** Retrieval and long-context models complement each other by addressing the limitations of each approach. Retrieval models can effectively gather relevant information, but long-context models struggle to utilize this information effectively, particularly when it is not positioned at the beginning o...

**Ground truth:** Retrieval narrows the search space by selecting the most relevant documents, while long-context language models reason over that retrieved evidence. Together they reduce the need to process unnecessarily large contexts while improving access to relevant information.

**Langfuse trace_id:** `e6930c83-ab54-495f-b47d-8e05d302e090`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.3750 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.4286 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 0.8000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.4286 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9394 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.8571 | 0.9897 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8333 | 0.8904 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8306 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9754 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.8750 | 0.6760 | 0.5000 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 1.0000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 1.0000 | 0.5940 | 1.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 0.9851 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.9029 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 1.0000 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.6667 | 0.7574 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.3750 | 1.0000 | 1.0000 | 1.0000 | How do retrieval and long-context models complement each other? |
