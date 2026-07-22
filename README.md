# WOW II Conjecture 19

Isolated research workspace for decisively classifying and formally proving Written on the Wall II Conjecture 19.

## Current classification

**CANDIDATE SOLVED.**

The mathematical proof is complete, the exact authoritative theorem has passed a Lean 4.27 kernel check under the pinned current Formal Conjectures environment, and the final adversarial source/evidence review is recorded in `INDEPENDENT_REVIEW.md`.

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

It then generates an isolated no-placeholder port of the audited proof and kernel-checks it under Lean 4.27.

## Formal certificate

Passing CI result on branch `ci-results`:

```text
failed_phase=none
exit_code=0
Build completed successfully (8040 jobs).
```

Final generated theorem SHA256:

```text
9cf7465ebb1a9d11b9b954ed4f6a14c7a81ae3b4fd2d041f84cc01d7762815f1
```

## Evidence

- No counterexample among 3,033 reproducibly tested connected graphs.
- Complete human proof in `HUMAN_PROOF.md`.
- Final status and trust boundaries in `STATUS.md`.
- Independent final review in `INDEPENDENT_REVIEW.md`.
- Reproducible finite search in `search/search_conjecture19.py`.
- Deterministic Lean port generator in `scripts/generate_lean_port.py`.
- Complete generated sources, build transcript, environment record, and hashes on branch `ci-results`.

## Integrity rules

- Preserve the upstream theorem statement exactly.
- No `sorry`, `admit`, custom axioms, or hidden theorem-strengthening assumptions in the proof certificate.
- Do not rely on the upstream Conjecture 13 placeholder.
- No upstream PR, issue, branch, submission, or maintainer contact without Brian's explicit approval.
