# WOW II Conjecture 19

Isolated research workspace for decisively classifying and formally proving Written on the Wall II Conjecture 19.

## Current classification

**Mathematically proven; exact Lean 4.27 / current Formal Conjectures kernel check in progress.**

The authoritative target is preserved unchanged:

```lean
theorem conjecture19 (G : SimpleGraph α) [Nontrivial α] (h_conn : G.Connected) :
    ⌊(∑ v ∈ Finset.univ, ((G.eccent v).toNat : ℝ)) / (Fintype.card α : ℝ) +
      sSup (Set.range (indepNeighbors G))⌋ ≤ b G := by
  sorry
```

This repository does **not** modify the shared Formal Conjectures checkout. CI creates fresh pinned checkouts of:

- `google-deepmind/formal-conjectures`
- `chainstart/amra`

It then generates an isolated, no-`sorry` port of the audited proof and kernel-checks it under the Formal Conjectures toolchain.

## Evidence

- No counterexample among 3,033 reproducibly tested connected graphs.
- Human proof in `HUMAN_PROOF.md`.
- Exact progress and trust boundaries in `STATUS.md`.
- Reproducible finite search in `search/search_conjecture19.py`.
- Lean port generator in `scripts/generate_lean_port.py`.

## Integrity rules

- Preserve the upstream theorem statement.
- No `sorry`, `admit`, custom axioms, or hidden theorem-strengthening assumptions.
- No upstream PR or maintainer contact without Brian's explicit approval.
- A successful CI run is a candidate solution, pending independent review.
