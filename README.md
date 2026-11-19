# Supply Co-usage Insight

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/k3ujwvwrpa/badge.svg)](https://ask.thili.ai/b/k3ujwvwrpa)

Which medical supplies are used together across procedures? This tool simulates procedure logs, mines the frequent supply sets with an exact bitset Apriori (the technique from the askThili drill *Teach a Language Model What Sells Together*), compares them with what independence would predict, and writes a report of supply bundles for hospital administrators.

## What you are building

**Goal.** Analyse mock medical procedure data to find which supplies are frequently used together.

**Done when.** A list of frequent itemsets with their support is printed, and a report of the identified supply bundles is generated.

## Milestones

- [x] **1. Create mock medical procedure data, where each procedure lists used supply SKUs.**
- [x] **2. Implement frequent itemset mining.**
- [ ] **3. Analyze and display the most frequent co-occurring supply itemsets.**
- [ ] **4. Compare the mined itemsets against simple baseline expectations.**
- [ ] **5. Generate a report of identified supply bundles.**

## Run it

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```
