from app.cli import main
from app.data import HIDDEN, generate_procedures
from app.mine import frequent_itemsets
from app.report import build_report, planted_recovery


def test_report_lists_every_hidden_bundle_as_surprising():
    found = frequent_itemsets([r["supplies"] for r in generate_procedures(5000)], 0.03)
    text = build_report(found, 5000, 0.03)
    surprising = text.split("## Surprising")[1].split("## Obvious")[0]
    for bundle in HIDDEN:
        assert " + ".join(sorted(bundle["items"])) in surprising
    assert all(got is not None for _, _, got in planted_recovery(found))
    assert "Sterile Gloves + Gauze Pads" not in surprising.replace("Gauze Pads + Sterile Gloves", "")


def test_command_line_generates_mines_and_reports(tmp_path, capsys):
    data, out = str(tmp_path / "p.jsonl"), str(tmp_path / "r" / "report.md")
    main(["generate", "--n", "2000", "--out", data])
    main(["mine", "--data", data, "--top", "3"])
    main(["report", "--data", data, "--out", out])
    shown = capsys.readouterr().out
    assert "frequent itemsets" in shown and "wrote" in shown
    assert (tmp_path / "r" / "report.md").read_text().startswith("# Supply bundle report")
