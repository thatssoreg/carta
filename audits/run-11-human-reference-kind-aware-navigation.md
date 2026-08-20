# CARTA Run 11 — Human Reference kind-aware navigation

## Outcome

Run 11 makes Human Reference navigation graph-backed **with deterministic reader semantics** while leaving the STRATA v0.2 machine graph authoritative.

Production now uses one explainable resolver for generation, testing, and audit analysis. It separates structural country membership from editorial anchors, preserves direct and explicit routes, and gates graph-only two-hop candidates by source profile kind and path shape. No machine entity, relationship, claim, source, schema kind, or profile disposition changed.

## Implemented semantics

- `country_entity_ids` is structural: it links a subject upward to its country and lets a country orient downward to governed region/appellation surfaces. It no longer turns every assigned producer into a reciprocal country recommendation.
- `representative_anchor_ids` remains editorial: outbound and reciprocal discovery both survive.
- Shared components, direct governed relationships, structural country routes, and editorial anchors bypass the two-hop gate.
- Country two-hop paths admit geographic, ecosystem, grape, and classification orientation, but not unselected producer/person/wine adjacency.
- Region, appellation, and landscape paths reject peer geography when every route is an up-then-down traversal through a broad container.
- Grape paths reject unanchored grape/classification adjacency created through a two-hop wine or classification bridge.
- Producer/person paths to producer/person targets require a professional, site/parcel, farming, planting, or explicit-practice predicate on at least one path.
- Other current schema kinds retain governed two-hop context until surfaced fixtures demonstrate a narrower reader job. Every schema kind must have an explicit policy-map entry.
- Surviving candidates retain the existing simple route/distance/title/ID ordering and 16-link cap. No numeric predicate weights, degree penalties, popularity scores, embeddings, or profile-ID exceptions entered production.

## Before / after navigation measurements

Authority is unchanged at 505 entities, 524 relationships, 396 claims, 292 sources, 33 names, 34 spatial assertions, and 183 profiles; 160 profiles have reader-facing surfaces and 486 relationship records are navigation-eligible.

| Metric | Run 10 | Run 11 |
|---|---:|---:|
| Directed candidate-profile pairs | 1,024 | 700 |
| Displayed links | 985 | 696 |
| Mean candidates | 6.40 | 4.38 |
| Median candidates | 5 | 4 |
| p95 candidates | 14 | 10 |
| Maximum candidates | 46 (France) | 20 (France) |
| Profiles at or above the 16-link cap | 5 (3.12%) | 1 (0.62%) |
| Profiles over the cap / actual displacement | 5 (3.12%) | 1 (0.62%) |

France is the only remaining capped surface, with 20 eligible candidates and four displaced by the cap. Its displayed list contains governed internal geography plus its explicit Richard Leroy anchor; structural country membership no longer supplies producer candidates.

Historical replay under the Run 11 policy retained every previously displayed common-profile link across Run 07 → Run 08 (559/559) and Run 08 → Run 09 (628/628), while allowing ordinary additive graph growth.

### Displayed route and distance distribution

The shortest-distance table is directly comparable to Run 10 and distinguishes anchor-only candidates from graph-reachable candidates.

| Shortest governed route | Run 10 | Run 11 |
|---|---:|---:|
| Anchor-only / no graph path | 251 (25.48%) | 229 (32.90%) |
| Shared component / distance 0 | 8 (0.81%) | 8 (1.15%) |
| Direct / distance 1 | 270 (27.41%) | 270 (38.79%) |
| Two-hop / distance 2 | 456 (46.29%) | 189 (27.16%) |

Among displayed graph-reachable distance-one/two links, the two-hop share fell from 62.81% (456/726) to 41.18% (189/459). Direct shortest paths were preserved exactly at 270.

The Run 11 winning projection routes are:

| Winning route | Links | Percent |
|---|---:|---:|
| Editorial anchor outbound | 261 | 37.50% |
| Editorial anchor reciprocal | 149 | 21.41% |
| Structural country outbound | 116 | 16.67% |
| Structural country descendant | 35 | 5.03% |
| Shared component | 6 | 0.86% |
| Direct relationship | 34 | 4.89% |
| Graph-only eligible two-hop | 95 | 13.65% |

## Run 10 ratings-fixture regression

The unchanged 28-page fixture still describes all 257 links displayed at the Run 10 baseline. The audit reconstructs that baseline and measures which rated links survive current production.

