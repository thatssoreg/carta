# Clos Apalta / Domaines Bournet-Lapostolle

**Apalta Valley, Colchagua, Chile**

The cellar seed **Le Petit Clos** resolves into a layered identity system: a Bournet-Lapostolle producer/company, the Clos Apalta estate/project, the Clos Apalta vineyard, the flagship wine also named Clos Apalta, and the distinct recurring wine Le Petit Clos.

CARTA keeps those identities separate.

## Family and project

Clos Apalta's first-party history places Alexandra Marnier Lapostolle's Chilean venture in **1994**. The current team page identifies Charles-Henri de Bournet Marnier Lapostolle as President and CEO since 2013, Andrea Leon as Technical Director, and Michel Rolland as a consultant personally involved since 1997.

The Run 03F-B report contained several unstable corporate-sale and reacquisition dates. Those were not necessary for the baseline profile and were not ingested.

## Le Petit Clos

Le Petit Clos is a durable named wine in the Clos Apalta portfolio, distinct from both the estate/project and the flagship Clos Apalta wine.

Its blend is explicitly vintage-variable:

- **2020:** 40% Carmenère, 38% Cabernet Sauvignon, 19% Merlot, 3% Petit Verdot;
- **2021:** 68% Carmenère, 16% Cabernet Sauvignon, 15% Merlot, 1% Cabernet Franc;
- **2022:** 59% Carmenère, 33% Cabernet Sauvignon, 5% Merlot, 3% Cabernet Franc.

CARTA therefore does not encode a timeless Le Petit Clos percentage formula.

## Apalta law

Chile's **Decree 56**, published 25 May 2018, added **Apalta** as a legally named viticultural Area within **Valle de Colchagua**. The decree defines the area's limit through the rural locality of Apalta in the commune of Santa Cruz.

CARTA represents this as `appellation:apalta` for legal-origin semantics, but does not pretend the Chilean zoning object is structurally identical to a French AOP.

The 2021 and 2022 Le Petit Clos pages explicitly use Apalta as the wine's appellation; the Spanish 2022 page says `D.O. Apalta`.

## Vineyard

Clos Apalta describes its vineyard as 60 hectares at the entrance of Apalta Valley, mostly southeast-facing, with old vines, substantial granite-derived soils and elevations between 150 and 300 metres.

These are estate-wide descriptors. They are not automatically parcel-level facts about every vintage of Le Petit Clos.

The estate states that it has been certified organic since 2009 and currently farms the 60 hectares organically. It also describes experience with biodynamic vineyard management; CARTA does not convert that phrasing into a separate biodynamic-certification claim.

## GIS status

The vineyard is anchored to Apalta Valley and the legal Apalta/Colchagua geography without guessed coordinates. Future work should acquire authoritative Area Apalta and vineyard geometry.

## Explore next

legal-company/public-brand naming chronology · parcel-level Le Petit Clos sourcing · vintage élevage history · official Apalta geometry · Clos Apalta flagship-wine history

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:clos-apalta`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `project:clos-apalta`

**Component entities**

- `producer:domaines-bournet-lapostolle-chile`
- `project:clos-apalta`
- `vineyard:clos-apalta-vineyard`
- `wine:clos-apalta`
- `wine:le-petit-clos`
- `person:alexandra-marnier-lapostolle`
- `person:cyril-de-bournet`
- `person:charles-henri-de-bournet-marnier-lapostolle`
- `person:andrea-leon`
- `person:michel-rolland`

**Representative anchors**

- `wine:le-petit-clos`
- `wine:clos-apalta`
- `vineyard:clos-apalta-vineyard`
- `appellation:apalta`
- `place:apalta-valley`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:apalta-legal-area-2018` | `reference / —` | `supported` | `high` | `source:sag-apalta-decree-56` |
| `claim:clos-apalta-leadership` | `reference / 2026-08-18` | `supported` | `high` | `source:clos-apalta-history`, `source:clos-apalta-team` |
| `claim:clos-apalta-organic-since-2009` | `reference / 2026-08-18` | `supported` | `high` | `source:clos-apalta-philosophy` |
| `claim:clos-apalta-project-identity` | `reference / —` | `supported` | `high` | `source:clos-apalta-history`, `source:clos-apalta-winery` |
| `claim:clos-apalta-vineyard-context` | `reference / —` | `supported` | `high` | `source:clos-apalta-vineyard` |
| `claim:le-petit-clos-2020-blend` | `reference / —` | `supported` | `high` | `source:le-petit-clos-2020` |
| `claim:le-petit-clos-2021-blend` | `reference / —` | `supported` | `high` | `source:le-petit-clos-2021` |
| `claim:le-petit-clos-2022-blend` | `reference / —` | `supported` | `high` | `source:le-petit-clos-2022` |
| `claim:le-petit-clos-identity` | `reference / —` | `supported` | `high` | `source:le-petit-clos`, `source:clos-apalta-history` |

### Sources

- `source:clos-apalta-history` — The Domaine — History
- `source:clos-apalta-philosophy` — The Domaine — Philosophy
- `source:clos-apalta-team` — The Domaine — Team
- `source:clos-apalta-vineyard` — The Domaine — Vineyard
- `source:clos-apalta-winery` — The Domaine — Winery
- `source:le-petit-clos` — Le Petit Clos
- `source:le-petit-clos-2020` — Le Petit Clos 2020
- `source:le-petit-clos-2021` — Le Petit Clos 2021
- `source:le-petit-clos-2022` — Le Petit Clos 2022
- `source:sag-apalta-decree-56` — Decreto 56 — Modifica zonificación vitícola

</details>

### Open questions

- Resolve legal-company versus public-facing Domaine Bournet-Lapostolle naming over time
- Acquire authoritative geometry for Area Apalta and Clos Apalta parcels
- Extend vintage-scoped Le Petit Clos blend and élevage history without universalizing percentages
<!-- END GENERATED CARTA PROVENANCE -->
