# Run 05 — Subtractive v0.2 Maintenance + Access / Frontier Proof

## Baseline

- Branch point: `74640af3774dc8ec4e904e8c13204a632cf8462b` (`Ingest Run 03G final cellar authority`).
- Remote `main` was independently confirmed at the same commit.
- Baseline validation passed: 285 entities, 264 relationships, 229 claims, 156 sources, 14 name assertions, 35 spatial assertions, and 42 profiles.

## Verified maintenance decisions

- Entity `claim_ids`, `name_assertion_ids`, and `spatial_refs` were incomplete reverse caches. All 47 authored pointers were accurate but redundant; forward records remain authoritative.
- Two `market_signal` entities only wrapped three dated claims. The claims now address `wine:ixilune` or `wine:rebel-rebel`; the containers were removed.
- The four analytical-comparison predicates and three `*_AT_TIME` predicates had no authored uses. They remain schema-compatible but are rejected for authored core data.
- One `network_anchor` spatial assertion duplicated graph presentation. It was removed; the real work/location graph remains.
- Twelve wine-to-appellation `WITHIN_APPELLATION` edges expressed legal designation. Their stable relationship IDs and evidence links remain, with predicate changed to `CLASSIFIED_AS`. Ten genuinely spatial containment edges remain unchanged.
- Entity summaries and tags remain display/search metadata. One unsupported identity-crosswalk summary was narrowed; two unsupported designation tags were removed and one was narrowed to geographic `bizkaia`.
- Fifty-nine existing perishable claims gained source-supported `observed_at` dates. No historical effective date was invented.

Compatibility fields and enum values were not physically removed because that would create an unnecessary schema-version boundary. The repository validator rejects their authored use.

## Authority migration

| Family | Before | After | Disposition |
|---|---:|---:|---|
| Entities | 285 | 287 | 2 transient market containers removed; 4 proof entities added; 22 retained records changed |
| Relationships | 264 | 268 | 12 predicates migrated; 3 existing records temporally/narratively narrowed; 4 proof relationships added |
| Claims | 229 | 233 | 3 claims retargeted; 59 existing claims date-backed; 4 proof claims added |
| Sources | 156 | 159 | 3 first-party/trade proof sources added |
| Name assertions | 14 | 14 | no authority change |
| Spatial assertions | 35 | 34 | 1 presentation anchor removed; 1 tenure-bearing description narrowed to spatial truth |
| Reference profiles | 42 | 42 | Béarn gained its separate legal appellation as a component; IDs and canonical paths remain stable |

## Human Reference

- 42 governed canonical pages: 40 published, 1 stub, 1 queued.
- 16 stale, alias, contradictory, or redundant component pages were removed after supported unique prose was moved to canonical profiles.
- Four indexes and every profile provenance block are deterministic projections from machine authority.
- Provenance exposes profile/component IDs, material claim IDs, layer/observation date, status, confidence, source IDs/titles, and unresolved questions without expanding representative-anchor research into unrelated claim dumps.
- Atlas contains 48 Markdown pages: 42 governed pages and 6 permitted navigation/reference pages. Every governed profile is reachable from the Atlas front door.

## Access / Frontier proof

| Case | Representation | Temporal/evidence treatment | Result |
|---|---|---|---|
| Durable importer | Goyo García Viadero `IMPORTED_BY` José Pastor Selections | 2022 trade evidence plus importer portfolio observed 2026-08-18; no start/exclusivity inference | PASS |
| Distributor route | Phelan Farm `DISTRIBUTED_BY` Polaner Selections | Reference relationship bounded to May 2026; Frontier claim cites Polaner's official New York wholesale list and withholds later distribution, stock, other territory, and exclusivity | PASS |
| Retail stock | Rebel Rebel dated availability claim | Buvons observation on 2026-08-18 preserves vintage, $72 price, and two-bottle stock quantity as retailer-specific intelligence | PASS |
| Retail price | Rebel Rebel dated price claim | Leon & Son observation on 2026-08-18 records $69.99 without implying availability | PASS |
| Unavailable observation | Rebel Rebel dated availability claim | Leon & Son `Sold Out` state is separate, retailer-specific Frontier intelligence | PASS |
| Shared facility | Scar of the Sea and Lady of the Sunshine each `CELLAR_IN` Tank Farm | Two first-party sources and 2019 start; no host/client, ownership, or collaboration inference | PASS |
| Vineyard tenure | Moon Hill Farm `FARMED_BY` Hiyu plus sourced farming claim | Farming begins in 2015; observed lease language is preserved without ownership or an invented lease interval | PASS |

The proof revealed no fact that STRATA v0.2 could not represent faithfully. It required no new family, predicate, observation container, cross-project ID registry, or STRATA v0.3.

## Enforcement and validation

The validator now enforces schema and referential integrity plus authored-deprecation gates, appellation endpoint semantics, temporal intervals, Frontier/market dates, price/availability layer rules, Access endpoints, canonical profile paths, deterministic provenance/indexes, Atlas page governance, internal links, and profile reachability.

Validation passed in normal mode and Human Reference write mode; a second write was idempotent. Representative negative fixtures confirmed that the repaired contracts fail closed.

## Next gate

No architectural gate blocks research. CARTA may resume its established three-seed research envelope while keeping Frontier observations dated and requiring future complexity to be earned by a concrete representation failure.
