# RAGAS Per-Question Details

- Generated at: 2026-07-05T23:35:08.499432+00:00
- Experiment: `hyde_only_r3`
- use_query_transform: `False`
- use_hyde: `True`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 6

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8313 |
| answer_relevancy | 0.9195 |
| context_precision | 0.9980 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 47276 |
| completion_tokens | 4751 |
| embedding_tokens | 2323 |
| total_tokens | 54350 |
| estimated_cost_usd | $0.009988 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 184587 |
| completion_tokens | 25099 |
| embedding_tokens | 0 |
| total_tokens | 209686 |
| estimated_cost_usd | $0.042440 |

### Totals

- Total estimated cost (pipeline + judge): `$0.052428`
- Query latency mean: `8305 ms`
- Query latency p50: `7398 ms`
- Query latency p95: `14503 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.5714

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `48e59451-46d7-4994-8d67-0f6e16af57fb`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.7618 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #6 — faithfulness 0.2857

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize and improve the training of the model by normalizing the outputs of the sub-layers. This is done to facilitate the residual connections, ensuring that...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `3b1a2737-2dd3-42a7-8021-c8c20c9ff1cb`

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

**Langfuse trace_id:** `e4074b8b-b891-46dd-bb54-a65fde1f1a83`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #21 — faithfulness 0.2857

**Question:** Why is retrieval useful even for very large language models?

**Answer:** Retrieval is useful for very large language models because it allows them to access and utilize relevant information effectively, which can enhance their performance on various tasks. Despite the models' ability to handle large contexts, they often struggle to retrieve and use relevant informatio...

**Ground truth:** Retrieval provides access to external knowledge at inference time, improving factual accuracy without requiring all knowledge to be stored in model parameters.

**Langfuse trace_id:** `fe9cac59-9cd9-480f-bf52-e7b1adc5660e`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.2857 |
| answer_relevancy | 0.9882 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.6250

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because it allows for the direct revision and expansion of knowledge, which can be accessed, inspected, and interpreted. This contrasts with pre-trained models that do not have access to external memory and may produce hallucinations due to their inability to u...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `5684402d-560c-4b24-900f-6aa8bd52a44d`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6250 |
| answer_relevancy | 0.8801 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #25 — faithfulness 0.4000

**Question:** How do retrieval and long-context models complement each other?

**Answer:** Retrieval and long-context models complement each other by addressing the limitations of each approach. Retrieval models can effectively gather relevant information, while long-context models can process and utilize that information. However, both types of models struggle with the positioning of ...

**Ground truth:** Retrieval narrows the search space by selecting the most relevant documents, while long-context language models reason over that retrieved evidence. Together they reduce the need to process unnecessarily large contexts while improving access to relevant information.

**Langfuse trace_id:** `5dbb6bf4-963a-4780-8c88-0629822e3f99`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.4000 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.5714 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 0.8000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.2857 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9394 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.8571 | 0.9897 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8030 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8333 | 0.9172 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8306 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.8750 | 0.9680 | 0.9500 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 1.0000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.8333 | 0.5693 | 1.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9522 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.8926 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.2857 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.6250 | 0.8801 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.4000 | 1.0000 | 1.0000 | 1.0000 | How do retrieval and long-context models complement each other? |
