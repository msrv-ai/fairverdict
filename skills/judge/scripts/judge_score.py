#!/usr/bin/env python3
"""Impartial-judge scorer: weighted totals, gap drivers, robustness checks.

Usage:  python3 judge_score.py scores.json

scores.json:
{
  "criteria": [{"name": "Time to MVP", "weight": 60}, {"name": "Ecosystem", "weight": 40}],
  "scores": {
    "Flutter":      {"Time to MVP": 9, "Ecosystem": {"score": 7, "confidence": "low"}},
    "React Native": {"Time to MVP": 8, "Ecosystem": 9}
  },
  "disqualified": {"Xamarin": "support ended May 2024"}
}
Scores are 0-10. Confidence: high | medium (default) | low.
"""
import json
import random
import sys

NOISE = {"high": 0.5, "medium": 1.0, "low": 1.5}  # score jitter (std dev) by confidence
SIMS = 5000
CONCENTRATION = 30  # weight jitter: a 30% weight typically moves by about +/-8 points


def fail(msg):
    sys.exit("error: " + msg)


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    crits = [(c["name"], float(c["weight"])) for c in data["criteria"]]
    if not crits or any(w <= 0 for _, w in crits):
        fail("each criterion needs a positive weight")
    total = sum(w for _, w in crits)
    if abs(total - 100) > 0.5:
        print(f"note: weights summed to {total:g}; normalized to 100\n")
    weights = {name: w / total for name, w in crits}
    dq = data.get("disqualified") or {}
    cands = {}
    for cand, row in data["scores"].items():
        if cand in dq:
            continue
        unknown = set(row) - set(weights)
        if unknown:
            fail(f"{cand}: unknown criteria {sorted(unknown)}")
        cells = {}
        for name in weights:
            if name not in row:
                fail(f"missing score: {cand} / {name}")
            v = row[name]
            if isinstance(v, dict):
                score, conf = v.get("score"), v.get("confidence", "medium")
            else:
                score, conf = v, "medium"
            score = float(score)
            if not 0 <= score <= 10:
                fail(f"{cand} / {name}: score {score:g} is outside 0-10")
            if conf not in NOISE:
                fail(f"{cand} / {name}: confidence must be high, medium or low")
            cells[name] = (score, conf)
        cands[cand] = cells
    if len(cands) < 2:
        fail("need at least two candidates that are not disqualified")
    return weights, cands, dq


def r0(x):
    return int(x + 0.5 + 1e-9)  # round half up, so 52.5 shows as 53


def totals(cands, weights):
    return {c: 10 * sum(w * cells[n][0] for n, w in weights.items()) for c, cells in cands.items()}


def leaders(tot, order):
    return [c for c in order if tot[order[0]] - tot[c] < 0.05]  # everyone tied for first


def ranked(tot):
    return sorted(tot, key=lambda c: (-tot[c], c))


def reweight(weights, factor):
    w = {n: v * factor(n) for n, v in weights.items()}
    w = {n: v for n, v in w.items() if v > 0}
    s = sum(w.values())
    return {n: v / s for n, v in w.items()}


def simulate(cands, weights):
    rng = random.Random(42)  # fixed seed: same input, same output
    names = list(weights)
    wins = dict.fromkeys(cands, 0.0)
    for _ in range(SIMS):
        g = [rng.gammavariate(CONCENTRATION * weights[n], 1.0) for n in names]
        gs = sum(g)
        w = [x / gs for x in g]
        tot = {}
        for c, cells in cands.items():
            tot[c] = sum(wi * min(10.0, max(0.0, cells[n][0] + rng.gauss(0, NOISE[cells[n][1]])))
                         for wi, n in zip(w, names))
        best = max(tot.values())
        best_ones = [c for c, t in tot.items() if t == best]
        for c in best_ones:
            wins[c] += 1 / len(best_ones)
    return {c: v / SIMS for c, v in wins.items()}


