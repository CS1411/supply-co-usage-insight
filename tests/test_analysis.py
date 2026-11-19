import pytest

from app.analysis import classify, describe, lift, maximal, top_itemsets
from app.data import HIDDEN, generate_procedures
from app.mine import frequent_itemsets


@pytest.fixture(scope="module")
def found():
    return frequent_itemsets([r["supplies"] for r in generate_procedures(5000)], 0.03)


def test_top_itemsets_are_sorted_and_have_at_least_two_items(found):
    top = top_itemsets(found, 10)
    assert len(top) == 10 and all(len(s) >= 2 for s, _ in top)
    assert [v for _, v in top] == sorted((v for _, v in top), reverse=True)


def test_lift_is_one_for_independent_items_and_high_for_a_hidden_bundle(found):
    assert lift(found, ["Sterile Gloves", "Gauze Pads"]) == pytest.approx(1.0, abs=0.15)
    assert lift(found, HIDDEN[0]["items"]) > 5


def test_hidden_bundles_are_all_recovered_and_called_surprising(found):
    for bundle in HIDDEN:
        items = frozenset(bundle["items"])
        assert items in found, bundle
        assert classify(found, items) == "surprising"
        assert found[items] == pytest.approx(bundle["share"], abs=0.02)


def test_a_procedure_core_is_called_obvious(found):
    assert classify(found, ["Gauze Pads", "Adhesive Dressing"]) == "obvious"
    assert describe(found, ["Gauze Pads", "Adhesive Dressing"])["size"] == 2


def test_maximal_keeps_only_the_largest_sets():
    a, b, c = frozenset("x"), frozenset("xy"), frozenset("z")
    assert set(maximal({}, [a, b, c])) == {b, c}
