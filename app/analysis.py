"""Milestones 3 and 4: rank the frequent itemsets, then compare them with what independence would predict.

Baseline expectation: if supplies were used independently, a set of items would appear in n * prod(item supports)
procedures. lift = observed support / expected support. Lift near 1 means the set is just popular items meeting by chance;
a high lift means the items really are used together.

Obvious vs surprising: a set is OBVIOUS when one procedure type explains it (every item is in that type's core supply list,
or all items are in one category); otherwise it is SURPRISING if its lift is high, and CHANCE if its lift is low.
"""
from app.data import CATEGORY_OF, PROCEDURES


def top_itemsets(itemsets: dict[frozenset, float], n: int = 15, min_size: int = 2) -> list[tuple[frozenset, float]]:
    """The n most supported itemsets of at least min_size items, best first (ties by name, so output is stable)."""
    pairs = [(s, v) for s, v in itemsets.items() if len(s) >= min_size]
    return sorted(pairs, key=lambda p: (-p[1], sorted(p[0])))[:n]


def expected_support(itemsets: dict[frozenset, float], items) -> float:
    p = 1.0
    for i in items:
        p *= itemsets[frozenset([i])]
    return p


def lift(itemsets: dict[frozenset, float], items) -> float:
    items = frozenset(items)
    return itemsets[items] / expected_support(itemsets, items)


def explained_by_one_procedure(items) -> str | None:
    for name, (_, core) in PROCEDURES.items():
        if set(items) <= set(core):
            return name
    return None


def classify(itemsets: dict[frozenset, float], items, high_lift: float = 3.0) -> str:
    items = frozenset(items)
    if explained_by_one_procedure(items) or len({CATEGORY_OF[i] for i in items}) == 1:
        return "obvious"
    return "surprising" if lift(itemsets, items) >= high_lift else "chance"


def maximal(itemsets: dict[frozenset, float], keep) -> list[frozenset]:
    "Itemsets in keep that are not strictly contained in another set of keep (so a bundle is listed once, at full size)."
    keep = list(keep)
    return [s for s in keep if not any(s < t for t in keep)]


def bundles(itemsets: dict[frozenset, float], gain: float = 1.5) -> list[frozenset]:
    """Itemsets of 2+ items in which EVERY item earns its place: dropping any one lowers the lift by at least a factor of gain.

    This keeps "ondansetron + blanket + probe" but drops "ondansetron + blanket + probe + gloves": gloves are in most
    procedures, so adding them leaves the lift unchanged. Singletons have lift 1 by definition.
    """
    keep = []
    for s in itemsets:
        if len(s) < 2:
            continue
        parts = [s - {i} for i in s]
        if all(lift(itemsets, s) >= gain * (lift(itemsets, p) if len(p) > 1 else 1.0) for p in parts):
            keep.append(s)
    return keep


def describe(itemsets: dict[frozenset, float], items) -> dict:
    items = frozenset(items)
    return {"items": sorted(items), "size": len(items), "support": itemsets[items],
            "expected": expected_support(itemsets, items), "lift": lift(itemsets, items), "kind": classify(itemsets, items)}
