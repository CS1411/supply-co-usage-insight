# Supply Co-usage Insight

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/k3ujwvwrpa/badge.svg)](https://ask.thili.ai/b/k3ujwvwrpa)

Which medical supplies are used together across procedures? This tool simulates procedure logs, mines the frequent supply sets with an exact bitset Apriori (the technique from the askThili drill *Teach a Language Model What Sells Together*), compares them with what independence would predict, and writes a report of supply bundles for hospital administrators.

## What you are building

**Goal.** Analyse mock medical procedure data to find which supplies are frequently used together.

**Done when.** A list of frequent itemsets with their support is printed, and a report of the identified supply bundles is generated.

## Milestones

- [x] **1. Create mock medical procedure data, where each procedure lists used supply SKUs.** `app/data.py`
- [x] **2. Implement frequent itemset mining.** `app/mine.py`, checked against brute force in `tests/test_mine.py`
- [x] **3. Analyze and display the most frequent co-occurring supply itemsets.** `python -m app.cli mine`
- [x] **4. Compare the mined itemsets against simple baseline expectations.** independence baseline, lift, obvious / surprising / chance in `app/analysis.py`
- [x] **5. Generate a report of identified supply bundles.** `python -m app.cli report` writes [reports/supply_bundles.md](reports/supply_bundles.md)

## Run it

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.cli generate            # 5,000 simulated procedures -> data/procedures.jsonl
python -m app.cli mine --top 15       # frequent sets with support, expected support and lift
python -m app.cli report              # reports/supply_bundles.md
pytest
```

## What it finds

The simulation has 9 procedure types, each with a core supply list, plus common supplies (gloves, gauze, saline...) and
three hidden bundles planted across procedure types. On 5,000 procedures at 3% minimum support:

| Planted bundle | Planted share | Mined support |
|---|---|---|
| Ondansetron + Warming Blanket + Pulse Oximeter Probe | 7% | 7.4% |
| Ringer Lactate + IV Giving Set + Surgical Gown | 5% | 5.2% |
| Head Cap + Suture Silk 0 + Skin Stapler + Fentanyl | 4% | 4.2% |

The mined supports are a little above the planted shares because the supplies are also used by chance elsewhere.

The point of the baseline: sorted by support alone, the top sets are all gloves-plus-something (Gauze + Gloves 41%,
Wipes + Gloves 38%) with lift about 1.0, which means they are common, not related. Ranking by lift and requiring that every
item adds association (`bundles`) is what surfaces the hidden bundles above the procedure kits ("obvious") and the
popular-but-unrelated pairs ("chance").

## Limits

- The data is simulated, so "surprising" means "not explained by one procedure type's kit", which is only as good as the kit lists in `app/data.py`.
- The `gain=1.5` and `high_lift=3.0` thresholds were chosen by hand for this simulation.
- Mining is exact but limited to sets of at most 4 supplies.

## Honest development notes

- Built with AI assistance (Claude) in a single working session; the commit timeline does not reflect days of work.
- Milestones 3, 4 and 5 were developed together and committed in one commit; the README checklist was ticked as each part worked.
- The first version of the report listed "bundle + Sterile Gloves" supersets as bundles; I replaced it with the `bundles` gain test and added tests for it.
