# RAGAS Per-Question Details

- Generated at: 2026-07-05T22:55:51.832815+00:00
- Experiment: `transform_only_r1`
- use_query_transform: `True`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 6

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8290 |
| answer_relevancy | 0.8770 |
| context_precision | 0.9480 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47247 |
| completion_tokens | 2854 |
| embedding_tokens | 395 |
| total_tokens | 50496 |
| estimated_cost_usd | $0.008812 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 184483 |
| completion_tokens | 22815 |
| embedding_tokens | 0 |
| total_tokens | 207298 |
| estimated_cost_usd | $0.033806 |

### Totals

- Total estimated cost (pipeline + judge): `$0.042618`
- Query latency mean: `7127 ms`
- Query latency p50: `6666 ms`
- Query latency p95: `9779 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.5714

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `774bac30-6b8e-4859-b686-666035464288`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.5000

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize and improve the training of the model by normalizing the output of each sub-layer before it is passed to the next layer. This process is described as ...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `0b760cf5-5a4d-41b5-99ff-815fb0817eda`

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

**Langfuse trace_id:** `f3d70698-09d9-4551-8c83-18e95a6f9899`

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

**Langfuse trace_id:** `ab1456d9-edae-4bd2-8693-ffe487ba7793`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.0000 |
| answer_relevancy | 0.0000 |
| context_precision | 0.2500 |
| context_recall | 1.0000 |

### #20 — faithfulness 0.5714

**Question:** How does attention enable modeling long-range dependencies?

**Answer:** Attention mechanisms enable modeling long-range dependencies by allowing the model to connect all positions with a constant number of sequentially executed operations, which reduces the path length between any two input and output positions. This shorter path length makes it easier to learn long-...

**Ground truth:** Attention directly connects every token with every other token, allowing dependencies to be modeled regardless of sequence distance.

**Langfuse trace_id:** `febd6fce-54a2-42c6-bc08-aea9e9ac8be8`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.8438 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.4000

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because it allows for the direct revision and expansion of knowledge, and the accessed knowledge can be inspected and interpreted, which helps in providing accurate information rather than generating potentially false or misleading content.

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `9cd37fb3-dd60-4ff8-b00f-cd074368788b`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4000 |
| answer_relevancy | 0.8520 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.5714 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 1.0000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9394 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.9000 | 0.9648 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.7455 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 1.0000 | 0.8151 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8306 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 1.0000 | 0.8370 | 0.4500 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 0.8750 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.0000 | 0.0000 | 0.2500 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9688 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 0.5714 | 0.8438 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.8571 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 0.8333 | 0.9802 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.4000 | 0.8520 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.8000 | 0.9009 | 1.0000 | 1.0000 | How do retrieval and long-context models complement each other? |
