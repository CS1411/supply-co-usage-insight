"""Milestone 1: mock procedure logs. Each procedure lists the supply SKUs it used.

The data is simulated with known structure, so the mining can be checked against an answer:
- every procedure type has a core supply list; each core supply is used with some probability;
- a few common supplies (gloves, gauze, saline...) are added to any procedure by chance;
- three HIDDEN bundles are planted across procedure types, independent of what the procedure is.
"""
import json
import random
from pathlib import Path

CATEGORIES = {
    "PPE": ["Sterile Gloves", "Surgical Mask", "Surgical Gown", "Drape Sheet", "Head Cap"],
    "Wound care": ["Gauze Pads", "Adhesive Dressing", "Elastic Bandage", "Antiseptic Wipes", "Skin Stapler"],
    "Sutures": ["Suture Vicryl 2-0", "Suture Nylon 3-0", "Suture Silk 0", "Surgical Needle Holder"],
    "IV and fluids": ["IV Cannula 20G", "IV Giving Set", "Saline 500 ml", "Ringer Lactate 500 ml", "Syringe 10 ml"],
    "Anaesthesia": ["Lidocaine 2%", "Propofol 20 ml", "Intubation Tube", "Ondansetron 4 mg", "Fentanyl 2 ml"],
    "Procedure kits": ["Scalpel Blade 11", "Trocar 10 mm", "Biopsy Forceps", "Guidewire", "Arthroscope Sleeve", "Cast Padding"],
    "Recovery": ["Warming Blanket", "Pulse Oximeter Probe", "Urine Catheter", "Drain Bag", "Pressure Dressing"],
}
SKUS = [s for items in CATEGORIES.values() for s in items]
CATEGORY_OF = {s: c for c, items in CATEGORIES.items() for s in items}

# procedure type -> (share of all procedures, {supply: probability it is used})
PROCEDURES = {
    "Appendectomy": (0.10, {"Trocar 10 mm": 0.95, "Scalpel Blade 11": 0.9, "Suture Vicryl 2-0": 0.9, "Drain Bag": 0.5, "Propofol 20 ml": 0.95, "Intubation Tube": 0.9}),
    "Hernia repair": (0.10, {"Scalpel Blade 11": 0.95, "Suture Nylon 3-0": 0.9, "Surgical Needle Holder": 0.9, "Propofol 20 ml": 0.9, "Pressure Dressing": 0.8}),
    "Knee arthroscopy": (0.08, {"Arthroscope Sleeve": 0.98, "Skin Stapler": 0.6, "Saline 500 ml": 0.95, "Elastic Bandage": 0.9, "Fentanyl 2 ml": 0.8}),
    "Cast application": (0.12, {"Cast Padding": 0.98, "Elastic Bandage": 0.7, "Lidocaine 2%": 0.4}),
    "Cardiac catheterization": (0.06, {"Guidewire": 0.98, "Lidocaine 2%": 0.95, "Pressure Dressing": 0.9, "Syringe 10 ml": 0.9, "Pulse Oximeter Probe": 0.8}),
    "Wound dressing change": (0.20, {"Gauze Pads": 0.97, "Adhesive Dressing": 0.9, "Antiseptic Wipes": 0.9}),
    "IV insertion": (0.18, {"IV Cannula 20G": 0.98, "IV Giving Set": 0.7, "Antiseptic Wipes": 0.8, "Adhesive Dressing": 0.6}),
    "Biopsy": (0.08, {"Biopsy Forceps": 0.95, "Lidocaine 2%": 0.9, "Syringe 10 ml": 0.8, "Gauze Pads": 0.7}),
    "Catheter placement": (0.08, {"Urine Catheter": 0.97, "Antiseptic Wipes": 0.8, "Drape Sheet": 0.7}),
}
BACKGROUND = {"Sterile Gloves": 0.85, "Gauze Pads": 0.30, "Saline 500 ml": 0.20, "Surgical Mask": 0.35, "Syringe 10 ml": 0.15,
              "Antiseptic Wipes": 0.10, "Head Cap": 0.12, "Surgical Gown": 0.15, "Drape Sheet": 0.10}
# hidden bundles: used together in `share` of ALL procedures, whatever the procedure is
HIDDEN = [
    {"items": ("Ondansetron 4 mg", "Warming Blanket", "Pulse Oximeter Probe"), "share": 0.07},
    {"items": ("Ringer Lactate 500 ml", "IV Giving Set", "Surgical Gown"), "share": 0.05},
    {"items": ("Head Cap", "Suture Silk 0", "Skin Stapler", "Fentanyl 2 ml"), "share": 0.04},
]


def generate_procedures(n: int = 5000, seed: int = 0) -> list[dict]:
    """n procedures: [{"id", "type", "supplies": [sku, ...]}]. Same seed, same data."""
    rng = random.Random(seed)
    types, weights = list(PROCEDURES), [PROCEDURES[t][0] for t in PROCEDURES]
    rows = []
    for i in range(n):
        kind = rng.choices(types, weights)[0]
        used = {s for s, p in PROCEDURES[kind][1].items() if rng.random() < p}
        used |= {s for s, p in BACKGROUND.items() if rng.random() < p}
        for bundle in HIDDEN:
            if rng.random() < bundle["share"]:
                used |= set(bundle["items"])
        rows.append({"id": i, "type": kind, "supplies": sorted(used)})
    return rows


def save_procedures(rows: list[dict], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def load_procedures(path: str) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
