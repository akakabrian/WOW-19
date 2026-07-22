# WOW II Conjecture 19 — Status

## STATUS

**MATHEMATICALLY PROVEN; EXACT LEAN 4.27 KERNEL CHECK RUNNING.**

The conjecture is classified as true. A complete human proof and a pinned no-placeholder Lean certificate have been audited. The only remaining completion gate is compilation of the generated definition-preserving port under the current Formal Conjectures toolchain, followed by independent review.

## STATEMENT

Authoritative theorem, preserved unchanged in `authoritative/GraphConjecture19.lean`:

```lean
theorem conjecture19 (G : SimpleGraph α) [Nontrivial α] (h_conn : G.Connected) :
    ⌊(∑ v ∈ Finset.univ, ((G.eccent v).toNat : ℝ)) / (Fintype.card α : ℝ) +
      sSup (Set.range (indepNeighbors G))⌋ ≤ b G := by
  sorry
```

Exact current definitions at Formal Conjectures commit
`e923379e609b9d5987011a1d1f06ec22ea25cd20`:

- `indepNeighbors G v = ((G.induce (G.neighborSet v)).indepNum : ℝ)`.
- `b G` is the real cast of the supremal cardinality of a vertex finset inducing a bipartite graph.
- `G.eccent v` is Mathlib's extended-natural eccentricity and the theorem applies `.toNat` before averaging.

**PROVEN:** formal statement matches the mathematical quantity used in the proof.

**OPEN:** none in the statement audit.

**NEXT:** retain exact theorem text in the generated compiled artifact.

## SEARCH

The exact finite evaluator tests

```text
floor((sum of eccentricities)/|V| + max_v alpha(G[N(v)])) <= b(G).
```

Search corpus:

| Corpus | Tested | Counterexamples | Equality cases |
|---|---:|---:|---:|
| All connected unlabeled graphs of orders 2–7 | 995 | 0 | 599 |
| Targeted dense/extremal families through order 16 | 538 | 0 | 157 |
| Seeded random connected graphs, orders 8–12 | 1,500 | 0 | 279 |
| **Total** | **3,033** | **0** | **1,035** |

Minimum observed margin was zero. The implementation is in `search/search_conjecture19.py`; the fixed random seed is `190019`.

**PROVEN:** no counterexample in the stated, reproducible corpus.

**OPEN:** finite search is supporting evidence, not the proof.

**NEXT:** retain the script and exact parameters with any submission package.

## PROOF

Let

- `d = diam(G)`,
- `λ = max_v α(G[N(v)])`, and
- `ē` be the average eccentricity.

A diameter-path window construction proves

```text
b(G) >= d + λ - 1.
```

Since `ē <= d`:

1. If `ē < d`, integrality gives `floor(ē + λ) <= d + λ - 1`, so the structural bound applies.
2. If `ē = d`, every vertex is diametral. Choose a vertex attaining `λ`, a maximum independent subset of its neighborhood, and a diametral geodesic starting there. Delete the first path neighbor and combine the remaining path with the independent neighborhood set. The parity coloring yields an induced bipartite subgraph of order `d + λ`.

A detailed argument, including the full short-window lemma rather than treating it as an assumption, is in `HUMAN_PROOF.md`.

**PROVEN:** complete human proof.

**OPEN:** none mathematically.

**NEXT:** compare the generated Lean witness construction line-by-line against this proof during independent review.

## LEAN

Pinned audited proof source:

- AMRA commit: `e4e339e5b380375cf1c7838251966d0fc3c06929`
- Original certificate toolchain: Lean 4.26 / mathlib `2df2f0150c275ad53cb3c90f7c98ec15a56a1a67`
- Current target toolchain: Lean 4.27 / mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`

`script/generate_lean_port.py` (path: `scripts/generate_lean_port.py`) creates three isolated modules inside a fresh pinned Formal Conjectures checkout:

1. `GraphConjecture19BipartiteSupport.lean`
2. `GraphConjecture19Conjecture13Support.lean`
3. `GraphConjecture19Solved.lean`

The generator:

- uses current upstream `b`, `indepNeighborsCard`, and `indepNeighbors` definitions;
- does not import the current upstream Conjecture 13 placeholder, whose body still contains `sorry`;
- removes the AMRA-only duplicate aliases;
- preserves the authoritative final theorem without an added `DecidableRel` assumption;
- rejects generated files containing `sorry`, `admit`, or `axiom`.

The workflow `.github/workflows/lean.yml` checks out exact commits, downloads the Mathlib cache, runs `lake env lean` on the generated final artifact, and publishes all generated source and logs to branch `ci-results`.

**PROVEN:** pinned certificate source has no textual `sorry`, `admit`, or custom `axiom`; exact-definition rewrite has been statically audited.

**OPEN:** current Lean 4.27 kernel result has not yet been published by CI.

**NEXT:** inspect `ci-results`; patch only concrete compiler errors; require exit code zero.

## REVIEW

Adversarial checks completed:

- Tested complete, multipartite, odd-cycle, wheel, friendship, join, and random dense/sparse families.
- Rechecked the floor/integrality split.
- Rechecked the path-window cardinality loss and both independent color classes.
- Verified the equality branch does not assume the maximizing local-independence vertex is peripheral; equality of average eccentricity with diameter proves every vertex is peripheral.
- Verified current upstream `b` and `indepNeighbors` semantics match the proof certificate.

**PROVEN:** no mathematical contradiction or hidden proof assumption found.

**OPEN:** independent Lean 4.27 build and source review after CI passes.

**NEXT:** have a second reviewer reproduce the pinned checkout and `lake env lean` command.

## SUBMISSION

No upstream branch, PR, issue, maintainer contact, or submission has been created for Conjecture 19.

The current repository is an isolated work/evidence repository supplied by Brian.

**PROVEN:** no upstream publication action taken.

**OPEN:** submission approval and reviewer-ready packaging.

**NEXT:** after kernel success and independent review, label the result **candidate solved** and ask Brian before any upstream action.
