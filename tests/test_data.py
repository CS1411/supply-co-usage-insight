from app.data import CATEGORY_OF, PROCEDURES, SKUS, BACKGROUND, HIDDEN, generate_procedures, load_procedures, save_procedures


def test_every_referenced_supply_is_a_known_sku():
    used = set(BACKGROUND) | {s for _, core in PROCEDURES.values() for s in core} | {s for b in HIDDEN for s in b["items"]}
    assert used <= set(SKUS)
    assert len(SKUS) == len(set(SKUS)) == len(CATEGORY_OF)


def test_procedures_are_reproducible_and_sorted():
    a, b = generate_procedures(300, seed=1), generate_procedures(300, seed=1)
    assert a == b and a != generate_procedures(300, seed=2)
    assert all(r["supplies"] == sorted(set(r["supplies"])) and r["supplies"] for r in a)


def test_core_supplies_follow_their_procedure_type():
    rows = [r for r in generate_procedures(4000) if r["type"] == "Cast application"]
    share = sum("Cast Padding" in r["supplies"] for r in rows) / len(rows)
    assert 0.95 < share <= 1.0


def test_save_and_load_round_trip(tmp_path):
    rows = generate_procedures(50)
    save_procedures(rows, str(tmp_path / "p.jsonl"))
    assert load_procedures(str(tmp_path / "p.jsonl")) == rows
