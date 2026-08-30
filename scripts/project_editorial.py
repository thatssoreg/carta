#!/usr/bin/env python3
"""Re-project the Atlas experience layer without rebuilding pinned geography.

An editorial run changes authored copy and the release overlay, never a shape.
This driver reuses `build_atlas` so every build-time contract still applies, and
recovers the geographic half of the search index from the committed artifact
rather than re-downloading the pinned source archives.

It rewrites the three artifacts an editorial run owns — `atlas-subjects.json`,
`atlas-entry-points.json` and `atlas-editorial.json` — and refuses to write if the
subject projection would change, because a subject change means geometry is in
play and `scripts/build_atlas.py` is the correct entry point.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import build_atlas as builder

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA_DIR = ROOT / "atlas-app/public/data"

# Keys `extend_search_index` adds to each geographic record downstream.
DERIVED_SEARCH_KEYS = ("native_route", "subject_kind", "experience_level")


def recover_geographic_search() -> list[dict[str, Any]]:
    """Rebuild the pre-extension geographic search records from the artifact."""
    committed = json.loads((PUBLIC_DATA_DIR / "search-index.json").read_text())
    return [
        {key: value for key, value in record.items() if key not in DERIVED_SEARCH_KEYS}
        for record in committed
        if record.get("result_type") != "native_subject"
    ]


def main() -> None:
    experience = builder.load_experience_config()
    geographic_search = recover_geographic_search()
    producer_points = builder.build_producer_points(experience)
    atlas_subjects = builder.build_atlas_subjects(
        experience, geographic_search, producer_points
    )
    subjects = atlas_subjects["subjects"]

    committed = json.loads((PUBLIC_DATA_DIR / "atlas-subjects.json").read_text())
    if committed["subjects"] != subjects:
        raise SystemExit(
            "Subject projection changed: this is not a copy-only run. "
            "Rebuild with scripts/build_atlas.py so geography is re-derived too."
        )

    editorial = builder.build_atlas_editorial(experience, subjects)
    entry_points = builder.build_entry_points(experience, subjects)

    builder.write_json(PUBLIC_DATA_DIR / "atlas-subjects.json", atlas_subjects)
    builder.write_json(PUBLIC_DATA_DIR / "atlas-entry-points.json", entry_points)
    builder.write_json(PUBLIC_DATA_DIR / "atlas-editorial.json", editorial)

    print(
        f"release: {editorial['release']} · "
        f"subjects unchanged: {len(subjects)} · "
        f"editorial subjects: {len(editorial['subjects'])} · "
        f"claims: {len(editorial['claim_support'])} · "
        f"entry points: {len(entry_points['entry_points'])}"
    )


if __name__ == "__main__":
    main()
