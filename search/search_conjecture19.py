#!/usr/bin/env python3
"""Reproducible counterexample search for WOW II Conjecture 19.

For each finite connected simple graph G with at least two vertices, compute exactly:
  avg_ecc_num / n  (ordinary eccentricity; equals ENat.toNat for connected finite G),
  L = max_v alpha(G[N(v)]),
  b = max{|S| : G[S] is bipartite},
and test floor(avg_ecc + L) <= b.

The exact integer test avoids floating point:
  floor(avg_ecc_num / n + L) = (avg_ecc_num + n*L) // n.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import networkx as nx


@dataclass(frozen=True)
class Result:
    name: str
    n: int
    m: int
    ecc_sum: int
    max_local_alpha: int
    lhs_floor: int
    b: int
    margin: int
    graph6: str
    edges: list[tuple[int, int]]


def canonicalize(G: nx.Graph) -> nx.Graph:
    return nx.convert_node_labels_to_integers(G, ordering="sorted")


def adjacency_masks(G: nx.Graph) -> list[int]:
    n = G.number_of_nodes()
    masks = [0] * n
    for u, v in G.edges():
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return masks


def alpha_of_mask_exact(adj: list[int], initial_mask: int) -> int:
    memo: dict[int, int] = {0: 0}

    def rec(mask: int) -> int:
        cached = memo.get(mask)
        if cached is not None:
            return cached
        bits = mask
        best_v = (bits & -bits).bit_length() - 1
        best_deg = -1
        while bits:
            bit = bits & -bits
            bits ^= bit
            v = bit.bit_length() - 1
            deg = (adj[v] & mask).bit_count()
            if deg > best_deg:
                best_deg = deg
                best_v = v
        without_v = mask & ~(1 << best_v)
        ans = max(rec(without_v), 1 + rec(without_v & ~adj[best_v]))
        memo[mask] = ans
        return ans

    return rec(initial_mask)


def max_local_alpha_exact(G: nx.Graph) -> int:
    adj = adjacency_masks(G)
    return max(alpha_of_mask_exact(adj, adj[v]) for v in range(G.number_of_nodes()))


def is_bipartite_mask(adj: list[int], subset: int) -> bool:
    colored0 = 0
    colored1 = 0
    unseen = subset
    while unseen:
        root = unseen & -unseen
        unseen ^= root
        colored0 |= root
        todo = root
        while todo:
            bit = todo & -todo
            todo ^= bit
            v = bit.bit_length() - 1
            nbrs = adj[v] & subset
            if colored0 & bit:
                if nbrs & colored0:
                    return False
                new = nbrs & ~(colored0 | colored1)
                colored1 |= new
            else:
                if nbrs & colored1:
                    return False
                new = nbrs & ~(colored0 | colored1)
                colored0 |= new
            unseen &= ~new
            todo |= new
    return True


def subset_masks_of_size(n: int, k: int):
    for combo in itertools.combinations(range(n), k):
        mask = 0
        for v in combo:
            mask |= 1 << v
        yield mask


def max_induced_bipartite_order_exact(G: nx.Graph) -> int:
    n = G.number_of_nodes()
    adj = adjacency_masks(G)
    for k in range(n, -1, -1):
        for subset in subset_masks_of_size(n, k):
            if is_bipartite_mask(adj, subset):
                return k
    raise AssertionError("unreachable")


def evaluate(G: nx.Graph, name: str) -> Result:
    G = canonicalize(G)
    n = G.number_of_nodes()
    if n < 2 or not nx.is_connected(G):
        raise ValueError("Conjecture requires a connected nontrivial graph")
    ecc = nx.eccentricity(G)
    ecc_sum = sum(ecc.values())
    local = max_local_alpha_exact(G)
    lhs = (ecc_sum + n * local) // n
    b = max_induced_bipartite_order_exact(G)
    graph6 = nx.to_graph6_bytes(G, header=False).decode().strip()
    return Result(
        name=name,
        n=n,
        m=G.number_of_edges(),
        ecc_sum=ecc_sum,
        max_local_alpha=local,
        lhs_floor=lhs,
        b=b,
        margin=b-lhs,
        graph6=graph6,
        edges=sorted((min(u, v), max(u, v)) for u, v in G.edges()),
    )


def complete_multipartite(parts: tuple[int, ...]) -> nx.Graph:
    return nx.complete_multipartite_graph(*parts)


def join_graph(G: nx.Graph, H: nx.Graph) -> nx.Graph:
    J = nx.disjoint_union(G, H)
    nG = G.number_of_nodes()
    nH = H.number_of_nodes()
    J.add_edges_from((u, nG + v) for u in range(nG) for v in range(nH))
    return J


def friendship_graph(k: int) -> nx.Graph:
    return nx.complete_graph(3) if k == 1 else nx.windmill_graph(k, 3)


def targeted_graphs() -> Iterable[tuple[str, nx.Graph]]:
    for n in range(2, 31):
        yield f"complete_K{n}", nx.complete_graph(n)
    for n in range(3, 31):
        yield f"cycle_C{n}", nx.cycle_graph(n)
    for n in range(4, 31):
        yield f"wheel_W{n}", nx.wheel_graph(n)
    for k in range(1, 15):
        yield f"friendship_F{k}", friendship_graph(k)
    seen: set[tuple[int, ...]] = set()
    for r in range(2, 6):
        for parts in itertools.combinations_with_replacement(range(1, 9), r):
            if sum(parts) <= 16 and parts not in seen:
                seen.add(parts)
                yield "K_" + "_".join(map(str, parts)), complete_multipartite(parts)
    for a in range(2, 9):
        for b in range(2, 9):
            if a + b <= 16:
                yield f"join_C{a}_I{b}", join_graph(nx.cycle_graph(a), nx.empty_graph(b))
                yield f"join_K{a}_I{b}", join_graph(nx.complete_graph(a), nx.empty_graph(b))


def run_atlas() -> tuple[list[Result], dict[int, int]]:
    results: list[Result] = []
    counts: dict[int, int] = {}
    for idx, G in enumerate(nx.graph_atlas_g()):
        n = G.number_of_nodes()
        if n >= 2 and nx.is_connected(G):
            counts[n] = counts.get(n, 0) + 1
            results.append(evaluate(G, f"atlas_{idx}"))
    return results, counts


def run_targeted(max_exact_n: int = 16) -> list[Result]:
    results: list[Result] = []
    for name, G in targeted_graphs():
        if G.number_of_nodes() <= max_exact_n:
            results.append(evaluate(G, name))
    return results


def run_random(seed: int, samples_per_pair: int, n_values: list[int], ps: list[float]) -> list[Result]:
    rng = random.Random(seed)
    results: list[Result] = []
    for n in n_values:
        for p in ps:
            accepted = 0
            attempts = 0
            while accepted < samples_per_pair and attempts < samples_per_pair * 100:
                attempts += 1
                graph_seed = rng.randrange(2**32)
                G = nx.gnp_random_graph(n, p, seed=graph_seed)
                if nx.is_connected(G):
                    results.append(evaluate(G, f"Gnp_n{n}_p{p}_seed{graph_seed}"))
                    accepted += 1
            if accepted < samples_per_pair:
                raise RuntimeError(f"Could only get {accepted} connected samples for n={n}, p={p}")
    return results


def summarize(results: list[Result]) -> dict:
    witnesses = [r for r in results if r.margin < 0]
    sharp = [r for r in results if r.margin == 0]
    min_margin = min((r.margin for r in results), default=None)
    return {
        "tested": len(results),
        "counterexamples": len(witnesses),
        "sharp": len(sharp),
        "min_margin": min_margin,
        "smallest_counterexample": asdict(min(witnesses, key=lambda r: (r.n, r.m, r.graph6))) if witnesses else None,
        "first_sharp": [asdict(r) for r in sorted(sharp, key=lambda r: (r.n, r.m, r.graph6))[:20]],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("search_results.json"))
    parser.add_argument("--random-seed", type=int, default=190019)
    parser.add_argument("--random-samples", type=int, default=100)
    args = parser.parse_args()

    atlas, atlas_counts = run_atlas()
    targeted = run_targeted(max_exact_n=16)
    random_results = run_random(
        seed=args.random_seed,
        samples_per_pair=args.random_samples,
        n_values=[8, 9, 10, 11, 12],
        ps=[0.25, 0.5, 0.75],
    )
    all_results = atlas + targeted + random_results
    payload = {
        "semantics": {
            "lhs_floor": "(sum eccentricities + n * max_v alpha(G[N(v)])) // n",
            "rhs_b": "maximum cardinality of S such that induced G[S] is bipartite",
            "connected_note": "For finite connected G, Lean ENat eccentricity .toNat equals ordinary finite graph eccentricity.",
        },
        "environment": {"python": __import__("sys").version, "networkx": nx.__version__},
        "parameters": {
            "atlas": "all connected unlabeled graphs in networkx graph_atlas_g (orders 2 through 7)",
            "atlas_counts": atlas_counts,
            "targeted_max_n": 16,
            "random_seed": args.random_seed,
            "random_samples_per_(n,p)": args.random_samples,
            "random_n": [8, 9, 10, 11, 12],
            "random_p": [0.25, 0.5, 0.75],
        },
        "atlas_summary": summarize(atlas),
        "targeted_summary": summarize(targeted),
        "random_summary": summarize(random_results),
        "overall_summary": summarize(all_results),
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload["parameters"], indent=2))
    print("ATLAS", json.dumps(payload["atlas_summary"], indent=2))
    print("TARGETED", json.dumps(payload["targeted_summary"], indent=2))
    print("RANDOM", json.dumps(payload["random_summary"], indent=2))
    print("OVERALL", json.dumps(payload["overall_summary"], indent=2))


if __name__ == "__main__":
    main()
