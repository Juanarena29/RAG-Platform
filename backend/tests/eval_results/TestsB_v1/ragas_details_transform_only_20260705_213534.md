# RAGAS Per-Question Details

- Generated at: 2026-07-05T21:39:30.017815+00:00
- Experiment: `transform_only`
- use_query_transform: `True`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 6

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8266 |
| answer_relevancy | 0.8646 |
| context_precision | 0.9400 |
| context_recall | 0.9200 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47360 |
| completion_tokens | 2725 |
| embedding_tokens | 388 |
| total_tokens | 50473 |
| estimated_cost_usd | $0.008749 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 183283 |
| completion_tokens | 27903 |
| embedding_tokens | 0 |
| total_tokens | 211186 |
| estimated_cost_usd | $0.043380 |

### Totals

- Total estimated cost (pipeline + judge): `$0.052129`
- Query latency mean: `6660 ms`
- Query latency p50: `6359 ms`
- Query latency p95: `10627 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `074f23bb-3af7-47d0-b4b2-54e5db0d8e4e`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.7619 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.5000

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize the learning process and improve convergence. Specifically, the output of each sub-layer is normalized using layer normalization, which is crucial for...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `fbadd184-8413-4580-8623-d182af270d4c`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6667

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows HyDE to circumvent the ...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `16818eb6-dea5-4011-9974-4dbab8c4d54e`

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

**Langfuse trace_id:** `d4b98554-d89a-4861-b24f-45dd335ae963`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.0000 |
| answer_relevancy | 0.0000 |
| context_precision | 0.0000 |
| context_recall | 1.0000 |

### #21 — faithfulness 0.2857

**Question:** Why is retrieval useful even for very large language models?

**Answer:** Retrieval is useful for very large language models because it allows them to combine parametric memory with non-parametric memories, addressing issues such as the inability to easily expand or revise memory and the production of 'hallucinations'. Hybrid models can directly revise and expand knowl...

**Ground truth:** Retrieval provides access to external knowledge at inference time, improving factual accuracy without requiring all knowledge to be stored in model parameters.

**Langfuse trace_id:** `da5c0381-06fc-4436-ac8b-96b6649e4e48`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.2857 |
| answer_relevancy | 0.9882 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.6250

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because hybrid models that combine parametric memory with non-parametric (i.e., retrieval-based) memories allow knowledge to be directly revised and expanded, and accessed knowledge can be inspected and interpreted. This capability helps address the issues of h...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `749f5bef-7b9a-4d8f-885a-826e52cfa1d2`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6250 |
| answer_relevancy | 0.7676 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.8100 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.4286 | 0.7619 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 1.0000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9285 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.7000 | 0.9648 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 1.0000 | 0.8205 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8366 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.7500 | 0.6760 | 0.5000 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 1.0000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9688 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 0.9451 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 0.8000 | 0.8438 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.2857 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 0.9634 | 1.0000 | 0.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.6250 | 0.7676 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.9091 | 0.9728 | 1.0000 | 0.0000 | How do retrieval and long-context models complement each other? |
