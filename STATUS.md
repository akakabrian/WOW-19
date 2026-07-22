# WOW II Conjecture 19 — Status

## STATUS

**MATHEMATICALLY PROVEN; LEAN 4.27 SOURCE PORT GENERATED; CORRECTED KERNEL BUILD PENDING.**

The conjecture is classified as true. The human proof is complete, the search is reproducible, and the exact current-definition port has reached Lean 4.27 CI.

## STATEMENT

The authoritative theorem is preserved unchanged in `authoritative/GraphConjecture19.lean`.

Current pinned semantics:

- `indepNeighbors G v` is the real cast of the induced-neighborhood independence number.
- `b G` is the real cast of the largest induced-bipartite order.
- `G.eccent v` is converted with `.toNat` before averaging.

**PROVEN:** exact statement and definitions audited.

**OPEN:** none.

**NEXT:** kernel-check this unchanged final theorem.

## SEARCH

| Corpus | Tested | Counterexamples | Equality cases |
|---|---:|---:|---:|
| Connected unlabeled graphs, orders 2–7 | 995 | 0 | 599 |
| Targeted extremal families through order 16 | 538 | 0 | 157 |
| Seeded random connected graphs, orders 8–12 | 1,500 | 0 | 279 |
| **Total** | **3,033** | **0** | **1,035** |

The search was rerun twice after the original run. Preserved JSON SHA256:

```text
34d231ca3f5544dcdae2439c54c3237282e19a45e2db0286176b716fd80bd2dc
```

See `search/search_conjecture19.py` and `search/SEARCH_RESULTS.md`.

**PROVEN:** no counterexample in the recorded corpus.

**OPEN:** search is supporting evidence, not the universal proof.

**NEXT:** retain the exact script and parameters.

## PROOF

Let `d` be the diameter, `λ` the maximum neighborhood independence number, and `ē` the average eccentricity.

A diameter-path short-window construction proves

```text
b(G) >= d + λ - 1.
```

If `ē < d`, integrality gives `floor(ē + λ) <= d + λ - 1`. If `ē = d`, every vertex is diametral; a maximum independent neighborhood set plus a diametral path with its first neighbor deleted induces a bipartite subgraph of order `d + λ`.

See `HUMAN_PROOF.md` for the full proof.

**PROVEN:** complete human proof.

**OPEN:** none mathematically.

**NEXT:** independent source review after formal compilation.

## LEAN

Pinned sources:

- Formal Conjectures: `e923379e609b9d5987011a1d1f06ec22ea25cd20`
- AMRA certificate: `e4e339e5b380375cf1c7838251966d0fc3c06929`
- Target: Lean 4.27 / mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`

`scripts/generate_lean_port.py` creates:

1. `GraphConjecture19BipartiteSupport.lean`
2. `GraphConjecture19Conjecture13Support.lean`
3. `GraphConjecture19Solved.lean`

The generator uses current upstream definitions, avoids the upstream Conjecture 13 placeholder, preserves the exact theorem without an extra assumption, and rejects `sorry`, `admit`, or `axiom`.

### First Lean 4.27 CI result

The following phases passed:

- install Lean 4.27;
- fetch both exact source commits;
- generate all three modules;
- forbidden-marker scan;
- record the exact environment;
- download and unpack the pinned Mathlib cache.

The first kernel phase failed before elaborating any theorem because it invoked the final source with direct `lake env lean`; the imported newly generated modules had not yet been built, producing:

```text
unknown module prefix 'FormalConjectures'
```

This was an invocation error, not a source-level Lean error. `scripts/run_port_ci.sh` now uses the canonical target:

```bash
lake build FormalConjectures.WrittenOnTheWallII.GraphConjecture19Solved
```

A corrected clean rerun has been queued. All temporary recurring schedules have been removed.

**PROVEN:** exact source generation succeeds under the Lean 4.27 workflow and produces no forbidden markers.

**OPEN:** result of the corrected Lake module build.

**NEXT:** inspect the next `ci-results/lean-build.log`; patch only concrete Lean compiler errors or record exit code zero.

## REVIEW

Adversarial review checked the floor split, equality case, window cardinality, parity classes, path chords, current-definition equivalence, and generated dependency closure.

**PROVEN:** no mathematical gap found.

**OPEN:** independent Lean build and final source review.

**NEXT:** reproduce the exact build after it passes.

## SUBMISSION

No upstream pull request, issue, branch, maintainer contact, or submission was created.

**PROVEN:** stop gate respected.

**OPEN:** kernel pass, independent review, and Brian's approval.

**NEXT:** only after those gates, use the label **CANDIDATE SOLVED**.
