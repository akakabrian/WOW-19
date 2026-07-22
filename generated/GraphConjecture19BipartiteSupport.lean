import FormalConjecturesUtil
import Mathlib.Tactic.NormNum

namespace SimpleGraph

open Classical

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Any explicit induced bipartite subgraph gives a lower bound for
`largestInducedBipartiteSubgraphSize`. -/
theorem card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
    {G : SimpleGraph α} {s : Finset α}
    (hs : (G.induce (s : Set α)).IsBipartite) :
    s.card ≤ largestInducedBipartiteSubgraphSize G := by
  classical
  unfold largestInducedBipartiteSubgraphSize
  apply le_csSup
  · exact ⟨Fintype.card α, by
      intro n hn
      rcases hn with ⟨t, _ht, rfl⟩
      exact Finset.card_le_univ t⟩
  · exact ⟨s, hs, rfl⟩

/-- Two disjoint independent finsets induce a bipartite graph on their union. -/
theorem induce_union_indep_isBipartite
    {G : SimpleGraph α} {A B : Finset α}
    (hA : G.IsIndepSet (A : Set α))
    (hB : G.IsIndepSet (B : Set α))
    (hdisj : Disjoint A B) :
    (G.induce ((A ∪ B : Finset α) : Set α)).IsBipartite := by
  classical
  let U : Set α := ((A ∪ B : Finset α) : Set α)
  let left : Set U := {x | x.1 ∈ A}
  let right : Set U := {x | x.1 ∈ B}
  change (G.induce U).IsBipartite
  refine (show (G.induce U).IsBipartiteWith left right from ?_).isBipartite
  constructor
  · rw [Set.disjoint_left]
    intro x hxA hxB
    exact (Finset.disjoint_left.mp hdisj hxA) hxB
  · intro x y hxy
    have hxmem : x.1 ∈ A ∪ B := x.2
    have hymem : y.1 ∈ A ∪ B := y.2
    rw [Finset.mem_union] at hxmem hymem
    rcases hxmem with hxA | hxB
    · rcases hymem with hyA | hyB
      · exact False.elim (hA hxA hyA (fun h => hxy.ne (Subtype.ext h)) hxy)
      · exact Or.inl ⟨hxA, hyB⟩
    · rcases hymem with hyA | hyB
      · exact Or.inr ⟨hxB, hyA⟩
      · exact False.elim (hB hxB hyB (fun h => hxy.ne (Subtype.ext h)) hxy)

/-- A shortest walk has no chord that skips at least one internal edge. -/
theorem shortest_walk_no_forward_chord
    {G : SimpleGraph α} {u v : α} (p : G.Walk u v)
    (hp_len : p.length = G.dist u v) {i j : ℕ}
    (hi : i ≤ p.length) (_hj : j ≤ p.length) (hgap : i + 1 < j) :
    ¬ G.Adj (p.getVert i) (p.getVert j) := by
  intro hadj
  let q : G.Walk u v := ((p.take i).concat hadj).append (p.drop j)
  have hq_len : q.length = i + 1 + (p.length - j) := by
    simp [q, SimpleGraph.Walk.length_append, SimpleGraph.Walk.length_concat,
      SimpleGraph.Walk.take_length, SimpleGraph.Walk.drop_length,
      Nat.min_eq_left hi]
  have hq_short : q.length < p.length := by
    rw [hq_len]
    omega
  have hdist_le : G.dist u v ≤ q.length := SimpleGraph.dist_le q
  omega

/-- A vertex together with any maximum independent subset of its neighbourhood
induces a bipartite star, giving a lower bound for the largest induced
bipartite subgraph. -/
theorem indepNeighborsCard_add_one_le_largestInducedBipartiteSubgraphSize
    {G : SimpleGraph α} (v : α) :
    indepNeighborsCard G v + 1 ≤ largestInducedBipartiteSubgraphSize G := by
  classical
  unfold largestInducedBipartiteSubgraphSize
  apply le_csSup
  · exact ⟨Fintype.card α, by
      intro n hn
      rcases hn with ⟨t, _ht, rfl⟩
      exact Finset.card_le_univ t⟩
  · unfold indepNeighborsCard
    obtain ⟨s, hs⟩ := (G.induce (G.neighborSet v)).exists_isNIndepSet_indepNum
    rw [SimpleGraph.isNIndepSet_iff] at hs
    let e : G.neighborSet v ↪ α := Function.Embedding.subtype _
    let leaves : Finset α := s.map e
    let t : Finset α := insert v leaves
    refine ⟨t, ?_, ?_⟩
    · refine (SimpleGraph.IsBipartiteWith.isBipartite
          (s := {x : (t : Set α) | x.1 = v})
          (t := {x : (t : Set α) | x.1 ∈ leaves}) ?_)
      constructor
      · rw [Set.disjoint_left]
        intro x hxv hxleaf
        dsimp at hxv hxleaf
        rw [Finset.mem_map] at hxleaf
        rcases hxleaf with ⟨w, _hw, hwx⟩
        change w.1 = x.1 at hwx
        have hadj : G.Adj v w.1 := w.2
        have : G.Adj v v := by
          simpa [hwx, hxv] using hadj
        exact G.irrefl this
      · intro x y hxy
        have hxyG : G.Adj x.1 y.1 := hxy
        have hxmem : x.1 ∈ t := x.2
        have hymem : y.1 ∈ t := y.2
        dsimp [t] at hxmem hymem
        rw [Finset.mem_insert] at hxmem hymem
        rcases hxmem with hxv | hxleaf
        · left
          constructor
          · exact hxv
          · rcases hymem with hyv | hyleaf
            · exfalso
              have : G.Adj v v := by
                simpa [hxv, hyv] using hxyG
              exact G.irrefl this
            · exact hyleaf
        · rcases hymem with hyv | hyleaf
          · right
            exact ⟨hxleaf, hyv⟩
          · exfalso
            rw [Finset.mem_map] at hxleaf hyleaf
            rcases hxleaf with ⟨a, ha, hax⟩
            rcases hyleaf with ⟨b, hb, hby⟩
            change a.1 = x.1 at hax
            change b.1 = y.1 at hby
            have habAdj : (G.induce (G.neighborSet v)).Adj a b := by
              change G.Adj a.1 b.1
              rwa [hax, hby]
            by_cases hab : a = b
            · subst hab
              exact G.irrefl habAdj
            · exact (hs.1 ha hb (fun h => hab h)) habAdj
    · dsimp [t, leaves]
      rw [Finset.card_insert_of_notMem]
      · rw [Finset.card_map]
        exact congrArg Nat.succ hs.2
      · simp only [Finset.mem_map, not_exists, not_and]
        intro w _hw hwv
        change w.1 = v at hwv
        have hadj : G.Adj v w.1 := w.2
        have : G.Adj v v := by
          rwa [hwv] at hadj
        exact G.irrefl this

end SimpleGraph
