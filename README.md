# PTW-friction

A friction-first **Play to Win** strategy workshop for [Claude Code](https://claude.com/claude-code) — six personas with private evidence dossiers, adversarial cross-examination of the Choice Cascade, fiction-firewalled Remember-the-Future, and mechanically ranked WWHTBT assumption mapping with a mandatory demand check. Plus a companion skill that renders the result as a readable HTML report.

Based on the *Play to Win* framework by A.G. Lafley and Roger L. Martin (Harvard Business Review Press, 2013).

## What's in here

Two Claude Code skills, self-contained, no external dependencies beyond Python 3's standard library:

- **`/PTW-friction`** — the workshop itself. Give it documents and organizational context; it partitions the evidence into six private dossiers (CEO, CFO, Head of Product, Tech Lead, Employee Rep, CRO), runs blind openings → cross-examination → concede-or-hold, a fiction-firewalled "Remember the Future" hypothesis pass, and a mechanically ranked assumption map (`scripts/rank_assumptions.py`). Ends in a Choice Cascade draft, a Collision Log of unresolved disagreements, a ranked assumption map, and gated experiments — not a consensus document.
- **`/ptw-friction-report`** — reads a finished `/PTW-friction` run's `PTW-draft-final.md` and renders it as a standalone HTML page (own template and styling; only the web fonts load from Google Fonts) — sectioned, with a jump-to table of contents, tables for the Capabilities and Assumption-Ranking sections, and the Collision Log rendered as stacked, attributed quotes so the disagreements stay visible instead of blending together.

See [`.claude/skills/PTW-friction/SKILL.md`](.claude/skills/PTW-friction/SKILL.md) and [`.claude/skills/PTW-friction/README.md`](.claude/skills/PTW-friction/README.md) (design rationale, v1-vs-v2 comparison) for how the workshop itself works.

## Use it

Drop the `.claude/skills/` folder into any project (or clone this repo and run `claude` inside it), then:

```
/PTW-friction
```

Follow the prompts — it will ask for documents and context, and walk through checkpoints you confirm along the way. When it finishes:

```
/ptw-friction-report
```

This finds the most recent run under `./PTW-friction/output/*/7_final/PTW-draft-final.md` and writes `PTW-Report.html` next to it.

## Why "friction"

Multi-perspective simulations tend to fail in a specific way: several lenses on the same document converge into a single, comfortable story, invented details drift downstream as if they were evidence, and the assumption that mattered most quietly loses its top-5 ranking to an arithmetic mistake nobody checked. This design makes those failure modes structurally difficult rather than just discouraged — see the README inside the skill folder for the audit that drove the design and how to compare it against the plain multi-perspective version.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- `python3` (standard library only — no `pip install`)
