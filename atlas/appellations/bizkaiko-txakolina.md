# Bizkaiko Txakolina

**CARTA ID:** `appellation:bizkaiko-txakolina`  
**Type:** appellation  
**Status:** active

## Why I should care

Bizkaiko Txakolina is one of the strongest demonstrations of CARTA's cross-border naming model. Current law connects Petit Courbu, Petit Manseng, and Gros Manseng to Basque legal names and changed Petit Courbu / Hondarrabi Zuri Zerratia to recommended/main status in 2025.

## Typed relationships

| Relationship | Direction | Connected entity | Status | Evidence |
|---|---:|---|---|---|
| `LOCATED_IN` | → | `place:spain` | supported | claim:bizkaiko-geographical-area |
| `PERMITTED_IN` | ← | `grape:gros-manseng` | supported | claim:bizkaia-grape-list |
| `RECOMMENDED_IN` | ← | `grape:petit-courbu` | supported | claim:petit-courbu-bizkaia-name, claim:bizkaia-grape-list |
| `PERMITTED_IN` | ← | `grape:petit-manseng` | supported | claim:bizkaia-grape-list |

## Names

| Name | Kind | Jurisdiction | Status | Evidence |
|---|---|---|---|---|
| Chacolí de Bizkaia | `legal_name` | `place:spain` | supported | claim:bizkaiko-legal-names |
| Txakoli de Bizkaia | `legal_name` | `place:spain` | supported | claim:bizkaiko-legal-names |

## Spatial representation

| Spatial record | Kind | Precision | Status | Description |
|---|---|---|---|---|
| `spatial:bizkaiko-source-described-area` | `source_described_area` | regional | supported | The current EU PDO record defines the geographical area as eligible registered land within municipalities of Bizkaia, Spain. Official polygon geometry has not yet been ingested. |

## What CARTA is watching

Official polygon geometry remains to be acquired. Legal grape status should always be read with a date/version.

## Claims and confidence

| Claim | Status | Confidence | Statement |
|---|---|---|---|
| `claim:bizkaia-grape-list` | supported | high | The current Bizkaiko Txakolina specification lists Hondarrabi Zuri, Hondarrabi Beltza, and Hondarrabi Zuri Zerratia (Petit Courbu) as recommended/main varieties, while Gros Manseng under Izkiriot Haundi and Petit Manseng under Izkiriota Ttipia are authorized varieties subject to the specification's limits. |
| `claim:petit-courbu-bizkaia-name` | supported | high | The current Bizkaiko Txakolina specification presents Hondarrabi Zuri Zerratia together with Petit Courbu as a recommended/main white variety, creating a jurisdiction-specific legal-name equivalence that should not automatically be generalized into universal synonymy. |
| `claim:bizkaiko-geographical-area` | supported | high | The current EU record defines the Bizkaiko Txakolina PDO geographical area as eligible registered land within municipalities of Bizkaia, Spain. |
| `claim:bizkaiko-legal-names` | supported | high | The current EU record protects the names Bizkaiko Txakolina, Chacolí de Bizkaia, and Txakoli de Bizkaia for the PDO. |
| `claim:txakoli-term` | supported | high | A 2024 Basque Government order reserves the traditional term Chacolí / Txakolina / Txakoli to wines entitled to use the Bizkaia, Getaria, or Álava protected designations named in the order. |

## Sources

- `source:euskadi-bizkaiko-pliego` — Bizkaiko Txakolina consolidated product specification (`source:euskadi-bizkaiko-pliego`)
- `source:eurlex-bizkaiko-2025-amendment` — [Approved standard amendment: Bizkaiko Txakolina / Chacolí de Bizkaia / Txakoli de Bizkaia](https://eur-lex.europa.eu/eli/C/2025/6563/oj/eng)
- `source:plantgrape-petit-courbu` — [Petit Courbu](https://plantgrape.fr/en/varieties/fruit-varieties/210)
- `source:euskadi-txakoli-term` — [Conditions of use of the traditional term Chacolí / Txakolina / Txakoli](https://www.euskadi.eus/bopv2/datos/2024/04/2401611a.shtml)

## Revision history

- Run 01: candidate research.
- STRATA v0.2 ingestion: first human-readable appellation surface.
