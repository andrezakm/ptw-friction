#!/usr/bin/env python3
"""Mechanically rank WWHTBT assumptions into quadrants.

Usage: python3 rank_assumptions.py <assumptions.json>

Input: JSON array of objects with fields:
  id             short key, e.g. "C3"
  statement      full assumption statement
  dimension      customer | industry | position | competitor | other
  importance     0-20 (how dependent is the strategy on this being true)
  knowledge      0-20 (how much evidence do we currently have)
  origin         evidence | inference | fiction
  demand_related true if the assumption concerns willingness to pay,
                 committed revenue, or real customer demand

Output (stdout, markdown): warnings, Quadrant A (I>10, K>=10) ranked by
I*K desc, Quadrant B (I>10, K<10) ranked by I*(20-K) desc, excluded list,
and a demand-assumption check. The agent that wrote the JSON may NOT
re-rank or re-quadrant in prose; this output is canonical.
"""
import json
import sys


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        die("usage: rank_assumptions.py <assumptions.json>")
    try:
        with open(sys.argv[1]) as f:
            items = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        die(f"cannot read {sys.argv[1]}: {e}")
    if not isinstance(items, list) or not items:
        die("input must be a non-empty JSON array")

    required = ("id", "statement", "dimension", "importance", "knowledge",
                "origin", "demand_related")
    warnings = []
    for a in items:
        missing = [k for k in required if k not in a]
        if missing:
            die(f"assumption {a.get('id', '?')} missing fields: {missing}")
        for k in ("importance", "knowledge"):
            if not isinstance(a[k], (int, float)) or not 0 <= a[k] <= 20:
                die(f"{a['id']}: {k} must be a number in 0-20")
        if a["origin"] not in ("evidence", "inference", "fiction"):
            die(f"{a['id']}: origin must be evidence|inference|fiction")
        # Fiction firewall: an invented future cannot count as knowledge.
        if a["origin"] == "fiction" and a["knowledge"] > 6:
            warnings.append(
                f"{a['id']}: origin=fiction but knowledge={a['knowledge']} — "
                f"fiction cannot justify K>6; capped to 6")
            a["knowledge"] = 6

    ids = [a["id"] for a in items]
    if len(ids) != len(set(ids)):
        die("duplicate assumption ids")

    qualified = [a for a in items if a["importance"] > 10]
    excluded = [a for a in items if a["importance"] <= 10]
    qa = sorted((a for a in qualified if a["knowledge"] >= 10),
                key=lambda a: (-(a["importance"] * a["knowledge"]), a["id"]))
    qb = sorted((a for a in qualified if a["knowledge"] < 10),
                key=lambda a: (-(a["importance"] * (20 - a["knowledge"])), a["id"]))

    print("# Assumption Ranking (canonical — computed, not judged)\n")
    if warnings:
        print("## Warnings")
        for w in warnings:
            print(f"- {w}")
        print()

    def table(rows, score_label, score_fn):
        print(f"| Rank | ID | Assumption | Dim | Origin | I | K | {score_label} |")
        print("|---|---|---|---|---|---|---|---|")
        for i, a in enumerate(rows, 1):
            stmt = a["statement"].replace("|", "/")
            print(f"| {i} | {a['id']} | {stmt} | {a['dimension']} | "
                  f"{a['origin']} | {a['importance']} | {a['knowledge']} | "
                  f"{score_fn(a)} |")
        print()

    print(f"## Quadrant A — Important & Known ({len(qa)})")
    print("*Lean on these; monitor them as canaries.*\n")
    table(qa, "IxK", lambda a: a["importance"] * a["knowledge"])

    print(f"## Quadrant B — Important & Unknown ({len(qb)})")
    print("*Bets placed in the dark. Top 5 require experiments before commitment.*\n")
    table(qb, "Ix(20-K)", lambda a: a["importance"] * (20 - a["knowledge"]))

    if excluded:
        print(f"## Excluded (importance <= 10) — {len(excluded)}, listed so nothing is silently dropped")
        for a in excluded:
            print(f"- {a['id']} (I={a['importance']}, K={a['knowledge']}): {a['statement']}")
        print()

    print("## Demand check")
    demand_b = [i for i, a in enumerate(qb, 1) if a["demand_related"]]
    demand_any = [a for a in items if a["demand_related"]]
    if not demand_any:
        print("- WARNING: no demand_related assumption exists AT ALL. "
              "The paying-customer question was never converted into an "
              "assumption. This is a known blind spot — go back and add it.")
    elif not demand_b:
        print("- NOTE: demand_related assumptions exist but none landed in "
              "Quadrant B — verify their Knowledge scores cite actual "
              "willingness-to-pay evidence (money, contracts, paid pilots), "
              "not enthusiasm.")
    else:
        top5 = [r for r in demand_b if r <= 5]
        if top5:
            print(f"- OK: demand_related assumption(s) in Quadrant B top 5 "
                  f"(rank {top5}).")
        else:
            print(f"- WARNING: highest demand_related assumption ranks "
                  f"#{demand_b[0]} in Quadrant B — outside the top 5 that "
                  f"get experiments. Check the scores before accepting this.")


if __name__ == "__main__":
    main()
