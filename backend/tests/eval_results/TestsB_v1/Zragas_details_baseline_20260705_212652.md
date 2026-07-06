# RAGAS Per-Question Details

- Generated at: 2026-07-05T21:31:24.836358+00:00
- Experiment: `baseline`
- use_query_transform: `False`
- use_hyde: `False`
- max_sources: `5`
- Sample size: 25
- Faithfulness threshold: 0.70
- Low faithfulness cases: 4

## Aggregate Metrics

| Metric | Score |
| --- | ---: |
| faithfulness | 0.8673 |
| answer_relevancy | 0.8833 |
| context_precision | 0.9567 |
| context_recall | 0.9600 |

## Usage

### Pipeline (/query)

| Metric | Value |
| --- | ---: |
| prompt_tokens | 43851 |
| completion_tokens | 2400 |
| embedding_tokens | 243 |
| total_tokens | 46494 |
| estimated_cost_usd | $0.008023 |

### RAGAS judge

| Metric | Value |
| --- | ---: |
| prompt_tokens | 186854 |
| completion_tokens | 23836 |
| embedding_tokens | 0 |
| total_tokens | 210690 |
| estimated_cost_usd | $0.042022 |

### Totals

- Total estimated cost (pipeline + judge): `$0.050045`
- Query latency mean: `7936 ms`
- Query latency p50: `7504 ms`
- Query latency p95: `8835 ms`

## Low Faithfulness Cases

### #6 — faithfulness 0.5000

**Question:** Why is layer normalization important in transformers?

**Answer:** Layer normalization is important in transformers because it is applied after the residual connections around each sub-layer, which helps stabilize and improve the training of the model by normalizing the output of each sub-layer before it is passed to the next layer. This process is described as ...

**Ground truth:** Layer normalization is applied together with residual connections around each sub-layer to stabilize optimization, improve convergence, and enable effective training of deep transformer models.

**Langfuse trace_id:** `36ea08fc-ce44-4693-bcd8-ab4571b3323e`

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

**Langfuse trace_id:** `d5f618dc-2de7-4be2-bfaa-edba526f4e38`

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

**Langfuse trace_id:** `1a8c9a38-6a77-45c8-9eb3-6c332e6272b6`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5000 |
| answer_relevancy | 0.0000 |
| context_precision | 0.0000 |
| context_recall | 1.0000 |

### #24 — faithfulness 0.5714

**Question:** Why can retrieval reduce hallucinations?

**Answer:** Retrieval can reduce hallucinations because hybrid models that combine parametric memory with non-parametric (i.e., retrieval-based) memories allow for direct revision and expansion of knowledge, and the accessed knowledge can be inspected and interpreted, which helps mitigate the production of h...

**Ground truth:** Retrieval reduces hallucinations by grounding generation on relevant external documents instead of relying only on knowledge stored in model parameters, allowing responses to be supported by retrieved evidence.

**Langfuse trace_id:** `e9365b60-1c6b-4c71-bdaf-ecd013264794`

| Metric | Score |
| --- | ---: |
| faithfulness | 0.5714 |
| answer_relevancy | 0.8417 |
| context_precision | 1.0000 |
| context_recall | 1.0000 |

## All Questions

| # | faithfulness | answer_relevancy | context_precision | context_recall | question |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0.8333 | 0.8317 | 1.0000 | 1.0000 | What is the attention mechanism in transformers? |
| 2 | 1.0000 | 0.9606 | 1.0000 | 1.0000 | How does multi-head attention work? |
| 3 | 0.8571 | 0.7618 | 1.0000 | 1.0000 | What problem does self-attention solve compared to recurrent networks? |
| 4 | 0.8333 | 0.9860 | 1.0000 | 1.0000 | Why are positional encodings required in transformers? |
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the purpose of feed-forward networks in transformer blocks? |
| 6 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | Why is layer normalization important in transformers? |
| 7 | 1.0000 | 0.9285 | 1.0000 | 1.0000 | What is scaled dot-product attention? |
| 8 | 0.7273 | 0.9648 | 1.0000 | 1.0000 | Why are transformers more parallelizable than recurrent neural networks? |
| 9 | 1.0000 | 0.8317 | 1.0000 | 1.0000 | What is retrieval-augmented generation? |
| 10 | 0.8889 | 0.8904 | 1.0000 | 1.0000 | How does RAG improve factual knowledge? |
| 11 | 1.0000 | 0.8535 | 1.0000 | 1.0000 | How are retrieved documents used in RAG? |
| 12 | 1.0000 | 0.9732 | 1.0000 | 1.0000 | What is top-k retrieval in RAG? |
| 13 | 0.8750 | 0.9174 | 0.9167 | 1.0000 | What is HyDE in information retrieval? |
| 14 | 1.0000 | 0.9711 | 1.0000 | 1.0000 | Why can HyDE improve zero-shot retrieval? |
| 15 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | What is the main advantage of HyDE over directly embedding the query? |
| 16 | 0.5000 | 0.0000 | 0.0000 | 1.0000 | What challenge does the 'Lost in the Middle' paper identify? |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | How does document position affect long-context language models? |
| 18 | 1.0000 | 0.9896 | 1.0000 | 1.0000 | Why are long context windows not always sufficient for question answering? |
| 19 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | What is the main contribution of the Transformer architecture? |
| 20 | 0.7143 | 0.8426 | 1.0000 | 1.0000 | How does attention enable modeling long-range dependencies? |
| 21 | 1.0000 | 0.9881 | 1.0000 | 1.0000 | Why is retrieval useful even for very large language models? |
| 22 | 1.0000 | 0.9235 | 1.0000 | 1.0000 | How do transformers enable retrieval-augmented generation systems? |
| 23 | 1.0000 | 0.6271 | 1.0000 | 1.0000 | What limitation of parametric knowledge motivates retrieval? |
| 24 | 0.5714 | 0.8417 | 1.0000 | 1.0000 | Why can retrieval reduce hallucinations? |
| 25 | 0.7143 | 1.0000 | 1.0000 | 0.0000 | How do retrieval and long-context models complement each other? |
