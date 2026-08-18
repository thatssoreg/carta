#!/usr/bin/env python3
"""Validate CARTA JSONL authority, Human Reference profiles, and cross-references."""
from __future__ import annotations
import json
from pathlib import Path

try:
    import jsonschema
except ImportError:
    raise SystemExit("Install dev dependency: python -m pip install jsonschema")

ROOT = Path(__file__).resolve().parents[1]

SETS = {
    "entities": ("data/entities", "schemas/entity.schema.json"),
    "relationships": ("data/relationships", "schemas/relationship.schema.json"),
    "claims": ("data/claims", "schemas/claim.schema.json"),
    "sources": ("data/sources", "schemas/source.schema.json"),
    "names": ("data/names", "schemas/name-assertion.schema.json"),
    "spatial": ("data/geography/assertions", "schemas/spatial-assertion.schema.json"),
    "profiles": ("data/reference-profiles", "schemas/reference-profile.schema.json"),
}

def load_jsonl(directory: Path):
    records = []
    if not directory.exists():
        return records
    for path in sorted(directory.glob("*.jsonl")):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}")
    return records

data = {}
for label, (directory, schema_path) in SETS.items():
    records = load_jsonl(ROOT / directory)
    schema = json.loads((ROOT / schema_path).read_text())
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    for record in records:
        errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
        if errors:
            raise SystemExit(f"{label} {record.get('id')}: {errors[0].message}")
    data[label] = records

ids = {}
for label, records in data.items():
    bucket = set()
    for record in records:
        rid = record["id"]
        if rid in bucket:
            raise SystemExit(f"duplicate {label} id: {rid}")
        bucket.add(rid)
    ids[label] = bucket

for r in data["relationships"]:
    if r["subject_id"] not in ids["entities"] or r["object_id"] not in ids["entities"]:
        raise SystemExit(f"{r['id']}: missing relationship endpoint")
    for cid in r.get("claim_ids", []):
        if cid not in ids["claims"]:
            raise SystemExit(f"{r['id']}: missing claim {cid}")

all_subject_ids = ids["entities"] | ids["relationships"] | ids["claims"] | ids["names"] | ids["spatial"]
for c in data["claims"]:
    if c["subject_ref"] not in all_subject_ids:
        raise SystemExit(f"{c['id']}: missing subject {c['subject_ref']}")
    for sr in c["source_refs"]:
        if sr["source_id"] not in ids["sources"]:
            raise SystemExit(f"{c['id']}: missing source {sr['source_id']}")

for n in data["names"]:
    if n["entity_id"] not in ids["entities"]:
        raise SystemExit(f"{n['id']}: missing entity")
    if n.get("jurisdiction_ref") and n["jurisdiction_ref"] not in ids["entities"]:
        raise SystemExit(f"{n['id']}: missing jurisdiction")
    for cid in n["claim_ids"]:
        if cid not in ids["claims"]:
            raise SystemExit(f"{n['id']}: missing claim {cid}")

for s in data["spatial"]:
    if s["entity_id"] not in ids["entities"]:
        raise SystemExit(f"{s['id']}: missing entity")
    for eid in s.get("anchor_entity_refs", []):
        if eid not in ids["entities"]:
            raise SystemExit(f"{s['id']}: missing anchor {eid}")
    for sid in s["source_ids"]:
        if sid not in ids["sources"]:
            raise SystemExit(f"{s['id']}: missing source {sid}")
    for cid in s.get("claim_ids", []):
        if cid not in ids["claims"]:
            raise SystemExit(f"{s['id']}: missing claim {cid}")

for p in data["profiles"]:
    for eid in p["component_entity_ids"]:
        if eid not in ids["entities"]:
            raise SystemExit(f"{p['id']}: missing component entity {eid}")
    primary = p.get("primary_entity_id")
    if primary and primary not in ids["entities"]:
        raise SystemExit(f"{p['id']}: missing primary entity {primary}")
    for eid in p.get("country_entity_ids", []):
        if eid not in ids["entities"]:
            raise SystemExit(f"{p['id']}: missing country entity {eid}")
    for eid in p.get("representative_anchor_ids", []):
        if eid not in ids["entities"]:
            raise SystemExit(f"{p['id']}: missing representative anchor {eid}")
    if p["publication_status"] == "published" and p["maturity"] == "node":
        raise SystemExit(f"{p['id']}: node maturity cannot be published as a finished reference")
    if p["publication_status"] in {"published", "stub"} and not (ROOT / p["path"]).exists():
        raise SystemExit(f"{p['id']}: reference path does not exist: {p['path']}")

print("PASS", ", ".join(f"{k}={len(v)}" for k, v in data.items()))
