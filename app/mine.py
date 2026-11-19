"""Milestone 2: exact frequent itemset mining (Apriori, counted with bitsets).

Technique from the drill: an itemset is frequent if it appears in at least min_support of the procedures; every subset of
a frequent itemset is frequent too (monotone), so size k+1 candidates are built only from frequent size-k sets. Each supply
gets one Python int whose bit i is set when procedure i used it, so the support of a set is the popcount of an AND.
"""
import math
from itertools import combinations


def bitsets(baskets: list[list[str]]) -> dict[str, int]:
    bits: dict[str, int] = {}
    for i, basket in enumerate(baskets):
        for item in basket:
            bits[item] = bits.get(item, 0) | (1 << i)
    return bits


def frequent_itemsets(baskets: list[list[str]], min_support: float, max_size: int = 4) -> dict[frozenset, float]:
    """{itemset: support} for every itemset of up to max_size items with support >= min_support."""
    n = len(baskets)
    need = max(1, math.ceil(min_support * n - 1e-9))
    bits = bitsets(baskets)
    level = {frozenset([i]): b for i, b in bits.items() if b.bit_count() >= need}
    result = {s: b.bit_count() / n for s, b in level.items()}
    size = 1
    while level and size < max_size:
        size += 1
        keys = sorted(level, key=sorted)
        next_level: dict[frozenset, int] = {}
        for a, b in combinations(keys, 2):
            union = a | b
            if len(union) != size or union in next_level:
                continue
            if any(union - {x} not in level for x in union):  # Apriori pruning
                continue
            joint = level[a] & level[b]
            if joint.bit_count() >= need:
                next_level[union] = joint
        level = next_level
        result.update({s: b.bit_count() / n for s, b in level.items()})
    return result


def support_of(baskets: list[list[str]], items) -> float:
    items = set(items)
    return sum(items <= set(b) for b in baskets) / len(baskets)
