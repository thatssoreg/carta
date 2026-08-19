# Run 07 — Human Reference Navigability Closure

## Starting state

The run inspected the connected live GitHub repository before editing.

- Repository: `thatssoreg/carta`
- Default branch: `main`
- Starting `main`: `c809b73885d79736987ce9763df3940b6942abf8` — `Merge Run 06 parallel research reconciliation`
- Local checkout after `git fetch origin --prune`: clean `main`, with local `HEAD` and `origin/main` both at the live SHA
- PR #13: open draft, base `main`, head `run-06d-reference-closure-proof`, head `9c09f50e703df8ded8a02e8df0b9355953af18b3`, eight changed files, no comments or reviews
- PR #13 CI: failed because `atlas/indexes/wines.md` was stale after the new Run 06D wine entities; the Actions log stopped at `generated index is stale: atlas/indexes/wines.md`
- Issue #14: open with the full Human Reference closure criteria
- `main` had not advanced from the handoff SHA

The starting repository validated cleanly after installing its pinned development dependency and running the documented validator with Python 3:

`PASS entities=340, relationships=311, claims=262, sources=182, names=17, spatial=34, profiles=42`

Starting Human Reference coverage was structurally incomplete:

- 38 active producers; 27 occurred in a governed profile and 11 did not
- 26 producer-world profiles
- eight active countries; two had profiles
- 39 active grapes; five had profiles
- 42 total profiles
- no disposition existed for an intentionally machine-only subject
- indexes were profile-driven, so uncovered producers, countries, and grapes could disappear without a validator error
- provenance and indexes were generated, but reader navigation and reciprocal discovery were not

## Root cause

The graph/profile distinction was correct, but the projection lifecycle only described objects that already had pages. `reference_profile.path` was mandatory, so the repository could not record “important machine authority, intentionally no page.” The validator therefore had no complete population against which to test producer, country, or grape projection coverage.

`representative_anchor_ids` and `country_entity_ids` already provided useful editorial projection authority, while typed relationships already held the graph truth. The missing implementation was a deterministic resolver joining those two forms of authority to canonical Human Reference paths and deriving reciprocal discovery.

## Architecture decision

Run 07 keeps STRATA v0.2 and extends only Human Reference projection governance.

### Disposition model

The existing `publication_status` lifecycle is reused:

- `published` — baseline or deep canonical Human Reference
- `stub` — honest node-level reader surface with a canonical path
- `queued` — governed surface awaiting work
- `machine_only` — explicit node-level deferral with no path
- `deprecated` — historical profile governance

The validator now requires every active Reference producer, country, and grape to occur in at least one profile disposition. `machine_only` requires `node` maturity and is forbidden from claiming an Atlas path.

### Navigation target model

No Markdown-side relationship graph was added. The generator resolves related profiles from:

1. governed `country_entity_ids` and `representative_anchor_ids`;
2. supported or provisional Reference relationships using a reader-useful predicate allowlist;
3. canonical `reference_profile` paths and publication dispositions.

Generated links never target a machine-only record. Deliberately deferred editorial anchors are rendered as plain text. Markdown link and reachability validation remains the final stale/broken-target guard.

### Reciprocal discovery model

The generator treats the graph as undirected for discovery only, follows at most two typed edges, prioritizes outbound and reciprocal editorial anchors, deduplicates profiles, and caps the generated list at 16. This surfaces useful reverse paths without dumping every relationship or creating unsupported inverse authority.

### Project and vineyard decision

No `project` or `vineyard` profile kinds were added. Tzum, Vins Pepe Raventós, Soleras del Pacífico, Eruptio, Moon Hill Farm, Evangelho Vineyard, Kronos Vineyard, Sunbasket Vineyard, Westhofener Kirchspiel, Terrasses del Serral, and the JONATA Estate Vineyard remain understandable as components of composite producer-world profiles. No real case demonstrated information loss that required another standalone kind.

## Implementation

### Schema and validator/generator

- made `path` conditional in `reference-profile.schema.json`
- added `machine_only` to the existing publication lifecycle
- added profile-kind/primary-entity semantic validation so countries, regions, appellations, classifications, grapes, producers, and projects cannot be silently confused
- added mandatory active-producer, active-country, and active-grape disposition coverage
- added deterministic `Explore CARTA` generation and reciprocal discovery
- added honest stub-shell generation under `--write-human-reference`
- updated all indexes to separate Human Reference surfaces from explicit machine-only dispositions
- updated the wine index to distinguish composite surfaces, machine-only deferral, and genuinely ungoverned wine nodes
- kept Atlas path governance, broken-link checks, and reachability checks active for every surfaced profile

### Run 06 backfill

Honest composite node/stub surfaces were added for:

- Domaine Labet
- Vins Pepe Raventós
- Soleras del Pacífico
- Eruptio
- Weingut Keller
- Corison Winery

The repair also added the country, grape, region, appellation, and classification surfaces needed to traverse these worlds without promoting thin content to baseline.

### Existing-world backfill

Every pre-existing producer profile received regenerated graph-backed navigation. All eight represented countries now have surfaces. Existing representative grape, regional, and appellation anchors were promoted to honest stubs where a reader-facing node was useful; remaining active grapes received explicit machine-only dispositions.

### Run 06D integration

The complete inspected PR #13 authority branch was merged into the Run 07 branch only after the closure invariant validated. Run 07 then added composite stubs and navigation for:

