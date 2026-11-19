from itertools import combinations

from app.data import HIDDEN, generate_procedures
from app.mine import frequent_itemsets, support_of


def brute_force(baskets, min_support, max_size):
    items = sorted({i for b in baskets for i in b})
    out = {}
    for k in range(1, max_size + 1):
        for combo in combinations(items, k):
            s = support_of(baskets, combo)
            if s >= min_support:
                out[frozenset(combo)] = s
    return out


def test_small_example_by_hand():
    baskets = [["bread", "milk"], ["bread", "sugar", "tea"], ["milk", "sugar", "tea"], ["bread", "milk", "sugar", "tea"], ["bread"], ["milk"]]
    found = frequent_itemsets(baskets, 0.5)
    assert found[frozenset(["bread"])] == 4 / 6
    assert found[frozenset(["sugar", "tea"])] == 3 / 6
    assert frozenset(["bread", "sugar"]) not in found      # only 2 of 6


def test_matches_brute_force_on_a_random_log():
    baskets = [r["supplies"] for r in generate_procedures(400, seed=3)]
    sub = [[s for s in b if s in set(sum([h["items"] for h in HIDDEN], ()))] for b in baskets]
    sub = [b for b in sub if b]
    assert frequent_itemsets(sub, 0.04, 4) == brute_force(sub, 0.04, 4)


def test_exact_threshold_is_inclusive():
    baskets = [["a"]] * 1 + [["b"]] * 9
    assert frozenset(["a"]) in frequent_itemsets(baskets, 0.1)
