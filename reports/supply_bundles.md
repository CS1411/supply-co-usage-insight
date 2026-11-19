# Supply bundle report

5,000 procedures, supply sets used in at least 3% of them: 592 frequent sets (557 with two or more items). A bundle is listed only if every item in it adds association (see `bundles` in `app/analysis.py`), and only at its largest size.

## How to read this

- **Support** is the share of procedures that used every supply in the bundle.
- **Expected** is the support if the supplies were used independently (the product of each one's own support).
- **Lift** is support divided by expected. About 1 means the items are just popular and meet by chance; well above 1 means they really are used together.

## Surprising bundles: stock these together

Used together far more often than chance and not explained by one procedure type. These are the findings a planner would not guess from the procedure list.

| Bundle | Support | Expected if independent | Lift |
|---|---|---|---|
| Fentanyl 2 ml + Head Cap + Skin Stapler + Suture Silk 0 | 4.2% | 0.0% | 762.9 |
| Ondansetron 4 mg + Pulse Oximeter Probe + Warming Blanket | 7.4% | 0.1% | 122.2 |
| IV Giving Set + Ringer Lactate 500 ml + Surgical Gown | 5.2% | 0.2% | 28.5 |

## Obvious bundles: already explained by a procedure

Everything in the bundle belongs to one procedure type's kit, or to one supply category. Confirming them shows the method works; they need no new action.

| Bundle | Support | Expected if independent | Lift |
|---|---|---|---|
| Intubation Tube + Propofol 20 ml + Suture Vicryl 2-0 + Trocar 10 mm | 7.5% | 0.0% | 472.1 |
| Drain Bag + Intubation Tube + Suture Vicryl 2-0 + Trocar 10 mm | 3.7% | 0.0% | 928.7 |
| Intubation Tube + Scalpel Blade 11 + Suture Vicryl 2-0 + Trocar 10 mm | 6.9% | 0.0% | 441.1 |
| Pressure Dressing + Scalpel Blade 11 + Surgical Needle Holder + Suture Nylon 3-0 | 6.3% | 0.0% | 315.1 |
| Drain Bag + Intubation Tube + Propofol 20 ml + Trocar 10 mm | 4.0% | 0.0% | 493.8 |
| Drain Bag + Propofol 20 ml + Suture Vicryl 2-0 + Trocar 10 mm | 3.9% | 0.0% | 484.6 |
| Drain Bag + Intubation Tube + Propofol 20 ml + Suture Vicryl 2-0 | 3.7% | 0.0% | 479.6 |
| Pressure Dressing + Propofol 20 ml + Surgical Needle Holder + Suture Nylon 3-0 | 5.9% | 0.0% | 290.8 |

## Popular but unrelated: do not bundle

Frequent only because each supply is common (lift close to 1, no item adds association). Stocking these together would not save anything.

| Bundle | Support | Expected if independent | Lift |
|---|---|---|---|
| Gauze Pads + Sterile Gloves | 41.1% | 41.2% | 1.0 |
| Antiseptic Wipes + Sterile Gloves | 38.2% | 37.8% | 1.0 |
| Sterile Gloves + Surgical Mask | 28.8% | 28.2% | 1.0 |
| Antiseptic Wipes + Gauze Pads | 26.7% | 21.6% | 1.2 |
| Adhesive Dressing + Sterile Gloves | 25.5% | 25.2% | 1.0 |
| Antiseptic Wipes + Gauze Pads + Sterile Gloves | 23.0% | 18.3% | 1.3 |
| Adhesive Dressing + Antiseptic Wipes + Sterile Gloves | 22.0% | 11.2% | 2.0 |
| Saline 500 ml + Sterile Gloves | 22.0% | 22.1% | 1.0 |

## Storage suggestion

- Shelf Fentanyl 2 ml + Head Cap + Skin Stapler + Suture Silk 0 in one grab-bag (they come from 4 categories: Anaesthesia, PPE, Sutures, Wound care).
- Shelf Ondansetron 4 mg + Pulse Oximeter Probe + Warming Blanket in one grab-bag (they come from 2 categories: Anaesthesia, Recovery).
- Shelf IV Giving Set + Ringer Lactate 500 ml + Surgical Gown in one grab-bag (they come from 2 categories: IV and fluids, PPE).