- Companhia de Vinhos dos Profetas e dos Villões / Porto Santo / Madeirense DOP / Palomino-Listrão
- Clos du Tue-Boeuf / Loire Valley / Menu Pineau-Orbois / Vin de France
- JONATA / Ballard Canyon / Todos

The integration preserves the PR's corrections:

- Madeirense DOP is not fortified DOP Madeira
- Listrão is a supported local name on Palomino Fino; Caracol remains unresolved
- 1937/1950 Brin de Chèvre plantings are not described as pre-phylloxera
- Vin de France is a classification, not an appellation or geographic container
- JONATA chronology follows the stronger first-party record
- Ballard Canyon AVA dates to 2013; Santa Barbara County is not an AVA
- Todos remains one persistent wine with vintage-scoped composition

## Coverage result

After Run 06D integration and projection backfill:

- 369 entities, 356 active Reference entities
- 41 active producers: 33 have reader surfaces, eight are explicitly machine-only, zero are undisposed
- 43 active grapes: 30 have reader surfaces, 13 are explicitly machine-only, zero are undisposed
- eight active countries: all eight have surfaces
- 151 governed profiles: 130 surfaced and 21 machine-only
- publication mix: 40 published, 89 honest stubs, one queued, 21 machine-only
- maturity mix: 40 baseline, 111 node, zero thin pages mislabeled baseline
- surfaced supporting geography/law: 24 regions, 28 appellations, and two classifications

Explicitly machine-only producers are Antica Terra, Bedrock Wine Co., Camin Larredya, Château Bouscassé, Clos Uroulat, Domaine Arretxea, Domaine Cauhapé, and Domaine de Souch.

Explicitly machine-only grapes are Bourboulenc, Caracol, Carmenère, Garnacha Tinta, Grenache Blanc, Merlot, Muscat Blanc, Petit Meslier, Petite Sirah, Pinot Gris, Pinot Noir, Sauvignon, and Ugni Blanc.

## Acceptance tests

### Keller

Ordinary producer discovery now reaches `Weingut Keller` from the generated producer index. The Keller surface resolves:

`Weingut Keller → Germany → Rheinhessen → Riesling → Kabinett`

The profile keeps Keller Riesling limestone, Keller Riesling Kabinett limestone, Keller Riesling RR, Westhofener Kirchspiel, and Klaus-Peter Keller inside the honest composite surface. Germany, Rheinhessen, and Riesling each generate a reciprocal link to Keller. Riesling also surfaces Hofgut Falkenstein and Weingut Rudi Pichler from represented authority.

### Cross-world tests

1. `Domaine Labet → Jura → Chardonnay / Savagnin`; Jura reciprocally surfaces Labet, while the page keeps ouillage and sous-voile distinct and rejects unsupported fortification.
2. `Eruptio → Azores → Pico DOP → Arinto dos Açores`; the grape remains separate from mainland Arinto and the legal designation remains distinct from physical island geography.
3. `Corison Winery → Napa Valley AVA → Cabernet Sauvignon`; the profile preserves the multi-vineyard flagship and separate Kronos/Sunbasket wine identities.
4. `Profetas e Villões → Porto Santo → Madeirense DOP → Palomino Fino`; Listrão local naming is governed, Madeirense/Madeira are not conflated, and Caracol is plainly deferred.
5. `Clos du Tue-Boeuf → Loire Valley → Menu Pineau / Orbois → Vin de France`; local naming, physical geography, and national classification stay semantically separate.
6. `JONATA → Ballard Canyon AVA → Todos`; Santa Barbara County is not rendered as an AVA, and the changing 2022 blend remains temporal composition on one persistent wine identity.

## Rejected alternatives

- **Give every entity a page:** rejected because ontology cardinality is not editorial publication judgment.
- **Promote thin nodes to baseline:** rejected because it would falsify Human Reference depth.
- **Keep uncovered nodes invisible until research is complete:** rejected because repeated high-value subjects need discoverable honest stubs or explicit deferral.
- **Maintain reciprocal lists by hand in Markdown:** rejected as a second unsynchronized knowledge graph.
- **Add project and vineyard profile kinds now:** rejected because composite profiles represent the tested cases without information loss.
- **Create STRATA v0.3:** rejected because all accepted facts fit existing v0.2 entities, relationships, claims, names, classifications, time, and geography.

## Validation

Executed after full generation and Run 06D integration:

```text
.venv/bin/python scripts/validate_data.py --write-human-reference
.venv/bin/python scripts/validate_data.py

PASS entities=369, relationships=359, claims=289, sources=200, names=20, spatial=34, profiles=151
```

Also executed:

```text
.venv/bin/python -m py_compile scripts/validate_data.py
git diff --check
```

The PR #13 stale-wine-index failure is resolved by committed generated output.

## Remaining gaps

- The 89 node/stub surfaces are intentionally not baseline references; subject-specific enrichment remains queued according to their recorded research gaps.
- Machine-only producers and grapes require an explicit future promotion decision if reader demand or graph centrality increases.
- Generic stubs orient through machine authority and navigation; they should gain reader-first prose only through evidence-backed enrichment rather than automatic filler.
- Issue #14 should remain open until the Run 07 pull request is reviewed and merged; repository closure is implemented on the branch but not yet on `main`.
- No authoritative parcel or appellation geometry was fabricated.

## STRATA result

`NO CONCRETE STRATA v0.2 REPRESENTATION FAILURE FOUND.`

Run 07 is a Human Reference projection, generation, and validation repair. STRATA remains v0.2.
