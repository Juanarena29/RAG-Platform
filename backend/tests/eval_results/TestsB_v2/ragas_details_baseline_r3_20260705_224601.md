# RAGAS Per-Question Details

- Generated at: 2026-07-05T22:50:47.065104+00:00
- Experiment: `baseline_r3`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 6

## Aggregate Metrics

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

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `fdc9e00f-b16b-4f2b-8c2b-29d26ffb61d2`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.5000

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize the learning process and improve convergence. Specifically, the output of each sub-layer is normalized using layer normalization, which is crucial for...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `15e83088-ec6c-446c-aae1-942563c524fc`

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

**Langfuse trace_id:** `c38d83eb-6314-4a08-8a72-9ea7d28d8348`

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

**Langfuse trace_id:** `0e07d55b-9bd9-477b-ae54-82d6fdd5cff8`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.0000 |
| answer_relevancy | 0.0000 |
| context_precision | 0.2500 |
| context_recall | 1.0000 |

### #21 — faithfulness 0.5714

**Question:** Why is retrieval useful even for very large language models?

**Answer:** Retrieval is useful for very large language models because it allows them to access and use relevant information effectively, especially in tasks that require retrieving matching tokens from input contexts. This capability is crucial for improving performance in multi-document question answering ...

**Ground truth:** Retrieval provides access to external knowledge at inference time, improving factual accuracy without requiring all knowledge to be stored in model parameters.

**Langfuse trace_id:** `598ddc7f-fe9f-431c-913e-67fd53e63e04`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.9882 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.5000

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because it allows models to access and utilize external, factual information, which can be directly revised and expanded. This contrasts with pre-trained models that rely solely on their internal knowledge, which may lead to inaccuracies or 'hallucinations'. Hy...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `d473a450-dd2e-4efc-8d56-b488d396ee6f`

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
| 5 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9394 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.8571 | 0.9897 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8750 | 0.9257 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8306 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 1.0000 | 0.7565 | 0.5000 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 0.8750 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.0000 | 0.0000 | 0.2500 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9631 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.9175 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.5714 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 0.8571 | 0.9379 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6270 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.5000 | 0.8801 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.8333 | 1.0000 | 1.0000 | 0.6667 | How do retrieval and long-context models complement each other? |
