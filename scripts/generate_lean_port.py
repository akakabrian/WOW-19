#!/usr/bin/env python3
"""Generate an isolated no-placeholder Lean port of WOWII Conjecture 19.

The generator reads two pinned, audited AMRA proof modules and adapts them to
use the exact definitions already present in a pinned Formal Conjectures
checkout. It never edits the authoritative GraphConjecture19.lean file.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

FORBIDDEN = re.compile(r"\b(sorry|admit|axiom)\b")


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"missing source: {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path} ({text.count(chr(10)) + 1} lines)")


def check_clean(label: str, text: str) -> None:
    match = FORBIDDEN.search(text)
    if match:
        line = text.count("\n", 0, match.start()) + 1
        raise SystemExit(f"forbidden marker {match.group(0)!r} in {label}:{line}")


def make_bipartite_support(source: str) -> str:
    marker = "/-- Any explicit induced bipartite subgraph gives a lower bound for"
    start = source.find(marker)
    if start < 0:
        raise SystemExit("could not locate induced-bipartite support marker")
    end = source.rfind("\nend SimpleGraph")
    if end < start:
        raise SystemExit("could not locate final SimpleGraph namespace terminator")
    body = source[start:end].rstrip()
    result = f"""import FormalConjecturesForMathlib.Combinatorics.SimpleGraph.Independence
import FormalConjecturesForMathlib.Combinatorics.SimpleGraph.Induced
import Mathlib.Combinatorics.SimpleGraph.Diam
import Mathlib.Tactic.NormNum

namespace SimpleGraph

open Classical

variable {{α : Type*}} [Fintype α] [DecidableEq α]

{body}

end SimpleGraph
"""
    check_clean("GraphConjecture19BipartiteSupport.lean", result)
    return result


def make_conjecture13_support(source: str) -> str:
    old_import = (
        "import AmraLibrary.Combinatorics.SimpleGraph.GraphConjectures."
        "LargestInducedTree"
    )
    new_import = (
        "import FormalConjectures.WrittenOnTheWallII."
        "GraphConjecture19BipartiteSupport"
    )
    if old_import not in source:
        raise SystemExit("could not locate AMRA LargestInducedTree import")
    result = source.replace(old_import, new_import, 1)
    check_clean("GraphConjecture19Conjecture13Support.lean", result)
    return result


def remove_definition(source: str, name: str) -> str:
    pattern = re.compile(
        rf"\nnoncomputable def {re.escape(name)}\b.*?\n(?=(?:theorem|noncomputable def|end SimpleGraph))",
        re.DOTALL,
    )
    result, count = pattern.subn("\n", source, count=1)
    if count != 1:
        raise SystemExit(f"expected to remove exactly one definition of {name}, removed {count}")
    return result


def make_conjecture19(source: str) -> str:
    old_import = (
        "import AmraLibrary.Combinatorics.SimpleGraph.GraphConjectures."
        "WowiiConjecture13"
    )
    new_import = (
        "import FormalConjectures.WrittenOnTheWallII."
        "GraphConjecture19Conjecture13Support"
    )
    if old_import not in source:
        raise SystemExit("could not locate AMRA WOWII 13 import")
    source = source.replace(
        old_import,
        new_import + "\nimport FormalConjecturesUtil.Attributes.Basic",
        1,
    )

    # Formal Conjectures already owns these two public symbols. Keep the local
    # real-valued bridge, but use upstream `indepNeighbors` and `G.eccent` in
    # the final theorem.
    source = remove_definition(source, "indepNeighbors")
    source = remove_definition(source, "eccentricity")

    # Rewrite the eccentricity bridge itself to state the fact directly about
    # Mathlib's `G.eccent` rather than through AMRA's deleted alias.
    source = source.replace("eccentricity G v", "G.eccent v")
    source = source.replace("simpa [eccentricity, ← hw] using", "simpa [← hw] using")
    source = source.replace("rw [eccentricity, ← hw]", "rw [← hw]")
    source = source.replace("simpa [eccentricity] using", "simpa using")

    final_marker = (
        "\nend SimpleGraph\n\nopen Classical\nopen SimpleGraph\n\n"
        "theorem wowii19_formal_conjectures_original_shape"
    )
    cut = source.find(final_marker)
    if cut < 0:
        raise SystemExit("could not locate AMRA final theorem block")
    support = source[:cut] + "\nend SimpleGraph\n"

    exact_final = r'''

namespace WrittenOnTheWallII.GraphConjecture19

open Classical
open SimpleGraph

variable {α : Type*} [Fintype α] [DecidableEq α]

/--
WOWII Conjecture 19, with the authoritative Formal Conjectures statement
preserved exactly and proved without importing the upstream placeholder.
-/
@[category research open, AMS 5]
theorem conjecture19 (G : SimpleGraph α) [Nontrivial α] (h_conn : G.Connected) :
    ⌊(∑ v ∈ Finset.univ, ((G.eccent v).toNat : ℝ)) / (Fintype.card α : ℝ) +
      sSup (Set.range (indepNeighbors G))⌋ ≤ b G := by
  classical
  simpa [SimpleGraph.indepNeighbors, SimpleGraph.indepNeighborsReal,
    SimpleGraph.eccentricity_toNat_eq_vertexEccentricityNat (G := G) h_conn] using
    SimpleGraph.wowii19_distEcc_sSup_indepNeighborsReal (G := G) h_conn

end WrittenOnTheWallII.GraphConjecture19
'''
    result = support.rstrip() + exact_final
    check_clean("GraphConjecture19Solved.lean", result)

    required = [
        "theorem conjecture19 (G : SimpleGraph α) [Nontrivial α] (h_conn : G.Connected) :",
        "((G.eccent v).toNat : ℝ)",
        "sSup (Set.range (indepNeighbors G))⌋ ≤ b G := by",
    ]
    for needle in required:
        if needle not in result:
            raise SystemExit(f"generated final theorem is missing: {needle}")
    if "[DecidableRel G.Adj] (h_conn" in result:
        raise SystemExit("final theorem incorrectly retains a DecidableRel assumption")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal", type=Path, required=True)
    parser.add_argument("--amra", type=Path, required=True)
    args = parser.parse_args()

    amra_root = args.amra / "amra_library/formal/AmraLibrary"
    largest = read(
        amra_root
        / "Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean"
    )
    c13 = read(
        amra_root
        / "Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean"
    )
    c19 = read(
        amra_root
        / "OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean"
    )

    out = args.formal / "FormalConjectures/WrittenOnTheWallII"
    write(
        out / "GraphConjecture19BipartiteSupport.lean",
        make_bipartite_support(largest),
    )
    write(
        out / "GraphConjecture19Conjecture13Support.lean",
        make_conjecture13_support(c13),
    )
    write(out / "GraphConjecture19Solved.lean", make_conjecture19(c19))

    print("generated port is free of sorry/admit/axiom markers")


if __name__ == "__main__":
    main()
