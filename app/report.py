"""Milestone 5: turn the mined itemsets into a readable markdown report of supply bundles."""
from app.analysis import bundles, describe, maximal, top_itemsets
from app.data import CATEGORY_OF, HIDDEN


def _table(rows: list[dict]) -> list[str]:
    lines = ["| Bundle | Support | Expected if independent | Lift |", "|---|---|---|---|"]
    for d in rows:
        lines.append(f"| {' + '.join(d['items'])} | {d['support']:.1%} | {d['expected']:.1%} | {d['lift']:.1f} |")
    return lines


def build_report(found: dict[frozenset, float], n_procedures: int, min_support: float, top: int = 8) -> str:
    multi = [s for s in found if len(s) >= 2]
    real = set(bundles(found))
    rows = [describe(found, s) for s in maximal(found, real)]
    by_kind = {k: sorted((d for d in rows if d["kind"] == k), key=lambda d: (-d["lift"] * d["support"], d["items"]))
               for k in ("surprising", "obvious")}
    by_kind["chance"] = [describe(found, s) for s, _ in top_itemsets(found, len(found)) if s not in real][:top]
    out = ["# Supply bundle report", "",
           f"{n_procedures:,} procedures, supply sets used in at least {min_support:.0%} of them: {len(found):,} frequent sets "
           f"({len(multi):,} with two or more items). A bundle is listed only if every item in it adds association (see `bundles` in `app/analysis.py`), and only at its largest size.", "",
           "## How to read this", "",
           "- **Support** is the share of procedures that used every supply in the bundle.",
           "- **Expected** is the support if the supplies were used independently (the product of each one's own support).",
           "- **Lift** is support divided by expected. About 1 means the items are just popular and meet by chance; "
           "well above 1 means they really are used together.", "",
           "## Surprising bundles: stock these together", "",
           "Used together far more often than chance and not explained by one procedure type. These are the findings "
           "a planner would not guess from the procedure list.", ""]
    out += _table(by_kind["surprising"][:top])
    out += ["", "## Obvious bundles: already explained by a procedure", "",
            "Everything in the bundle belongs to one procedure type's kit, or to one supply category. Confirming them "
            "shows the method works; they need no new action.", ""]
    out += _table(by_kind["obvious"][:top])
    out += ["", "## Popular but unrelated: do not bundle", "",
            "Frequent only because each supply is common (lift close to 1, no item adds association). Stocking these together would not save anything.", ""]
    out += _table(by_kind["chance"])
    out += ["", "## Storage suggestion", ""]
    for d in by_kind["surprising"][:top]:
        cats = sorted({CATEGORY_OF[i] for i in d["items"]})
        out.append(f"- Shelf {' + '.join(d['items'])} in one grab-bag (they come from {len(cats)} categories: {', '.join(cats)}).")
    return "\n".join(out) + "\n"


def planted_recovery(found: dict[frozenset, float]) -> list[tuple[tuple, float, float | None]]:
    "For each bundle planted in the simulation: (items, planted share, mined support or None if missed)."
    return [(b["items"], b["share"], found.get(frozenset(b["items"]))) for b in HIDDEN]
