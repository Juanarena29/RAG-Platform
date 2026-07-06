# RAGAS Per-Question Details

- Generated at: 2026-07-05T22:41:37.981257+00:00
- Experiment: `baseline_r1`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 6

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8292 |
| answer_relevancy | 0.8895 |
| context_precision | 0.9600 |
| context_recall | 0.9600 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 43851 |
| completion_tokens | 2397 |
| embedding_tokens | 243 |
| total_tokens | 46491 |
| estimated_cost_usd | $0.008022 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 186183 |
| completion_tokens | 25439 |
| embedding_tokens | 0 |
| total_tokens | 211622 |
| estimated_cost_usd | $0.043037 |

### Totals

- Total estimated cost (pipeline + judge): `$0.051059`
- Query latency mean: `5562 ms`
- Query latency p50: `5085 ms`
- Query latency p95: `6241 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `82f42a43-ab8e-4d1b-a09e-92cb3f55ab85`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4286 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.2857

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize and improve the training of the model by normalizing the outputs of the sub-layers. This is done to facilitate the residual connections, ensuring that...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `e48ebbe4-bbce-4ff2-81b4-76c55d494f6b`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.2857 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6667

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows HyDE to circumvent the ...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `503eb5c7-57d0-4939-9d6b-531a389ee4b1`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 0.0000 |

### #16 — faithfulness 0.5000

**Question:** What challenge does the 'Lost in the Middle' paper identify?

**Answer:** I do not have enough information in the uploaded documents.

**Ground truth:** The paper shows that long-context language models often fail to use relevant information effectively when it appears in the middle of the provided context, performing better when the information is located near the beginning or end.

**Langfuse trace_id:** `c33f54d9-5279-43cb-a9cf-78b1d435288a`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.0000 |
| context_precision | 0.2500 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.5000

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because it allows models to access and utilize external, factual information, which can be directly revised and expanded. This contrasts with pre-trained models that rely solely on their internal knowledge, which may lead to inaccuracies or 'hallucinations'. Hy...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `1262b53d-2184-482f-b57a-19da7bbc778a`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.8802 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #25 — faithfulness 0.5000

**Question:** How do retrieval and long-context models complement each other?

**Answer:** Retrieval and long-context models complement each other by addressing the limitations of each approach. Retrieval models can effectively gather relevant information, but long-context models struggle to utilize this information effectively, particularly when it is positioned in the middle of long ...

**Ground truth:** Retrieval narrows the search space by selecting the most relevant documents, while long-context language models reason over that retrieved evidence. Together they reduce the need to process unnecessarily large contexts while improving access to relevant information.

**Langfuse trace_id:** `35272cd6-4139-4a23-a7f3-3e94e1a0a8af`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.9287 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.4286 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 0.8000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.2857 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9285 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.9091 | 0.9648 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8319 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 1.0000 | 0.7565 | 0.7500 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 0.8750 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 0.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.5000 | 0.0000 | 0.2500 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.9175 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.7143 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 0.7500 | 0.9524 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.5000 | 0.8802 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.5000 | 0.9287 | 1.0000 | 1.0000 | How do retrieval and long-context models complement each other? |
