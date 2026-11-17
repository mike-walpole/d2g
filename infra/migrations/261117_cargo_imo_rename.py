#!/usr/bin/env python3
"""
2026-11-17 client change request:
  1. New cargo list (client order). Items without a match in the client's database
     carry `mapsTo: "others"` -> submit_form sends them on as "Others".
     Old 7 generic types are kept but set inactive (47 historic submissions reference them).
     New/changed values are English-only on purpose (zh falls back to en in get_config).
  2. IMO question removed -> new schema version dock2gdansk-main 1.1.0 (1.0.0 kept untouched).
  3. Platform renamed Dock2Gdansk -> Port Gdańsk Connect in the live translations.

Live backup of every item touched: infra/schemas/live-backup-261117/
Dry run by default; pass --apply to write.
"""

import copy
import json
import re
import sys
from datetime import datetime, timezone

import boto3

REGION = "ap-east-1"
TABLE = "d2g-form-schemas"
OLD_BRAND = "Dock2Gdansk"
OLD_BRAND_ZH = "码头到格但斯克"  # zh brand; new name stays English in every locale
NEW_BRAND = "Port Gdańsk Connect"
NEW_SCHEMA_VERSION = "1.1.0"

# Client list, in the client's order. Second element True = no match in the client's
# database -> treated as "others".
CARGO = [
    ("Containers", False),
    ("Project cargo", False),
    ("Automotive", False),
    ("Loose logs", False),
    ("Coke", False),
    ("Aggregates", False),
    ("Oats", False),
    ("Bulk bentonite", True),
    ("Faba beans", False),
    ("Cement", False),
    ("Phosphates", False),
    ("Barley", False),
    ("Petroleum coke", True),
    ("Corn", False),
    ("Molasses", False),
    ("Urea", False),
    ("NPK fertilizers", True),
    ("Wheat", False),
    ("Iron ore", False),
    ("Rapeseed", False),
    ("CAN fertilizer", False),
    ("Bulk sulphates", True),
    ("Feldspar", False),
    ("Soda ash", True),
    ("Potash", False),
    ("Oilseed meals", False),
    ("Wire rod", False),
    ("Hard coal", True),
    ("Miscellaneous steel products", True),
    ("Scrap", False),
    ("Rye", False),
    ("Sugar", True),
    ("LPG", True),
    ("Paper", False),
    ("Container depot", True),
    ("Crude oil", True),
    ("Slabs", False),
    ("Steel", False),
    ("Phosphoric acid", True),
    ("Sulphuric acid", True),
    ("Caustic soda", True),
    ("Fertilizers", False),
    ("Ammonium nitrate", False),
    ("Bentonite", False),
    ("Steel sheets", False),
    ("Bauxite", False),
    ("Timber", False),
    ("Bananas", False),
    ("Fresh meat", False),
    ("Profiles", False),
    ("Syllables", True),  # verbatim from client; almost certainly a mistranslation (billets?)
    ("Rails", False),
    ("BESS", False),
    ("Structures and equipment", True),
    ("Bitumen", False),
    ("Sulphur", False),
    ("Base oil", True),
    ("Fresh and frozen meat", True),
    ("Fresh and frozen fish", True),
    ("Oilseed meal", False),
    ("Coal", False),
    ("Blooms", True),
    ("Others", False),  # the "+ others" catch-all
]


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def build_cargo_schema(live_schema: dict) -> dict:
    new_items = []
    for order, (name, unmatched) in enumerate(CARGO, start=1):
        item = {"id": slug(name), "name": {"en": name}, "active": True, "order": order}
        if unmatched:
            item["mapsTo"] = "others"
        new_items.append(item)

    new_ids = [i["id"] for i in new_items]
    if len(set(new_ids)) != len(new_ids):
        raise SystemExit(f"Duplicate cargo ids: {new_ids}")
    unmatched_count = sum(1 for i in new_items if i.get("mapsTo") == "others")
    if unmatched_count != 20:
        raise SystemExit(f"Expected 20 unmatched cargo types (client list), got {unmatched_count}")

    retired = []
    for old in live_schema["cargoTypes"]:
        if old["id"] in new_ids:
            continue  # already migrated (re-run)
        if old["id"] in {slug(n) for n, _ in CARGO}:
            continue
        o = copy.deepcopy(old)
        o["active"] = False
        retired.append(o)

    out = copy.deepcopy(live_schema)
    out["cargoTypes"] = new_items + retired
    out["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    return out


def rebrand(obj):
    if isinstance(obj, str):
        return obj.replace(OLD_BRAND, NEW_BRAND).replace(OLD_BRAND_ZH, NEW_BRAND)
    if isinstance(obj, list):
        return [rebrand(x) for x in obj]
    if isinstance(obj, dict):
        return {k: rebrand(v) for k, v in obj.items()}
    return obj


def main():
    apply = "--apply" in sys.argv
    t = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)

    # 1. Cargo types
    cargo_item = t.get_item(Key={"formId": "config", "version": "cargo-types"})["Item"]
    new_cargo = build_cargo_schema(cargo_item["schema"])
    active = [c for c in new_cargo["cargoTypes"] if c["active"]]
    print(f"cargo-types: {len(active)} active, "
          f"{sum(1 for c in active if c.get('mapsTo') == 'others')} map to others, "
          f"{len(new_cargo['cargoTypes']) - len(active)} retired")

    # 2. Schema 1.1.0 without IMO
    base = t.get_item(Key={"formId": "dock2gdansk-main", "version": "1.0.0"})["Item"]
    existing_new = t.get_item(Key={"formId": "dock2gdansk-main", "version": NEW_SCHEMA_VERSION}).get("Item")
    new_schema = copy.deepcopy(base["schema"])
    before = len(new_schema["fields"])
    new_schema["fields"] = [f for f in new_schema["fields"] if f["id"] != "imo_cargo"]
    if len(new_schema["fields"]) != before - 1:
        raise SystemExit("imo_cargo field not found exactly once in dock2gdansk-main 1.0.0")
    new_schema["version"] = NEW_SCHEMA_VERSION
    new_schema = rebrand(new_schema)
    schema_item = {
        "formId": "dock2gdansk-main",
        "version": NEW_SCHEMA_VERSION,
        "schema": new_schema,
        "isActive": True,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "description": f"Main shipping inquiry form for {NEW_BRAND} - IMO question removed (2026-11-17)",
    }
    print(f"schema {NEW_SCHEMA_VERSION}: {before} -> {len(new_schema['fields'])} fields"
          f"{' (already exists, will overwrite)' if existing_new else ''}")

    # 3. Translations rebrand
    tr_item = t.get_item(Key={"formId": "config", "version": "translations"})["Item"]
    new_tr = rebrand(tr_item)
    changed = json.dumps(new_tr, ensure_ascii=False, default=str) != json.dumps(tr_item, ensure_ascii=False, default=str)
    print(f"translations: {'rebranded' if changed else 'no change'}")
    for lang, vals in new_tr["schema"]["translations"].items():
        print(f"  {lang}: site_title={vals.get('site_title')!r} copyright={vals.get('footer', {}).get('copyright')!r}")

    if not apply:
        print("\nDry run. Re-run with --apply to write.")
        return

    cargo_item["schema"] = new_cargo
    t.put_item(Item=cargo_item)
    t.put_item(Item=schema_item)
    if changed:
        t.put_item(Item=new_tr)
    print("\nApplied.")


if __name__ == "__main__":
    main()
