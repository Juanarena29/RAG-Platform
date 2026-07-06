# RAGAS Per-Question Details

- Generated at: 2026-07-05T22:45:46.885561+00:00
- Experiment: `baseline_r2`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 6

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8258 |
| answer_relevancy | 0.8955 |
| context_precision | 0.9480 |
| context_recall | 1.0000 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 43851 |
| completion_tokens | 2311 |
| embedding_tokens | 243 |
| total_tokens | 46405 |
| estimated_cost_usd | $0.007969 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 185897 |
| completion_tokens | 24032 |
| embedding_tokens | 0 |
| total_tokens | 209929 |
| estimated_cost_usd | $0.032454 |

### Totals

- Total estimated cost (pipeline + judge): `$0.040423`
- Query latency mean: `5543 ms`
- Query latency p50: `5041 ms`
- Query latency p95: `7857 ms`

## Low Faithfulness Cases

### #3 — faithfulness 0.4286

**Question:** What problem does self-attention solve compared to recurrent networks?

**Answer:** Self-attention solves the problem of learning long-range dependencies more effectively than recurrent networks by connecting all positions with a constant number of sequentially executed operations, whereas recurrent layers require O(n) sequential operations. This allows for greater parallelizati...

**Ground truth:** Self-attention reduces sequential computation by allowing every position to attend directly to every other position with a constant number of sequential operations, making it easier to model long-range dependencies than recurrent networks.

**Langfuse trace_id:** `174cbacc-5b8d-4341-87ca-4024d6faa253`

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

**Langfuse trace_id:** `be2556f2-6db1-4806-8c2c-c54c5945cbc1`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #10 — faithfulness 0.6000

**Question:** How does RAG improve factual knowledge?

**Answer:** RAG improves factual knowledge by being more strongly grounded in real factual knowledge sources like Wikipedia, which reduces the likelihood of generating hallucinated content and increases the factual accuracy of its outputs. Additionally, RAG's retrieval mechanism allows it to dynamically upda...

**Ground truth:** RAG retrieves relevant external documents at inference time so generation is grounded in retrieved evidence instead of relying only on model parameters.

**Langfuse trace_id:** `6590d2d8-25b8-4835-9e02-ca47bb1cd9cd`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6000 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #15 — faithfulness 0.6667

**Question:** What is the main advantage of HyDE over directly embedding the query?

**Answer:** The main advantage of HyDE over directly embedding the query is that it decomposes dense retrieval into two tasks: a generative task performed by an instruction-following language model and a document-document similarity task performed by a contrastive encoder. This allows HyDE to circumvent the ...

**Ground truth:** HyDE creates a richer semantic representation of the user's intent by embedding a generated hypothetical document instead of the short query itself.

**Langfuse trace_id:** `4c2dc660-a571-4248-8e92-4f13b7558b66`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.6667 |
| answer_relevancy | 1.0000 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

### #16 — faithfulness 0.5000

**Question:** What challenge does the 'Lost in the Middle' paper identify?

**Answer:** I do not have enough information in the uploaded documents.

**Ground truth:** The paper shows that long-context language models often fail to use relevant information effectively when it appears in the middle of the provided context, performing better when the information is located near the beginning or end.

**Langfuse trace_id:** `6a98513d-ea08-4663-96d2-16cfaeb73be7`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.0000 |
| context_precision | 0.2500 |
| context_recall | 1.0000 |

### #25 — faithfulness 0.5714

**Question:** How do retrieval and long-context models complement each other?

**Answer:** Retrieval and long-context models complement each other by allowing for the integration of relevant information from retrieved documents into the language model's processing. However, the effectiveness of this integration is limited, as models often struggle to utilize long contexts effectively, ...

**Ground truth:** Retrieval narrows the search space by selecting the most relevant documents, while long-context language models reason over that retrieved evidence. Together they reduce the need to process unnecessarily large contexts while improving access to relevant information.

**Langfuse trace_id:** `d40dc8da-4f7a-4ff2-b260-79852c18dd21`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.9525 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0.8333 | 0.8317 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.4286 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 1.0000 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9394 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.8571 | 0.9897 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.6000 | 1.0000 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8915 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.8750 | 0.9174 | 0.4500 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 0.8000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.5000 | 0.0000 | 0.2500 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 1.0000 | 0.9175 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 0.7143 | 0.9882 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 0.8333 | 0.9669 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.7143 | 0.8801 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.5714 | 0.9525 | 1.0000 | 1.0000 | How do retrieval and long-context models complement each other? |
