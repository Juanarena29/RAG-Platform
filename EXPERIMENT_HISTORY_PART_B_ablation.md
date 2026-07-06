# RAG Pipeline — Experiment History — Part B: Ablation Study (`query_transform` × `hyde`)

> This is **Part B** of the experiment history. Unlike **[Part A](./EXPERIMENT_HISTORY_PART_A.md)** — a sequential log where each experiment tweaks prompt wording and is compared to the immediately previous run — Part B is a **controlled 2×2 ablation**: the generator/prompt configuration is held fixed (the best configuration carried over from Part A), and only two boolean pipeline flags are toggled: `use_query_transform` and `use_hyde`.

| Experiment | `use_query_transform` | `use_hyde` |
| --- | :-: | :-: |
| B1 — `baseline` | ❌ | ❌ |
| B2 — `transform_only` | ✅ | ❌ |
| B3 — `hyde_only` | ❌ | ✅ |
| B4 — `full` | ✅ | ✅ |

This design isolates the individual contribution of each step and lets us check whether their effects **compose additively** when both are enabled — something Part A could not test, since every Part A experiment from Exp 3 onward had `hyde` enabled.

**This document has two revisions, kept both for traceability:**

- **[v2 — canonical results](#part-b-v2--canonical-results-n3-generator-temperature--00)** (below): generator `temperature = 0.0`, **3 runs per configuration** (12 runs total). This is the version to cite going forward.
- **[v1 — archived, superseded](#part-b-v1--archived-superseded)** (end of document): the original single-run-per-configuration pass, run with generator `temperature = 0.1`. Kept for history only — several of its per-question findings did not replicate in v2 (see [Revision notes](#revision-notes-v1--v2)).

**Why the revision:** v1 was run before it was noticed that the answer generator (`backend/app/rag/generator.py`) had `temperature = 0.1` while `hyde.py` and `query_transformer.py` were already at `0.0`. Part A had already shown (Experiments 5–7) that non-zero generator temperature alone can swing faithfulness by ±0.05 across identical configurations. v1's four ablation cells were each a **single run**, so it was impossible to tell how much of the B1–B4 differences were the pipeline flags vs. generator sampling noise. v2 fixes the generator at `temperature = 0.0` and repeats each cell 3 times to report mean ± population standard deviation.

---

## Part B v2 — Canonical results (n=3, generator temperature = 0.0)

**Timestamps:** 2026-07-05T22:37–23:48 UTC (12 runs).

**Methodology:** Same 25-question set as v1 and Part A, same `max_sources = 5`, same Part-A-derived query-rewrite/HyDE prompts. The only code change relative to v1 is `generator.py`'s `temperature: 0.1 → 0.0`. Each of the 4 configurations (B1–B4) was run 3 times back-to-back (`_r1`, `_r2`, `_r3`). Raw artifacts: `backend/tests/eval_results/TestsB_v2/`.

### Summary — mean ± std across 3 runs

| Config | Faithfulness | Answer Relevancy | Context Precision | Context Recall | Low-faith count (mean) | Cost (mean) | Latency mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 `baseline` | 0.8279 ± 0.0015 | 0.8912 ± 0.0030 | 0.9527 ± 0.0052 | 0.9822 ± 0.0166 | 6.0 | $0.0452 | 6,214 ms |
| B2 `transform_only` | 0.8398 ± 0.0076 | 0.8780 ± 0.0024 | 0.9527 ± 0.0052 | 0.9600 ± 0.0327 | 5.3 | $0.0434 | 7,836 ms |
| B3 `hyde_only` | 0.8326 ± 0.0030 | **0.9173 ± 0.0032** | **0.9909 ± 0.0078** | 0.9600 ± 0.0327 | 5.7 | $0.0464 | 7,708 ms |
| B4 `full` | **0.8600 ± 0.0053** | 0.9143 ± 0.0062 | 0.9787 ± 0.0009 | **1.0000 ± 0.0000** | 5.0 | $0.0461 | **9,888 ms** |

### Per-run detail (transparency appendix)

| Run | Faithfulness | Answer Relevancy | Context Precision | Context Recall | Cost | Latency mean / p95 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline_r1 | 0.8292 | 0.8895 | 0.9600 | 0.9600 | $0.05106 | 5,562 / 6,241 ms |
| baseline_r2 | 0.8258 | 0.8955 | 0.9480 | 1.0000 | $0.04042 | 5,543 / 7,857 ms |
| baseline_r3 | 0.8286 | 0.8887 | 0.9500 | 0.9867 | $0.04394 | 7,538 / 8,575 ms |
| transform_only_r1 | 0.8290 | 0.8770 | 0.9480 | 1.0000 | $0.04262 | 7,127 / 9,779 ms |
| transform_only_r2 | 0.8453 | 0.8758 | 0.9500 | 0.9200 | $0.04439 | 7,404 / 9,535 ms |
| transform_only_r3 | 0.8452 | 0.8813 | 0.9600 | 0.9600 | $0.04325 | 8,976 / 10,896 ms |
| hyde_only_r1 | 0.8367 | 0.9127 | 0.9800 | 0.9600 | $0.04156 | 7,622 / 10,496 ms |
| hyde_only_r2 | 0.8298 | 0.9196 | 0.9947 | 0.9200 | $0.04507 | 7,198 / 9,003 ms |
| hyde_only_r3 | 0.8313 | 0.9195 | 0.9980 | 1.0000 | $0.05243 | 8,305 / 14,503 ms |
| full_r1 | 0.8672 | 0.9058 | 0.9800 | 1.0000 | $0.04710 | 9,110 / 11,671 ms |
| full_r2 | 0.8580 | 0.9169 | 0.9780 | 1.0000 | $0.04870 | 10,017 / 12,584 ms |
| full_r3 | 0.8548 | 0.9203 | 0.9780 | 1.0000 | $0.04257 | 10,537 / 12,647 ms |

### Stability by question (low-faithfulness incidence, out of 3 runs per config)

| # | Question topic | baseline | transform_only | hyde_only | full |
| :-: | --- | :-: | :-: | :-: | :-: |
| 3 | Self-attention vs. RNNs | 3/3 | 3/3 | 3/3 | 3/3 |
| 6 | Layer normalization rationale | 3/3 | 3/3 | 3/3 | 3/3 |
| 15 | HyDE's advantage over raw embedding | 3/3 | 3/3 | 3/3 | 3/3 |
| 16 | "Lost in the Middle" | 3/3 | 3/3 | **0/3** | **0/3** |
| 21 | Retrieval usefulness for large LLMs | 1/3 | 2/3 | 3/3 | 2/3 |
| 24 | Retrieval reduces hallucinations | 2/3 | 2/3 | 2/3 | 2/3 |
| 25 | Retrieval + long-context complementarity | 2/3 | 0/3 | 2/3 | 0/3 |

Context-recall instability (< 1.0 in at least one run) concentrates on two questions:

| # | Question | baseline recall (r1,r2,r3) | transform_only | hyde_only | full |
| :-: | --- | --- | --- | --- | --- |
| 22 | Transformers enabling RAG | 1.0, 1.0, 1.0 | 1.0, **0.0**, 1.0 | 1.0, 1.0, 1.0 | 1.0, 1.0, 1.0 |
| 25 | Retrieval + long-context complementarity | 1.0, 1.0, 0.67 | 1.0, 1.0, 1.0 | **0.0, 0.0**, 1.0 | 1.0, 1.0, 1.0 |

### Analysis

**Faithfulness is now stable within each config (std 0.0015–0.0076)**, roughly an order of magnitude tighter than the ±0.05 swings observed in Part A Experiments 5–7 at `temperature = 0.1`. This confirms the generator's sampling temperature — not the pipeline flags — was the dominant source of noise in v1. With that noise removed, the config ranking on faithfulness is now clear and repeatable: `full` (0.8600) > `transform_only` (0.8398) > `hyde_only` (0.8326) > `baseline` (0.8279).

**Question #16 ("Lost in the Middle") is now cleanly and consistently fixed by HyDE alone**, independent of query-transform: 0/3 low-faithfulness in both `hyde_only` and `full`, vs. 3/3 in both configs without HyDE. This is a stronger, cleaner version of the same finding from v1 — the recurring retrieval miss is resolved whenever `use_hyde = True`, regardless of `use_query_transform`.

**Questions #3, #6, and #15 are now confirmed as a hard, generator-side ceiling on faithfulness, independent of every pipeline flag combination:** all three appear as low-faithfulness in **12 out of 12 runs**, across all four configurations. This is the strongest and cleanest signal in the whole experiment series — retrieval quality is not the variable here (context precision/recall for these three questions is consistently near-perfect in the underlying detail records); the generator adds claims beyond what the retrieved context strictly supports on these three synthesis-style questions regardless of what augmentation feeds it.

**Context recall instability on #22 and #25 is real but does not replicate v1's story.** v1 attributed a "negative interaction" specifically to `full` (query-transform breaking a fix that HyDE alone provided on #25). In v2, `full` has **perfect context recall in all 3 runs**, while it is `hyde_only` that shows the #25 miss (2 of 3 runs at 0.0) and `transform_only` that shows the isolated #22 miss (1 of 3 runs). **The v1 "query-transform + HyDE interact negatively" conclusion does not replicate under n=3 with a stable generator** — see [Revision notes](#revision-notes-v1--v2).

**Latency and cost scale as expected with the number of LLM calls**: `baseline` (6.2 s) < `hyde_only` ≈ `transform_only` (7.7–7.8 s) < `full` (9.9 s). v1's anomaly (`transform_only` appearing *faster* than `baseline`) does not reproduce in v2 — `transform_only` is reliably slower than `baseline` across all 3 runs, confirming that anomaly was measurement noise as flagged in v1's "Next Planned Experiments."

### Conclusions (v2)

1. **`full` (query_transform ON, HyDE ON) is the best-performing configuration overall**, not `hyde_only`. It has the best faithfulness (0.8600), a perfect and stable context recall (1.0000 ± 0.0000 across all 3 runs), and the second-best answer relevancy — at the cost of being the slowest configuration (~9.9 s mean).
2. **`hyde_only` remains the best choice for answer relevancy and per-run context precision**, and is meaningfully faster than `full` (~7.7 s vs. ~9.9 s), but its context recall is less stable than `full`'s (std 0.0327 vs. 0.0000) due to intermittent misses on question #25.
3. **HyDE (with or without query-transform) is what fixes question #16**, not query-transform. This part of the v1 finding is confirmed and strengthened.
4. **Query-transform alone (`transform_only`) is no longer the clear worst configuration it appeared to be in v1.** Its faithfulness (0.8398) is actually the second-best of the four, though it does not resolve #16 on its own and has the least stable context recall together with `hyde_only`.
5. **Three questions (#3, #6, #15) set a hard faithfulness ceiling regardless of configuration.** This is now the single highest-confidence, highest-priority finding across both Part A and Part B — it is a generator/prompt problem, not a retrieval or augmentation-flag problem, and no combination of `use_query_transform`/`use_hyde` tested here moves it.

### Recommended configuration (v2)

**`full` (`use_query_transform = True`, `use_hyde = True`)** is the recommended production configuration if faithfulness and retrieval completeness are prioritized over latency: it has the best faithfulness and the only perfectly stable (0 variance) context recall of the four configurations.

**`hyde_only`** remains a reasonable choice if the ~2.2 s latency saving vs. `full` matters more than the last ~0.03 of faithfulness and the occasional #25 recall miss.

Either way, **the next highest-leverage fix is on the generator/prompt side**, targeting the #3/#6/#15 faithfulness ceiling — not further toggling of `query_transform`/`hyde` presence.

### Revision notes (v1 → v2)

| v1 claim | Status after v2 | Notes |
| --- | --- | --- |
| "HyDE alone (`hyde_only`) is the best single-feature configuration and the best overall" | **Revised** | With n=3, `full` has both higher mean faithfulness and a perfectly stable 1.0 context recall; `hyde_only` no longer strictly dominates. |
| "`transform_only` is the worst configuration on nearly every metric" | **Revised** | `transform_only` has the second-best faithfulness in v2 (0.8398); it is only clearly worse on answer relevancy and context precision. |
| "The two steps interact negatively; `full` reintroduces the #25 regression that HyDE alone fixed" | **Not replicated** | In v2, `full` has zero recall misses on #25 across 3 runs; the #25 miss instead appears in `hyde_only` (2/3 runs). The specific interaction-effect story from v1 does not hold up. |
| "`transform_only` has lower mean latency than `baseline`" | **Not replicated** | Confirmed as noise, as v1 itself flagged; `transform_only` is consistently slower than `baseline` in all 3 v2 runs. |
| "Generator verbosity on #3/#15/#24 (and other recurring questions) sets the faithfulness ceiling" | **Confirmed and sharpened** | v2 pins this down to #3, #6, #15 specifically, at 12/12 runs — the cleanest and most repeatable finding in either part of this study. |
| "HyDE resolves the recurring #16 retrieval/faithfulness miss" | **Confirmed** | Now 0/3 in both `hyde_only` and `full` vs. 3/3 in both non-HyDE configs — cleaner than the single-run v1 evidence. |

### Next planned experiments

1. **Target the #3/#6/#15 faithfulness ceiling directly** — e.g. a generator-prompt revision that explicitly restricts claims to what is verbatim supported by the numbered context fragments, tested against `full` (the current recommended config) with n≥3 for comparability.
2. **Investigate the #25 miss under `hyde_only`** specifically (2 of 3 runs at 0.0 recall) — inspect the hypothetical document HyDE generates for the raw (non-rewritten) phrasing of that question to understand why it sometimes misses the right chunk.
3. **Cost/latency-aware rollout decision**: `full` costs ~$0.046/run and ~9.9 s mean latency vs. `hyde_only`'s ~$0.046/run and ~7.7 s. If production latency budgets are tight, re-evaluate whether `hyde_only`'s occasional #25 miss is an acceptable trade-off for the ~2.2 s saving.
4. **Extend n=3 to n≥5** for the two closest configs (`hyde_only` vs. `full`) before finalizing a permanent production default, given that context recall std for both is non-trivial (0.0327 and 0.0000 respectively, but based on only 3 samples).

---

## Part B v1 — Archived, superseded

> **Superseded by v2 above.** This section is kept only for historical traceability of what was concluded before the generator's `temperature = 0.1` bug was identified and fixed. Do not cite these conclusions going forward — see the [Revision notes](#revision-notes-v1--v2) table above for what changed and why. Raw artifacts: `backend/tests/eval_results/TestsB_v1/`.

**Timestamps:** 2026-07-05T21:31–22:03 UTC (4 runs, 1 per configuration, generator `temperature = 0.1`).

| Exp | query_transform | hyde | Faithfulness | Answer Relevancy | Context Precision | Context Recall | Low-faith cases | Total cost | Mean latency |
| :-: | :-: | :-: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 `baseline` | ❌ | ❌ | 0.8673 | 0.8833 | 0.9567 | 0.9600 | 4 | $0.050045 | 7,936 ms |
| B2 `transform_only` | ✅ | ❌ | 0.8266 | 0.8646 | 0.9400 | 0.9200 | 6 | $0.052129 | 6,660 ms |
| B3 `hyde_only` | ❌ | ✅ | 0.8370 | 0.9194 | 0.9947 | 1.0000 | 5 | $0.054241 | 9,914 ms |
| B4 `full` | ✅ | ✅ | 0.8575 | 0.9077 | 0.9947 | 0.9200 | 5 | $0.052082 | 12,327 ms |

v1's headline conclusion at the time was: *"`hyde_only` is the best single-feature configuration and dominates `full` on context recall; disable query-transform in production."* As shown above, this specific claim about the query-transform/HyDE interaction and the `hyde_only` vs. `full` ranking **did not replicate** once the generator was fixed to `temperature = 0.0` and each configuration was repeated 3 times. The single most important v1 lesson that *did* survive is that **a single run per configuration is not sufficient to rank configurations that differ by a few hundredths of a faithfulness point** — which is exactly why v2 exists.
