# Human Proof — WOW II Conjecture 19

Let `G` be a finite connected nontrivial graph. Put

- `d = diam(G)`,
- `λ = max_v α(G[N(v)])`, and
- `ē = |V(G)|⁻¹ ∑_v ecc(v)`.

We prove

```text
floor(ē + λ) ≤ b(G),
```

where `b(G)` is the maximum order of an induced bipartite subgraph.

## Lemma: the diameter/local-independence bound

We first prove

```text
b(G) ≥ d + λ - 1.                      (1)
```

Fix a vertex `v`, and let `A⊆N(v)` be an independent set of maximum size in its neighborhood. Take a diametral geodesic

```text
P : x₀,x₁,…,x_d.
```

Define the close-index window

```text
Q = {i∈{0,…,d} : dist(v,x_i)≤2}.
```

For `i,j∈Q`, geodesicity gives `dist(x_i,x_j)=|i-j|`, while the route through `v` has length at most four. Hence `|i-j|≤4`, so `Q` occupies at most five path positions.

Choose `T⊆Q` so that all its indices have the same parity, every `i∈T` satisfies `dist(v,x_i)=2`, and `|Q|-|T|≤3`:

- if `|Q|≤3`, take `T=∅`;
- if `|Q|=4`, the extreme indices differ by at least three, so they cannot both be within distance one of `v`; take an extreme at distance two;
- if `|Q|=5`, the extremes differ by four, forcing both distances to equal two; take both, which have the same parity.

Retain the indices

```text
I = ({0,…,d} \ Q) ∪ T.
```

Let `c` be the common parity of `T` (choose either parity if `T` is empty). Define

```text
L = A ∪ {x_i : i∈I and i has parity 1-c},
R = {v} ∪ {x_i : i∈I and i has parity c}.
```

Both sets are independent. Same-parity vertices on a geodesic are nonadjacent. The set `A` is independent. A retained parity-`c` path vertex is either outside `Q`, hence farther than two from `v`, or belongs to `T`, hence is exactly distance two; in either case it is not adjacent to `v`. A retained opposite-parity index never belongs to `T`, so it is outside `Q`; if its path vertex were adjacent to some `a∈A`, then `v-a-x_i` would be a path of length two, a contradiction.

The selected vertices are disjoint by their distances from `v`. Because the geodesic is simple and at most three close indices remain deleted,

```text
|{x_i:i∈I}| = (d+1)-|Q|+|T| ≥ d-2.
```

Thus the induced bipartite subgraph on `L∪R` has at least

```text
(d-2)+|A|+1 = d+|A|-1
```

vertices. Choose `v` attaining `λ`; this proves (1).

## Main inequality

Every vertex has eccentricity at most `d`, hence `ē≤d`.

### Case 1: `ē<d`

Since `d` and `λ` are integers,

```text
floor(ē+λ) ≤ d+λ-1.
```

By (1), `d+λ-1≤b(G)`, proving the result.

### Case 2: `ē=d`

All eccentricities are at most `d`, so equality of their average forces every vertex to have eccentricity `d`.

Choose `v` with `α(G[N(v)])=λ`, and choose an independent set `A⊆N(v)` of size `λ`. Since `ecc(v)=d`, take a geodesic

```text
x₀=v,x₁,…,x_d.
```

Let

```text
S = A ∪ {x₀,x₂,x₃,…,x_d}.
```

This disjoint union has size `λ+d`. Color each retained path vertex by the parity of its index, and place every vertex of `A` in the odd color class. Same-parity geodesic vertices are nonadjacent; `A` is independent; and if `a∈A` were adjacent to an odd `x_i` with `i≥3`, then `v-a-x_i` would contradict `dist(v,x_i)=i`. Hence `G[S]` is bipartite, and

```text
b(G) ≥ |S| = d+λ = floor(ē+λ).
```

The two cases prove WOW II Conjecture 19.
