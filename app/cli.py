"""Command line: python -m app.cli generate | mine | report"""
import argparse
from pathlib import Path

from app.analysis import describe, top_itemsets
from app.data import generate_procedures, load_procedures, save_procedures
from app.mine import frequent_itemsets
from app.report import build_report, planted_recovery

DATA = "data/procedures.jsonl"


def _mined(path: str, min_support: float):
    rows = load_procedures(path)
    return rows, frequent_itemsets([r["supplies"] for r in rows], min_support)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="supply-co-usage-insight", description="Which supplies are used together?")
    sub = parser.add_subparsers(dest="command", required=True)
    g = sub.add_parser("generate", help="simulate procedure logs")
    g.add_argument("--n", type=int, default=5000)
    g.add_argument("--seed", type=int, default=0)
    g.add_argument("--out", default=DATA)
    m = sub.add_parser("mine", help="print the most frequent supply sets with support, expectation and lift")
    m.add_argument("--data", default=DATA)
    m.add_argument("--min-support", type=float, default=0.03)
    m.add_argument("--top", type=int, default=15)
    r = sub.add_parser("report", help="write the markdown report of supply bundles")
    r.add_argument("--data", default=DATA)
    r.add_argument("--min-support", type=float, default=0.03)
    r.add_argument("--out", default="reports/supply_bundles.md")
    args = parser.parse_args(argv)
    if args.command == "report":
        rows, found = _mined(args.data, args.min_support)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(build_report(found, len(rows), args.min_support))
        print(f"wrote {args.out}")
        for items, share, got in planted_recovery(found):
            print(f"planted {share:.0%} bundle {' + '.join(items)}: mined {'MISSED' if got is None else f'{got:.1%}'}")
    elif args.command == "generate":
        save_procedures(generate_procedures(args.n, args.seed), args.out)
        print(f"wrote {args.n} procedures to {args.out}")
    elif args.command == "mine":
        rows, found = _mined(args.data, args.min_support)
        print(f"{len(rows)} procedures, {len(found)} frequent itemsets at min support {args.min_support:.1%}")
        print(f"{'support':>8} {'expected':>9} {'lift':>6}  kind        items")
        for items, _ in top_itemsets(found, args.top):
            d = describe(found, items)
            print(f"{d['support']:8.1%} {d['expected']:9.1%} {d['lift']:6.1f}  {d['kind']:10s}  {' + '.join(d['items'])}")


if __name__ == "__main__":
    main()
