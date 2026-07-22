# WOW II Conjecture 19 — Status

## STATUS

**MATHEMATICALLY PROVEN; LEAN 4.27 PORT PREPARED; KERNEL EXECUTION BLOCKED.**

The conjecture is classified as true. The human proof is complete, the counterexample search is reproducible, and a deterministic port from the pinned no-placeholder Lean certificate to the current Formal Conjectures definitions is committed here.

The only unmet gate is an actual Lean 4.27 kernel run followed by independent review.

## STATEMENT

The authoritative statement is preserved unchanged in `authoritative/GraphConjecture19.lean`.

Current pinned Formal Conjectures semantics:

- `indepNeighbors G v` is the real cast of the independence number of the graph induced by `N(v)`.
- `b G` is the real cast of the largest induced-bipartite vertex-set cardinality.
- `G.eccent v` is converted with `.toNat` before averaging.

**PROVEN:** exact statement and definitions audited.

**OPEN:** none.

**NEXT:** compile the unchanged final theorem.

## SEARCH

Exact search corpus:

| Corpus | Tested | Counterexamples | Equality cases |
|---|---:|---:|---:|
| Connected unlabeled graphs, orders 2–7 | 995 | 0 | 599 |
| Targeted extremal families through order 16 | 538 | 0 | 157 |
| Seeded random connected graphs, orders 8–12 | 1,500 | 0 | 279 |
| **Total** | **3,033** | **0** | **1,035** |

The search was rerun twice after the original run. The preserved JSON outputs were byte-for-byte identical:

```text
34d231ca3f5544dcdae2439c54c3237282e19a45e2db0286176b716fd80bd2dc
```

See `search/search_conjecture19.py` and `search/SEARCH_RESULTS.md`.

**PROVEN:** no counterexample in the recorded corpus.

**OPEN:** search is supporting evidence, not the universal proof.

**NEXT:** retain the script, parameters, and hash.

## PROOF

Let `d` be the diameter, `λ` the maximum neighborhood independence number, and `ē` the average eccentricity.

A diameter-path window construction proves

```text
b(G) >= d + λ - 1.
```

Because `ē <= d`:

1. If `ē < d`, integrality gives `floor(ē + λ) <= d + λ - 1`.
2. If `ē = d`, every vertex is diametral. Starting a diametral geodesic at a vertex attaining `λ`, delete its first neighbor and combine the remaining path with a maximum independent subset of its neighborhood. Parity gives an induced bipartite subgraph of order `d + λ`.

The complete short-window construction is in `HUMAN_PROOF.md`.

**PROVEN:** complete human proof.

**OPEN:** none mathematically.

**NEXT:** independent proof review after formal compilation.

## LEAN

Pinned sources:

- Formal Conjectures: `e923379e609b9d5987011a1d1f06ec22ea25cd20`
- AMRA certificate: `e4e339e5b380375cf1c7838251966d0fc3c06929`
- Target toolchain: Lean 4.27, mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`

`scripts/generate_lean_port.py` creates three isolated modules and preserves the exact final theorem. It uses the current definitions, avoids the upstream Conjecture 13 placeholder, removes duplicate aliases, and rejects proof placeholders.

`scripts/run_port_ci.sh` fetches the exact commits, generates the modules, downloads the Mathlib cache, runs `lake env lean`, and writes a complete result bundle.

### Execution blocker

These trigger paths were tested:

- pushes to `main`;
- branch creation;
- a scheduled full build;
- repeated scheduled one-step smoke jobs.

None produced a workflow run, status check, result branch, or compiler transcript. Therefore this is a repository Actions/event-execution blocker, not a Lean compilation failure.

Temporary schedules and the smoke workflow were removed. `.github/workflows/lean.yml` now has only explicit push and manual triggers.

**PROVEN:** pinned certificate and generated-source transformation are statically audited; all required structural helpers are included.

**OPEN:** one actual Lean 4.27 kernel run.

**NEXT:** enable repository Actions and manually run **Lean kernel check**, or execute `bash scripts/run_port_ci.sh` from a networked clone. Require `failed_phase=none` and `exit_code=0`.

## REVIEW

Adversarial review checked the floor split, equality case, short-window cardinality, parity classes, path chords, current definition equivalence, and generated dependency closure. No mathematical gap was found.

**PROVEN:** mathematical review complete.

**OPEN:** independent Lean build and source review.

**NEXT:** reproduce the exact pinned build after the kernel run passes.

## SUBMISSION

No upstream pull request, issue, branch, maintainer contact, or submission was created.

**PROVEN:** stop gate respected.

**OPEN:** kernel pass, independent review, and Brian's approval.

**NEXT:** only after those gates, use the label **CANDIDATE SOLVED**.
