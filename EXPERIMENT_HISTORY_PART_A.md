# RAG Pipeline — Experiment History — Part A: Prompt Iteration

> This is **Part A** of the experiment history, covering the initial prompt-engineering iteration (query-rewrite and HyDE prompt wording, generator behavior). It is organized as a **chronological, sequential log**: each experiment typically changes one thing relative to the previous one and is compared to it directly.
>
> For the follow-up **controlled 2×2 ablation study** (isolating the *presence* of the query-transform step and the HyDE step, independent of prompt wording), see **[Part B — Ablation Study](./EXPERIMENT_HISTORY_PART_B_ablation.md)**.

This document tracks the chronological evolution of RAGAS-based evaluation experiments on the RAG pipeline (query rewriting → HyDE → hybrid retrieval → generation). All runs use the same 25-question evaluation set (transformer / RAG / HyDE / long-context topics), `faithfulness_threshold = 0.70`.

> **Note on comparability:** Between Experiment 1 and Experiment 2 the `ground_truth` reference answers for several questions (notably #3, #6) were rewritten to be longer and more specific. `context_precision` and `context_recall` are computed relative to `ground_truth`, so part of the metric movement between those two runs reflects a **change in the evaluation reference, not necessarily a pipeline change**. `faithfulness` and `answer_relevancy` do not depend on `ground_truth` (faithfulness is scored against retrieved context, relevancy against the question), so movement in those two metrics between Exp 1 and Exp 2 is attributable to answer/generation variance rather than the ground-truth edit. This is called out explicitly below and should be kept in mind for all cross-experiment deltas.

---



## Experiment 1 — Baseline

**Timestamp:** 2026-07-05T16:40:33Z

**Objective:** Establish a baseline RAGAS score for the pipeline before any prompt tuning.

**Changes introduced:** None — first recorded evaluation run. The pipeline already includes a query-rewrite step and a HyDE step at this point; both run with their baseline/default prompts (not yet captured verbatim in this report — the baseline query-rewrite prompt is documented for the first time in Experiment 3, for reference purposes).

**Motivation:** Need a reference point before iterating on prompts or retrieval parameters.

**RAGAS Metrics**


| Metric            | Score  |
| ----------------- | ------ |
| Faithfulness      | 0.8428 |
| Answer Relevancy  | 0.8879 |
| Context Precision | 0.9347 |
| Context Recall    | 0.9600 |


Low-faithfulness cases: 6 (#3, #6, #15, #16, #24, #25).

**Comparison with previous experiment:** N/A (baseline).

**Technical analysis:** Failures cluster on questions requiring synthesis/comparison ("problem self-attention solves vs RNNs", "why layer norm matters", "HyDE's advantage over raw query embedding", "how retrieval and long-context models complement each other"). In all of these, `context_precision`/`context_recall` are already 1.0, meaning retrieval is not the bottleneck — the generator is adding paraphrased claims not strictly traceable to the retrieved chunks. Case #16 ("Lost in the Middle") returned a refusal ("I do not have enough information"), zeroing `answer_relevancy` for that item, which points to a retrieval miss for that specific query, not a faithfulness issue.

**Conclusion:** Reasonable starting point (faithfulness 0.84). Main opportunity: reduce generator paraphrasing/over-elaboration and fix the one clear retrieval miss (#16).

---



## Experiment 2 — Ground truth revision

**Timestamp:** 2026-07-05T17:33:51Z

**Objective:** Tighten the evaluation reference set and introduce an explicit HyDE system prompt (previously implicit/default).

**Changes introduced:**

1. `ground_truth` rewritten for several questions (e.g., #3, #6) to be longer and technically denser.
2. HyDE prompt made explicit:
  ```text
   Write a concise technical paragraph (~150 words) that would answer the user's
   question as if it appeared in a research paper or technical document.
   Use factual, declarative language. Return only the paragraph.
  ```
3. Query-rewrite prompt unchanged — still running the same baseline version that was active since Experiment 1 (not yet documented verbatim; first captured in Experiment 3).

**Motivation:** More detailed ground truths give the LLM-judge a stricter, less ambiguous reference for `context_precision`/`context_recall` scoring; formalizing the HyDE prompt makes the hypothetical-document generation step reproducible and tunable going forward.

**RAGAS Metrics**


| Metric            | Score  |
| ----------------- | ------ |
| Faithfulness      | 0.8201 |
| Answer Relevancy  | 0.8901 |
| Context Precision | 0.9447 |
| Context Recall    | 0.9600 |


Low-faithfulness cases: 5 (#3, #6, #16, #24, #25).

**Comparison with previous experiment:** Faithfulness **↓ 0.0227**, Answer Relevancy ↑ 0.0022, Context Precision ↑ 0.0100, Context Recall unchanged.

**Technical analysis:** ⚠️ **Confounded comparison.** The `context_precision` increase could be influenced by the ground-truth rewrite rather than the new HyDE prompt alone, since precision scoring is reference-dependent. The faithfulness drop, however, is *not* explained by the ground-truth change (faithfulness has no dependency on `ground_truth`); it is driven by answer #6 scoring 0.2857 — the worst single result recorded across all experiments — where the generated answer padded the correct claim with extra unsupported elaboration. This looks like normal generation variance rather than a regression caused by either change.

**Conclusion:** **Inconclusive as an isolated experiment** — two variables changed simultaneously (ground truth + HyDE prompt), and the net faithfulness score is worse. Recommend not treating this as a "the HyDE prompt made things worse" result; the observed drop is most likely LLM sampling variance in the generator, unrelated to the HyDE change.

---



## Experiment 3 — Stricter HyDE prompt

**Timestamp:** 2026-07-05T17:51:35Z

**Objective:** Reduce HyDE hallucination risk, specifically topic/domain drift when a question references a paper title or named method.

**Changes introduced:** HyDE prompt rewritten with explicit guardrails:

```text
- Stay faithful to the user's question.
- Do not invent alternative meanings for titles, names, or terminology.
- If the question mentions a paper title, assume it refers to the actual research
  paper rather than another domain.
- Use precise technical language and avoid speculation.
- Do not mention that this is hypothetical.
```

Query-rewrite prompt: **no change** — this is where the baseline version (already active and unchanged since Experiment 1) is documented verbatim for the first time, purely as a reference point for the deliberate change made in Experiment 4:

```text
You rewrite user questions to improve semantic document retrieval. Expand
abbreviations, clarify intent, and remove conversational filler. Return only
the rewritten question without explanation.
```

Ground truth unchanged from Experiment 2.

**Motivation:** Prevent HyDE from generating hypothetical documents that reinterpret ambiguous titles/terms (e.g., "Lost in the Middle") into an unrelated domain, which would pull irrelevant chunks into context. The query-rewrite prompt was left untouched in this run so that the effect of the HyDE change could be isolated, and so its baseline text would be on record before being modified in Experiment 4.

**RAGAS Metrics**


| Metric            | Score  |
| ----------------- | ------ |
| Faithfulness      | 0.8470 |
| Answer Relevancy  | 0.8963 |
| Context Precision | 0.9733 |
| Context Recall    | 0.9600 |


Low-faithfulness cases: 7 (#3, #6, #15, #20, #21, #24, #25).

**Comparison with previous experiment:** Faithfulness ↑ 0.0269, Answer Relevancy ↑ 0.0062, Context Precision **↑ 0.0286**, Context Recall unchanged. Ground truth is held constant vs. Exp 2, so this Context Precision gain is cleanly attributable to the pipeline change (stricter HyDE + new query-rewrite step) rather than a reference shift.

**Technical analysis:** Because the query-rewrite prompt was held constant here (same baseline as Exp 1/Exp 2) and only the HyDE prompt changed, the context precision improvement is cleanly attributable to the HyDE guardrails: a prompt that refuses to reinterpret titles produces hypothetical documents better aligned with the true document space, improving the ranking of retrieved chunks. Faithfulness improved only modestly and the *count* of low-faithfulness cases actually grew (5 → 7), with two new entries (#20, #21) appearing. This indicates the HyDE fix did not address the generator's tendency to over-elaborate/paraphrase on synthesis-style questions — the same failure mode seen in Exp 1 and Exp 2 — and that the query-rewrite step (still on its baseline prompt) remained a separate, unaddressed weak point.

**Conclusion:** **Confirmed, isolated improvement** on context precision from the HyDE guardrails alone. Faithfulness gain is marginal and the underlying generator-verbosity problem persists. The query-rewrite prompt is still on its original baseline at this point — the next experiment targets that step directly.

---



## Experiment 4 — Query-rewrite prompt hardened (canonical terminology)

**Timestamp:** 2026-07-05T17:59:10Z

**Objective:** Fix retrieval/generation failures tied to named methods, papers, and abbreviations being paraphrased away during query rewriting.

**Changes introduced:** Query-rewrite prompt significantly expanded:

```text
- Preserve the original meaning of the question.
- Expand abbreviations when appropriate (e.g., RAG → Retrieval-Augmented Generation).
- Clarify ambiguous wording without changing the user's intent.
- If the question mentions a paper title, method, model, dataset, or algorithm,
  preserve its canonical name exactly and, when helpful, include its technical context.
- Do NOT reinterpret titles or names into another domain.
- Remove conversational filler.
- Keep the rewritten question concise (one sentence).
```

HyDE prompt unchanged from Experiment 3 (guardrailed version). Ground truth unchanged from Experiment 3 (full `SAMPLE_QA_PAIRS` list confirmed identical). This is the **first and only change made to the query-rewrite prompt** across the whole series — it had been running on its original baseline (documented in Experiment 3) since Experiment 1.

**Motivation:** The query rewriter, not just HyDE, could be silently dropping or reinterpreting canonical terms (paper titles, model names) before the query ever reaches HyDE/retrieval — extending the same guardrail principle applied to HyDE in Exp 3 to this earlier stage of the pipeline.

**RAGAS Metrics**


| Metric            | Score  |
| ----------------- | ------ |
| Faithfulness      | 0.9135 |
| Answer Relevancy  | 0.9253 |
| Context Precision | 0.9747 |
| Context Recall    | 1.0000 |


Low-faithfulness cases: **2** (#3, #15).

**Comparison with previous experiment:** Faithfulness **↑ 0.0665** (best result to date), Answer Relevancy ↑ 0.0290, Context Precision ↑ 0.0014, Context Recall **↑ 0.0400 → perfect 1.0000**. Low-faithfulness case count dropped from 7 to 2.

**Technical analysis:** This is the clearest cause-and-effect result in the series. Ground truth and HyDE prompt were both held constant relative to Experiment 3, and — unlike Exp 1–3, where the query-rewrite prompt had never been touched — this run changed *only* the query-rewrite prompt. Context recall reaching 1.0000 confirms that previously-missed relevant chunks (e.g., for "Lost in the Middle" style questions) are now being retrieved, because the canonical term-preservation instruction stops the rewriter from softening or generalizing specific terminology. Higher recall directly feeds a more complete context for generation, which explains the faithfulness jump — the generator has more grounded material to draw claims from, reducing the incidence of unsupported elaboration.

**Conclusion:** **Confirmed improvement — best configuration recorded so far.** The query-rewrite prompt (canonical-term preservation) is the single highest-leverage change identified in this experiment series.

---



## Experiment 5 — Repeat run, same configuration

**Timestamp:** 2026-07-05T18:11:54Z

**Objective:** (Undocumented change set — no prompt or ground-truth diffs are present in this run's artifacts relative to Experiment 4.)

**Changes introduced:** None documented. Presumed same query-rewrite prompt, HyDE prompt, and ground truth as Experiment 4.

**Motivation:** N/A — appears to be a repeat evaluation rather than a deliberate pipeline change.

**RAGAS Metrics**


| Metric            | Score  |
| ----------------- | ------ |
| Faithfulness      | 0.8591 |
| Answer Relevancy  | 0.9190 |
| Context Precision | 0.9780 |
| Context Recall    | 1.0000 |


Low-faithfulness cases: 5 (#6, #15, #21, #24, #25).

**Comparison with previous experiment:** Faithfulness **↓ 0.0544** vs. Experiment 4, Answer Relevancy ↓ 0.0063, Context Precision ↑ 0.0033, Context Recall unchanged (still perfect). Low-faithfulness cases rose from 2 to 5.

**Technical analysis:** Since no configuration change is recorded between Exp 4 and Exp 5, and context recall remains perfect, this drop is best explained by **generation-side stochastic variance** (non-zero sampling temperature in the answer generator) rather than a regression in the pipeline itself. Question #6 ("why is layer normalization important") re-surfaces as a low-faithfulness case for the second time in the series — consistent with it being a systematically fragile question rather than one tied to any specific prompt version.

**Conclusion:** **Inconclusive / not a confirmed regression.** No pipeline change was made; the metric swing illustrates that a single run at Experiment 4's configuration is not sufficient to certify 0.9135 as the "true" faithfulness of that configuration. Repeated trials are needed before treating any single score as representative.

---



## Experiment 6 — Repeat run, same configuration

**Timestamp:** 2026-07-05T18:21:52Z

**Objective:** (Undocumented change set — no prompt or ground-truth diffs recorded vs. Experiment 5.)

**Changes introduced:** None documented.

**Motivation:** N/A.

**RAGAS Metrics**


| Metric            | Score  |
| ----------------- | ------ |
| Faithfulness      | 0.8917 |
| Answer Relevancy  | 0.9076 |
| Context Precision | 0.9800 |
| Context Recall    | 0.9467 |


Low-faithfulness cases: 4 (#6, #15, #16, #24).

**Comparison with previous experiment:** Faithfulness ↑ 0.0326 (partial recovery), Answer Relevancy ↓ 0.0114, Context Precision ↑ 0.0020, Context Recall **↓ 0.0533** (first drop below 1.0 since Experiment 4).

**Technical analysis:** The context recall drop (questions #21 and #25 lost some recall) with no documented retrieval or prompt change again points to **evaluator/generation stochasticity** rather than a deterministic pipeline effect — at this sample size (25 questions), a single question moving from full to partial recall is enough to move the aggregate by several points. #16 ("Lost in the Middle") reappears as a low-faithfulness case, though not a full retrieval miss this time (context precision is 1.0 for it), suggesting intermittent generator over-generalization on that question rather than a resolved-then-regressed retrieval issue.

**Conclusion:** **Inconclusive.** Still within the noise band established by Experiments 4–6; no new pipeline change to attribute this movement to.

---



## Experiment 7 — Repeat run, same configuration

**Timestamp:** 2026-07-05T18:42:52Z

**Objective:** (Undocumented change set — no prompt or ground-truth diffs recorded vs. Experiment 6.)

**Changes introduced:** None documented.

**Motivation:** N/A.

**RAGAS Metrics**


| Metric            | Score      |
| ----------------- | ---------- |
| Faithfulness      | 0.8850     |
| Answer Relevancy  | 0.9199     |
| Context Precision | **1.0000** |
| Context Recall    | 0.9600     |


Low-faithfulness cases: 4 (#3, #6, #15, #25).

**Comparison with previous experiment:** Faithfulness ↓ 0.0067 (essentially flat), Answer Relevancy ↑ 0.0123, Context Precision **↑ 0.0200 → perfect 1.0000 for the first time**, Context Recall ↑ 0.0133.

**Technical analysis:** Context precision reaching 1.0000 is a positive signal but, combined with the flat faithfulness score and the recurrence of the same recurring hard questions (#3, #6, #15, #25 have now each appeared as low-faithfulness cases in the majority of the seven runs), it reinforces that **retrieval quality is no longer the limiting factor** at this configuration — the ceiling on faithfulness (~0.85–0.91 across Exp 4–7) is set by the generator's tendency to add paraphrased, only loosely-grounded elaboration on synthesis/comparison questions.

**Conclusion:** **Stable plateau, no regression.** The pipeline has converged to a configuration where retrieval is near-perfect but faithfulness is capped by generator verbosity on a known, recurring subset of questions.

---



## Key Lessons Learned

1. **Query-rewrite prompt is the highest-leverage change found.** The query-rewrite step was present from Experiment 1 onward but stayed on its original baseline prompt through Experiments 1–3. The first and only time it was modified — Experiment 4, enforcing preservation of canonical terminology (paper titles, method/model names, abbreviations) — produced the largest confirmed jump in faithfulness (+0.0665) and drove context recall to a perfect 1.0000 for the first time.
2. **HyDE guardrails against domain reinterpretation improve context precision** (Experiment 3), independent of and complementary to the query-rewrite fix.
3. **Ground-truth edits and pipeline edits should never be bundled in the same run.** Experiment 2 changed both simultaneously, making it impossible to cleanly attribute the context-precision movement to either cause; `faithfulness`/`answer_relevancy` are unaffected by ground-truth wording and remain safe to compare across such edits, but `context_precision`/`context_recall` are not.
4. **A single evaluation run is not sufficient to certify a configuration.** Experiments 5–7 held configuration constant (as far as documented) yet faithfulness varied by ±0.05 and context recall moved between 0.9467 and 1.0000, purely from generation/evaluation stochasticity. Any reported "best score" should be an average over multiple runs, not a single sample.
5. **A small set of questions is systemically weak** — self-attention vs. RNNs (#3), layer normalization rationale (#6), HyDE's advantage over raw embeddings (#15), and retrieval/long-context complementarity (#25) recur as low-faithfulness cases in nearly every experiment, almost always with perfect context precision/recall. This points to a **generation-side issue** (answers add explanatory detail beyond what is explicitly supported by retrieved context) rather than a retrieval issue, and should be the next target.

---



## Evolution of the Pipeline


| Exp | Timestamp (UTC) | Key change                                                                                         | Faithfulness | Answer Relevancy | Context Precision | Context Recall | Low-faith cases |
| --- | --------------- | -------------------------------------------------------------------------------------------------- | ------------ | ---------------- | ----------------- | -------------- | --------------- |
| 1   | 16:40           | Baseline                                                                                           | 0.8428       | 0.8879           | 0.9347            | 0.9600         | 6               |
| 2   | 17:33           | Ground truth rewritten + HyDE prompt formalized (query-rewrite still on baseline)                  | 0.8201       | 0.8901           | 0.9447            | 0.9600         | 5               |
| 3   | 17:51           | HyDE prompt hardened (no domain reinterpretation); query-rewrite baseline documented but unchanged | 0.8470       | 0.8963           | 0.9733            | 0.9600         | 7               |
| 4   | 17:59           | Query-rewrite prompt changed for the first time (canonical terminology)                            | **0.9135**   | **0.9253**       | 0.9747            | **1.0000**     | **2**           |
| 5   | 18:11           | Repeat run, no documented change                                                                   | 0.8591       | 0.9190           | 0.9780            | 1.0000         | 5               |
| 6   | 18:21           | Repeat run, no documented change                                                                   | 0.8917       | 0.9076           | 0.9800            | 0.9467         | 4               |
| 7   | 18:42           | Repeat run, no documented change                                                                   | 0.8850       | 0.9199           | **1.0000**        | 0.9600         | 4               |


---



## Current Best Configuration

**As of Experiment 4 / carried forward through Experiment 7 (unchanged):**

- **Query-rewrite prompt:** canonical-terminology-preserving version (expands abbreviations, keeps paper/method/model names exact, one-sentence output).
- **HyDE prompt:** guardrailed version (no domain reinterpretation of titles/terms, factual/declarative tone, ~100–150 word hypothetical paragraph, no meta-commentary).
- **Ground truth set:** the expanded/detailed `SAMPLE_QA_PAIRS` version introduced in Experiment 2 and unchanged since.

Peak single-run result: **Experiment 4** (Faithfulness 0.9135, Context Recall 1.0000). Experiments 5–7 at nominally the same configuration averaged **Faithfulness ≈ 0.879 (range 0.859–0.914 including Exp 4)**, which should be treated as the more realistic expected performance of this configuration pending further runs.

---

## Addendum — findings confirmed by Part B

Two open items from this document were later resolved by the [Part B ablation study](./EXPERIMENT_HISTORY_PART_B_ablation.md):

1. **The Experiment 5–7 variance was indeed caused by non-zero generator temperature**, as suspected in the technical analysis above (`backend/app/rag/generator.py` was running at `temperature = 0.1`). This was confirmed when Part B's own v1 → v2 revision fixed the generator to `temperature = 0.0` and repeat-run standard deviation on faithfulness dropped from ±0.05 (this document, Exp 5–7) to ±0.002–0.008 (Part B v2, n=3 per configuration). **Key Lesson 4** above (single runs are not sufficient to certify a configuration) is the direct ancestor of that fix.
2. **Key Lesson 1** ("query-rewrite prompt is the highest-leverage change") should be read together with Part B: every experiment here that used the hardened query-rewrite prompt (Exp 4 onward) also had HyDE enabled, so the two effects were never isolated in this document. Part B's controlled ablation found that `full` (both enabled) is the best configuration overall, but that `transform_only` alone does not clearly dominate `baseline` the way this document's sequential comparisons implied — see Part B's "Revision notes (v1 → v2)" for the full picture.
3. **Key Lesson 5**'s systemically-weak question set (#3, #6, #15, #25) is **confirmed and narrowed** by Part B v2: across 12 ablation runs (4 configurations × 3 repeats), questions **#3, #6, and #15** show low faithfulness in 12/12 runs regardless of `query_transform`/`hyde` settings, while #25 turned out to be tied to specific augmentation combinations rather than universally weak. This is now the highest-confidence, highest-priority remaining issue across both experiment series, and it is a generator/prompt problem rather than a retrieval one.