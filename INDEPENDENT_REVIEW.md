# WOW II Conjecture 19 — Independent Final Review

## Verdict

**CANDIDATE SOLVED.**

This review was performed after the successful Lean 4.27 CI run and did not rely on the earlier narrative classification. It rechecked the theorem statement, generated proof artifact, dependency boundary, compiler transcript, and integrity hashes.

## Statement identity

The authoritative theorem in `authoritative/GraphConjecture19.lean` is:

```lean
theorem conjecture19 (G : SimpleGraph α) [Nontrivial α] (h_conn : G.Connected) :
    ⌊(∑ v ∈ Finset.univ, ((G.eccent v).toNat : ℝ)) / (Fintype.card α : ℝ) +
      sSup (Set.range (indepNeighbors G))⌋ ≤ b G := by
```

The generated final theorem in the passing `ci-results` artifact has the same namespace, variables, hypotheses, expression, and conclusion. No extra `DecidableRel`, nonemptiness, or stronger graph assumption was added.

## Trust boundary

The final module imports only the generated support chain. It does not import either authoritative theorem placeholder or the upstream Conjecture 13 theorem containing `sorry`.

The generated Conjecture 13 support proves its diameter/local-independence inequality from an explicit per-vertex induced-bipartite witness. The Conjecture 19 proof then handles the two average-eccentricity cases and bridges the exact upstream definitions.

## Kernel evidence

Pinned environment:

- Formal Conjectures: `e923379e609b9d5987011a1d1f06ec22ea25cd20`
- AMRA source certificate: `e4e339e5b380375cf1c7838251966d0fc3c06929`
- Lean: `4.27.0`
- Mathlib: `a3a10db0e9d66acbebf76c5e6a135066525ac900`

Passing CI result:

```text
failed_phase=none
exit_code=0
Build completed successfully (8040 jobs).
```

The generated modules passed the workflow's scan for `sorry`, `admit`, and `axiom`. The final generated source hash is:

```text
9cf7465ebb1a9d11b9b954ed4f6a14c7a81ae3b4fd2d041f84cc01d7762815f1
```

The compiler emitted copyright-header linter warnings only. No theorem, elaboration, typeclass, tactic, or kernel error remained.

## Mathematical review

The proof architecture was rechecked independently:

1. Average eccentricity is at most diameter.
2. In the strict case, integrality lowers the floor target to `diam + maxLocalIndependence - 1`.
3. The short-window geodesic construction supplies an induced bipartite witness of that size.
4. In the equality case, every vertex has eccentricity equal to diameter.
5. Choosing a local-independence maximizer and a diametral geodesic from it yields an induced bipartite witness of size `diam + maxLocalIndependence`.
6. The supremum and real-cast bridges match the current Formal Conjectures definitions.

No missing case, circular use of Conjecture 19, or reliance on the upstream Conjecture 13 placeholder was found.

## Supporting finite search

The preserved evaluator tested 3,033 connected graphs across exhaustive small graphs, targeted extremal families, and seeded random graphs. It found no counterexample. This is supporting evidence only; the universal classification rests on the proved theorem.

## Remaining gate

No mathematical or formal-proof gate remains in this repository.

The only remaining action is external process: obtain a separate human or model review if desired, then ask Brian before any upstream submission, PR, issue, or maintainer contact.
