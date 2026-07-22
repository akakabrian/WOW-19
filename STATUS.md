# WOW II Conjecture 19 — Status

## STATUS

**CANDIDATE SOLVED.**

The conjecture is mathematically proved and the unchanged authoritative theorem has been kernel-checked successfully under the pinned current Formal Conjectures environment.

## STATEMENT

The source-of-truth theorem remains unchanged in `authoritative/GraphConjecture19.lean`:

```lean
theorem conjecture19 (G : SimpleGraph α) [Nontrivial α] (h_conn : G.Connected) :
    ⌊(∑ v ∈ Finset.univ, ((G.eccent v).toNat : ℝ)) / (Fintype.card α : ℝ) +
      sSup (Set.range (indepNeighbors G))⌋ ≤ b G := by
```

Current definitions were audited:

- `indepNeighbors G v` is the real cast of the independence number of the graph induced by the open neighborhood of `v`.
- `b G` is the real cast of the largest induced-bipartite vertex-set cardinality.
- `G.eccent v` is converted using `.toNat` before averaging.

**PROVEN:** generated final theorem matches the authoritative theorem exactly.

**OPEN:** none.

**NEXT:** preserve this statement unchanged in any submission.

## SEARCH

| Corpus | Tested | Counterexamples | Equality cases |
|---|---:|---:|---:|
| Connected unlabeled graphs, orders 2–7 | 995 | 0 | 599 |
| Targeted extremal families through order 16 | 538 | 0 | 157 |
| Seeded random connected graphs, orders 8–12 | 1,500 | 0 | 279 |
| **Total** | **3,033** | **0** | **1,035** |

The search was reproduced after the original run. Preserved result SHA256:

```text
34d231ca3f5544dcdae2439c54c3237282e19a45e2db0286176b716fd80bd2dc
```

**PROVEN:** no counterexample in the reproducible corpus.

**OPEN:** none relevant to the universal classification; search is supporting evidence.

**NEXT:** retain the script, fixed seed, parameters, and result hash.

## PROOF

Let `d` be the diameter, `λ` the maximum neighborhood independence number, and `ē` the average eccentricity.

The structural proof constructs an induced bipartite subgraph showing

```text
b(G) >= d + λ - 1.
```

Then:

1. If `ē < d`, integrality gives `floor(ē + λ) <= d + λ - 1`.
2. If `ē = d`, every vertex is diametral. At a vertex attaining `λ`, a maximum independent neighborhood set combined with a diametral geodesic with its first neighbor removed yields an induced bipartite subgraph of order `d + λ`.

The complete argument, including the geodesic short-window construction, is in `HUMAN_PROOF.md`.

**PROVEN:** complete human proof.

**OPEN:** none mathematically.

**NEXT:** use `INDEPENDENT_REVIEW.md` as the final adversarial-review record.

## LEAN

Pinned environment:

- Formal Conjectures: `e923379e609b9d5987011a1d1f06ec22ea25cd20`
- AMRA source certificate: `e4e339e5b380375cf1c7838251966d0fc3c06929`
- Lean: `4.27.0`
- Mathlib: `a3a10db0e9d66acbebf76c5e6a135066525ac900`

The deterministic generator produces:

1. `GraphConjecture19BipartiteSupport.lean`
2. `GraphConjecture19Conjecture13Support.lean`
3. `GraphConjecture19Solved.lean`

It uses the current upstream definitions, avoids the upstream Conjecture 13 placeholder, preserves the exact theorem without an extra assumption, and rejects generated files containing `sorry`, `admit`, or `axiom`.

Passing CI certificate on branch `ci-results`:

```text
Repository commit: 57d6f1efbd57158ea661e568dfa901c16a8abb73
failed_phase: none
exit_code: 0
Build completed successfully (8040 jobs).
```

Final generated theorem SHA256:

```text
9cf7465ebb1a9d11b9b954ed4f6a14c7a81ae3b4fd2d041f84cc01d7762815f1
```

The only compiler messages at completion were non-fatal copyright-header linter warnings.

**PROVEN:** unchanged authoritative theorem kernel-checks under Lean 4.27 with no proof placeholders.

**OPEN:** none in the formal proof.

**NEXT:** preserve the passing CI result, generated sources, build log, and hashes.

## REVIEW

`INDEPENDENT_REVIEW.md` rechecked:

- exact theorem identity;
- absence of additional hypotheses;
- no import of the upstream Conjecture 19 or Conjecture 13 placeholders;
- proof dependency closure;
- strict and equality branches;
- path-window cardinality and parity coloring;
- current-definition equivalence;
- successful kernel transcript and source hashes.

**PROVEN:** final adversarial source and evidence review passed.

**OPEN:** an additional external human/model review is optional, not a mathematical or kernel gate.

**NEXT:** request external review before or during submission if desired.

## SUBMISSION

No upstream pull request, issue, branch, maintainer contact, or submission has been created.

**PROVEN:** publication stop gate respected.

**OPEN:** Brian's approval for any upstream action.

**NEXT:** do not submit or contact maintainers until Brian explicitly approves.
