# Reproduced counterexample search

Command:

```bash
python3 -m pip install 'networkx==3.6.1'
python3 search/search_conjecture19.py --out search_results.json
```

Environment used for the independent rerun:

- Python `3.13.5`
- NetworkX `3.6.1`
- Fixed random seed `190019`

## Exact corpus

| Corpus | Tested | Counterexamples | Equality cases |
|---|---:|---:|---:|
| All connected unlabeled graphs in NetworkX's graph atlas, orders 2–7 | 995 | 0 | 599 |
| Targeted complete, multipartite, cycle, wheel, friendship, and join families through order 16 | 538 | 0 | 157 |
| Seeded random connected graphs, orders 8–12, p in {0.25, 0.5, 0.75}, 100 per pair | 1,500 | 0 | 279 |
| **Total** | **3,033** | **0** | **1,035** |

Minimum observed margin `b(G) - floor(avgEcc(G) + maxLocalAlpha(G))` was `0`.

The original and independent rerun JSON files were byte-for-byte identical:

```text
SHA256 34d231ca3f5544dcdae2439c54c3237282e19a45e2db0286176b716fd80bd2dc
```

Source script SHA256:

```text
SHA256 a2dcc32010168e2533efee9f904f7142f1cd71b8eb1f69cd05f6a47661b7a1d6
```

This enumeration is supporting evidence only. The proof does not depend on it.
