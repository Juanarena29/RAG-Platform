# RAGAS Per-Question Details

- Generated at: 2026-07-05T23:16:58.779886+00:00
- Experiment: `hyde_only_r2`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 6

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8298 |
| answer_relevancy | 0.9196 |
| context_precision | 0.9947 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47411 |
| completion_tokens | 4793 |
| embedding_tokens | 2306 |
| total_tokens | 54510 |
| estimated_cost_usd | $0.010033 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 187950 |
| completion_tokens | 27073 |
| embedding_tokens | 0 |
| total_tokens | 215023 |
| estimated_cost_usd | $0.035038 |

### Totals

- Total estimated cost (pipeline + judge): `$0.045071`
- Query latency mean: `7198 ms`
- Query latency p50: `6929 ms`
- Query latency p95: `9003 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.5714

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `a5faa3df-8e3f-4381-8eb7-69510b066177`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.3333

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize the learning process and improve convergence. Specifically, the output of each sub-layer is normalized, which aids in maintaining consistent performan...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `975f4a10-ce62-4276-9d70-e2b7c54b217b`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.3333 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6667

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows HyDE to circumvent the ...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `7f0cf228-14b1-40f4-a33b-8eb0ec9dfbea`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #21 — faithfulness 0.5714

**Question:** Why is retrieval useful even for very large language models?

**Answer:** Retrieval is useful for very large language models because it allows them to access and utilize relevant information effectively, which can enhance their performance on various tasks. Despite the models' ability to handle large contexts, they often struggle to retrieve and use relevant informatio...

**Ground truth:** Retrieval provides access to external knowledge at inference time, improving factual accuracy without requiring all knowledge to be stored in model parameters.

**Langfuse trace_id:** `7b75b14c-2cb8-487e-9fd9-1aa47c1012ca`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.9881 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.3333

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because it allows models to access and utilize external, factual information directly, which can be revised and expanded. This contrasts with pre-trained models that rely solely on their internal knowledge, which may lead to inaccuracies or 'hallucinations'. Hy...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `afb24d0c-2df5-426c-8733-d2252eab2ec1`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.3333 |
| answer_relevancy | 0.8801 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #25 — faithfulness 0.2857

**Question:** How do retrieval and long-context models complement each other?

**Answer:** Retrieval and long-context models complement each other by addressing the limitations of each approach. Retrieval models can effectively gather relevant information, but long-context models struggle to utilize this information effectively, particularly when it is not positioned at the beginning o...

**Ground truth:** Retrieval narrows the search space by selecting the most relevant documents, while long-context language models reason over that retrieved evidence. Together they reduce the need to process unnecessarily large contexts while improving access to relevant information.

**Langfuse trace_id:** `56b5d5e2-872d-4c93-b125-0a96d3585300`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.2857 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 0.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.5714 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 0.8333 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.3333 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9394 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.9000 | 0.9648 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 1.0000 | 0.8905 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8306 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.8750 | 0.9469 | 0.8667 | 0.0000 | What is HyDE in information retrieval? |
| 14 | 0.8750 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.7500 | 0.6123 | 1.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9631 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.9175 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.5714 | 0.9881 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 0.9668 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.3333 | 0.8801 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.2857 | 1.0000 | 1.0000 | 0.0000 | How do retrieval and long-context models complement each other? |
