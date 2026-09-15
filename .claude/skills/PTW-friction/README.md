# PTW-friction — design rationale and comparison guide

Successor to `/PTW-workshop`. The v1 skill stays untouched so runs can be compared in hindsight. This redesign responds to an audit of a v1 pilot run (2026-07) and to a control-vs-friction boardroom-simulation experiment.

## What the audit found in v1

1. **Harmonization (moderate):** four of five personas converged on the same cascade; the sharpest dissent (Employee: "candidates are a product with good marketing") arrived structurally late (Pair C) and was never treated as blocking. Root cause: five lenses on identical information — framing diversity, not information diversity.
2. **Fiction leak:** the assumption scoring cited "Jordan's retrospective" (a Remember-the-Future invention) as an engineering estimate.
3. **Ranking error:** the willingness-to-pay assumption (C3, I=17, K=7) scored 221 by the file's own I×(20−K) formula — higher than C2's 216 — yet was demoted to a "secondary" footnote while C2 made the top 5. Nothing checked the arithmetic, so the paying-customer assumption lost its experiment slot.
4. **No demand seat:** the CFO asked good WTP questions, but no seat owned them; the source document's one hard demand signal (an employer leaving over candidate quality) was never elevated.
5. **v1 strengths kept:** the WWHTBT reverse engineering, the status-quo check, and the experiment designs were the best parts of v1 — v2 keeps all three and armors them.

## The design changes, mapped

| v1 failure | v2 mechanism |
|---|---|
| Lens diversity ≠ information diversity | **Step 0b partition**: every material fact goes to exactly one of six private dossiers; personas read only their slice + a shared brief. |
| Consensus-seeking pairs | **Cross-examination + concede-or-hold** replaces pairs; no blended resolutions; unresolved clashes preserved verbatim in a Collision Log. |
| Fiction leak | **Fiction firewall**: mandatory `[FICTION]` header; only legal export is hypotheses → assumptions with `origin: fiction`, capped at Knowledge ≤ 6 by the script. |
| Ranking error | **`scripts/rank_assumptions.py`** computes quadrants and rankings arithmetically from `assumptions.json`; agents may not re-rank in prose; nothing is silently dropped. |
| No demand seat | **CRO persona (Robin)** with attack duty, plus a **mandatory demand check** in the script that warns if no willingness-to-pay assumption exists or none makes the top 5. |
| Evidence gaps invisible | **Step 0b evidence-gaps.md**: dossier questions the documents can't answer are documented gaps and become assumptions. Authoring the dossiers *is* diligence. |

## How to compare in hindsight

Run both skills on the same input documents (v1 → `./PTW-workshop/output/`, v2 → `./PTW-friction/output/`) and compare:

- **Divergence count** at the opening stage — contradictions, not emphasis differences.
- **Collision survival**: disagreements reaching the final draft unresolved (v2 Collision Log) vs. synthesized away (v1 "both are partly right").
- **Provenance integrity**: sample evidence citations in the final cascade; count claims tracing only to Remember-the-Future fiction.
- **Demand question**: rank of the highest willingness-to-pay assumption in Quadrant B (the v2 script reports this; in that v1 run it was a footnote).
- **Actionability**: experiments with falsification criteria written before anyone is invested, and next steps gated on evidence events.

Cost note: v2 runs ~20 sub-agents vs. v1's ~16, plus a heavier facilitator role in Step 0b. The partition step is slower by design — that's where the evidence inventory gets built.