| Rating | Run 10 links | Retained in Run 11 | Removed |
|---|---:|---:|---:|
| A — essential | 103 | 102 | 1 |
| B — strong | 6 | 6 | 0 |
| C — useful expansion | 76 | 57 | 19 |
| D — low-salience | 28 | 2 | 26 |
| E — distracting/misleading | 44 | 0 | 44 |

- A/B retention: 108/109 (99.08%).
- Professional B retention: 6/6 (100%).
- D/E removal: 70/72 (97.22%).
- All 44 E links were eliminated.
- The sole A regression is Napa Valley AVA → St. Helena AVA; it is the expected authority-gap result described below.

The 19 removed C links are explainable consequences of the generic policy rather than ID exceptions: ten structurally reciprocal country-to-producer links on Germany/Portugal; four weak producer-to-producer regional/grape expansions (Burgess and Houillon); two Côtes du Rhône sibling-appellation paths via France; two Chardonnay/Savagnin co-occurrence directions; and Domaine Labet → Domaine de Saint Pierre through broad components alone.

### D/E rate by sampled source kind

The Run 11 rate is the D/E share among retained, previously rated links for that kind. Newly displayed links were not retroactively added to the immutable Run 10 fixture.

| Source kind | Run 10 D/E rate | Run 11 retained-link D/E rate |
|---|---:|---:|
| Country | 15.79% | 0% |
| Region | 41.07% | 0% |
| Appellation | 38.46% | 7.14% |
| Grape | 6.98% | 0% |
| Producer | 36.00% | 2.27% |

The two retained D links are Côtes du Rhône → Vin de France (a cross-classification wine path) and Günther Steinmetz → Hiyu (a Riesling/planting path). They are real remaining salience questions; this run does not add narrower appellation-classification or cross-producer planting rules without another reviewed fixture.

## Required cases

- France and the United States retain internal region/appellation orientation without structural-country producer flooding. France retains Richard Leroy because France explicitly anchors that producer.
- Loire, Jura, Savoie, and Côtes du Rhône no longer display peer French surfaces solely through France.
- Napa Valley no longer displays Contra Costa, Santa Barbara County, or Santa Ynez Valley solely through California.
- California retains downward descendant navigation to Ballard Canyon through Santa Ynez Valley.
- Syrah → Cabernet Sauvignon and grape → Vin de France two-hop co-occurrence links are removed.
- Lampyres → Matassa remains direct through `WORKED_FOR`; Houillon retains Overnoy and Bruyère-Houillon through explicit/direct professional context; Imanol Garay retains Alfredo Egia and Richard Leroy.
- Broad composite-producer adjacency through grape/classification components is removed; the path-specific Labet → Hiyu case survives.

## St. Helena / Napa disposition

The authority gap remains deliberately unresolved. Existing governed evidence establishes St. Helena AVA and locates it in California, but it does not assert St. Helena AVA `WITHIN` Napa Valley AVA under CARTA's evidence rules. The new resolver therefore rejects Napa → California → St. Helena as the same up-then-down sibling shape it rejects elsewhere.

No projection exception or remembered geographic fact was added. A future focused authority pass may add containment only when a fit existing or newly governed source directly supports it.

## Generated Human Reference

The canonical generator refreshed 89 Atlas pages. A second `--write-human-reference` run produced no updates, demonstrating deterministic regeneration. Generated pages were not patched by hand.

## Validation

All checks passed:

```text
.venv/bin/python -m py_compile scripts/validate_data.py scripts/audit_navigation.py tests/test_navigation.py
.venv/bin/python scripts/validate_data.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/audit_navigation.py \
  --ratings audits/run-10-human-reference-navigation-ratings.json \
  --format markdown
.venv/bin/python scripts/audit_navigation.py \
  --git-ref 27f3ab7 --compare-ref ee49ef6 --format json
.venv/bin/python scripts/audit_navigation.py \
  --git-ref f74088f --compare-ref 27f3ab7 --format json
.venv/bin/python scripts/validate_data.py --write-human-reference
```

The canonical validator covers schemas, record references, authored authority contracts, relationship/claim/source rules, profile governance, generated Human Reference freshness, Atlas governance, local links, and Atlas reachability. CI now also runs the 11 focused navigation tests.

## Architectural disposition

- Machine authority remains the only knowledge authority.
- Human Reference remains a generated reader projection.
- STRATA remains v0.2.
- No profile-specific eligibility exceptions were introduced.
- Projects and vineyards remain components of composite producer-world profiles.
- Persistent wine identity remains non-vintage-specific.