def main():
    if len(sys.argv) != 2:
        fail("usage: python3 judge_score.py scores.json")
    weights, cands, dq = load(sys.argv[1])
    names = list(weights)
    tot = totals(cands, weights)
    order = ranked(tot)
    win = simulate(cands, weights)
    first, second = order[0], order[1]
    lead = tot[first] - tot[second]
    share = win[first]
    top = leaders(tot, order)
    if len(top) > 1:
        shares = ", ".join(f"{c} {win[c]:.0%}" for c in top)
        print(f"VERDICT: exact tie between {' and '.join(top)} at {r0(tot[first])}/100 | "
              f"TOO CLOSE TO CALL | simulation wins: {shares}\n")
    else:
        if share >= 0.80 and lead >= 5:
            strength = "CLEAR (wins >= 80% and leads by >= 5)"
        elif share < 0.55 or lead < 3:
            why = [text for text, hit in ((f"lead {lead:.1f} < 3", lead < 3),
                                          (f"wins {share:.1%} < 55%", share < 0.55)) if hit]
            strength = "TOO CLOSE TO CALL (" + "; ".join(why) + ")"
        else:
            strength = "WITH CAVEATS (between the clear and too-close thresholds)"
        print(f"VERDICT: {first} {r0(tot[first])}/100 | {strength} | lead over {second}: "
              f"{lead:.1f} pts | wins {share:.1%} of {SIMS} simulations\n")

    print("## Leaderboard")
    print("| # | Candidate | Score /100 | Wins in simulations |")
    print("|---|---|---|---|")
    for c in order:
        rank = 1 + sum(1 for d in order if tot[d] - tot[c] >= 0.05)  # ties share a rank
        print(f"| {rank} | {c} | {r0(tot[c])} | {win[c]:.0%} |")
    for c, why in dq.items():
        print(f"| ⛔ | {c} | — | disqualified: {why} |")

    print("\n## Score matrix (0-10, * = low confidence)")
    print("| Criterion (weight) | " + " | ".join(order) + " |")
    print("|---|" + "---|" * len(order))
    for n in names:
        cells = [f"{cands[c][n][0]:g}{'*' if cands[c][n][1] == 'low' else ''}" for c in order]
        print(f"| {n} ({weights[n]:.0%}) | " + " | ".join(cells) + " |")
    print("| **Total /100** | " + " | ".join(f"**{r0(tot[c])}**" for c in order) + " |")

    print(f"\n## Gap drivers: {first} vs {second} (weighted points)")
    gaps = sorted(((10 * weights[n] * (cands[first][n][0] - cands[second][n][0]), n) for n in names),
                  reverse=True)
    for d, n in gaps:
        if abs(d) >= 0.05:
            print(f"{d:+.1f}  {n}: {cands[first][n][0]:g} vs {cands[second][n][0]:g}")

    print("\n## Winner under other weightings")
    scenarios = [("Equal weights", {n: 1 / len(names) for n in names})]
    if len(names) > 1:
        scenarios += [(f"Without '{n}'", reweight(weights, lambda k, n=n: 0 if k == n else 1))
                      for n in names]
        scenarios += [(f"'{n}' counts double", reweight(weights, lambda k, n=n: 2 if k == n else 1))
                      for n in names]
    flips = []
    for label, w in scenarios:
        t = totals(cands, w)
        r = ranked(t)
        tied = leaders(t, r)
        if len(tied) > 1:
            print(f"- {label}: tie {' = '.join(tied)} ({r0(t[r[0]])})")
        else:
            print(f"- {label}: {r[0]} ({r0(t[r[0]])}, +{t[r[0]] - t[r[1]]:.1f} over {r[1]})")
        if tied != [first]:
            flips.append(label + (" (tie)" if len(tied) > 1 else f" ({r[0]})"))
    print("Winner changes or ties under: " + ("; ".join(flips) if flips else "none of these"))
    print(f"\nSimulation: {SIMS} runs; weights jittered around the given ones (Dirichlet, "
          f"concentration {CONCENTRATION}); scores jittered by confidence "
          f"(SD high {NOISE['high']}, medium {NOISE['medium']}, low {NOISE['low']}).")


if __name__ == "__main__":
    main()
