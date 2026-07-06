# RAG Pipeline — Experiment History — Index

This experiment log is split into two files because it covers two different kinds of experiments:

- **[Part A — Prompt Iteration](./EXPERIMENT_HISTORY_PART_A.md)**: a chronological, sequential log (7 runs). Each experiment tweaks one thing (a HyDE or query-rewrite prompt, or the reference ground truth) relative to the run before it, and is compared directly to that previous run.
- **[Part B — Ablation Study](./EXPERIMENT_HISTORY_PART_B_ablation.md)**: a controlled 2×2 ablation that isolates the *presence* of the `query_transform` and `hyde` pipeline steps, holding the prompt configuration fixed. This is a different experimental design (independent variables toggled against a shared control) and also newly logs token usage, cost, and latency per run. Part B has two revisions: **v1** (1 run per config, generator `temperature = 0.1`, archived/superseded) and **v2** (3 runs per config, generator `temperature = 0.0`, canonical — cite this one).

**Why keep them separate:** the two designs answer different questions (prompt wording vs. feature presence) and mixing their tables would make "comparison with previous experiment" ambiguous — Part A's comparisons are sequential, Part B's are all relative to its own `baseline` control. Part B also revises some of Part A's conclusions (see below), so keeping the two logs distinct in time makes that revision traceable.

## Important cross-references

**Part A concluded that hardening the query-rewrite prompt (Experiment 4) was the single highest-leverage change made.** Part B's ablation shows every Part A run using that hardened prompt also had HyDE enabled, so the two effects were never isolated. In isolation, `transform_only` does not clearly dominate — see Part B v2 below. Part A's own Experiments 5–7 already showed that a single run at a fixed configuration is not sufficient to certify a score, given generator sampling variance; this is the same lesson Part B later re-learned and fixed directly (see next point).

**Part B v1 was itself revised by Part B v2.** v1 ran with the generator (`backend/app/rag/generator.py`) still at `temperature = 0.1` and only 1 run per configuration; several of its conclusions (notably: "`hyde_only` dominates `full`", "query-transform + HyDE interact negatively on questions #22/#25") did not replicate once the generator was fixed to `temperature = 0.0` and each configuration was repeated 3 times. **v2 is the current source of truth for Part B.** See Part B's "Revision notes (v1 → v2)" table for the full list of what changed.

## Quick summary

| | Best Faithfulness | Best Context Recall | Recommended config |
| --- | --- | --- | --- |
| Part A | Exp 4 — 0.9135 (single run; 0.859–0.914 range on repeats) | Exp 4 — 1.0000 | Hardened query-rewrite + guardrailed HyDE prompts |
| Part B v2 (canonical, n=3, temp=0.0) | `full` — 0.8600 ± 0.0053 | `full` — 1.0000 ± 0.0000 | `full` (query_transform **on**, hyde **on**) |
| Part B v1 (archived, n=1, temp=0.1) | Baseline — 0.8673 | `hyde_only` — 1.0000 | *(superseded — see v2)* |

## A note on generator temperature

Part A's own repeat runs (Experiments 5–7) and Part B's v1 → v2 revision both point to the same root cause: `backend/app/rag/generator.py` ran with `temperature = 0.1` while `hyde.py` and `query_transformer.py` were already at `0.0`. Non-zero generator temperature was enough to swing faithfulness by up to ±0.05 between otherwise-identical runs, which made single-run comparisons across configurations unreliable. The generator has since been fixed to `temperature = 0.0`; Part B v2 was run under this fix with 3 repeats per configuration. **Any future experiment comparing configurations should use `temperature = 0.0` and at least 3 runs per configuration**, per this lesson.
