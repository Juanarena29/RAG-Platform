# RAGAS Per-Question Details

- Generated at: 2026-07-05T23:01:06.171254+00:00
- Experiment: `transform_only_r2`
- use_query_transform: `True`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 5

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8453 |
| answer_relevancy | 0.8758 |
| context_precision | 0.9500 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47239 |
| completion_tokens | 2810 |
| embedding_tokens | 391 |
| total_tokens | 50440 |
| estimated_cost_usd | $0.008781 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 182921 |
| completion_tokens | 29120 |
| embedding_tokens | 0 |
| total_tokens | 212041 |
| estimated_cost_usd | $0.035608 |

### Totals

- Total estimated cost (pipeline + judge): `$0.044389`
- Query latency mean: `7404 ms`
- Query latency p50: `6813 ms`
- Query latency p95: `9535 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `3575ce92-2f5c-481d-91de-4abf7b7b9921`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.3333

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize the learning process and improve convergence. Specifically, the output of each sub-layer is normalized, which aids in maintaining consistent performan...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `629e02d9-4127-41bd-93e1-206e733dbf8f`

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

**Langfuse trace_id:** `c4eb7bb6-7f3c-4070-88e6-f034b15ae8a8`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #16 — faithfulness 0.0000

**Question:** What challenge does the 'Lost in the Middle' paper identify?

**Answer:** I do not have enough information in the uploaded documents.

**Ground truth:** The paper shows that long-context language models often fail to use relevant information effectively when it appears in the middle of the provided context, performing better when the information is located near the beginning or end.

**Langfuse trace_id:** `29579db2-a59f-4628-9fa9-636008e11120`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.0000 |
| answer_relevancy | 0.0000 |
| context_precision | 0.2500 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.5000

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because it allows models to access and utilize external, factual information directly, which can be revised and expanded as needed. This contrasts with pre-trained models that rely solely on their internal knowledge, which may lead to inaccuracies or 'hallucina...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `7b612ba8-179b-467b-93af-b290f8b0cb86`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.8801 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.4286 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 1.0000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.3333 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9394 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.8571 | 0.9931 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 1.0000 | 0.9130 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8306 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 0.8571 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 1.0000 | 0.6760 | 0.5000 | 0.0000 | What is HyDE in information retrieval? |
| 14 | 0.8750 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.0000 | 0.0000 | 0.2500 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9631 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 0.8353 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.8831 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.8571 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 0.8333 | 1.0000 | 1.0000 | 0.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6270 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.5000 | 0.8801 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.9231 | 0.9022 | 1.0000 | 1.0000 | How do retrieval and long-context models complement each other? |
