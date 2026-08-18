# Petit Courbu

**CARTA ID:** `grape:petit-courbu`  
**Type:** grape  
**Status:** active

## Why I should care

Petit Courbu is one of the clearest examples of why CARTA separates biological identity from legal naming. Bizkaiko law can call this grape Hondarrabi Zuri Zerratia without CARTA turning every naming context into a universal synonym claim.

## Identity and naming

| Name | Kind | Jurisdiction | Status | Evidence |
|---|---|---|---|---|
| Hondarrabi Zuri Zerratia | `legal_name` | `appellation:bizkaiko-txakolina` | supported | claim:petit-courbu-bizkaia-name, claim:bizkaia-grape-list |

## Where it fits

| Relationship | Direction | Connected entity | Status | Evidence |
|---|---:|---|---|---|
| `MADE_FROM` | ← | `wine:ixilune` | supported | claim:ixilune-composition |
| `RECOMMENDED_IN` | → | `appellation:bizkaiko-txakolina` | supported | claim:petit-courbu-bizkaia-name, claim:bizkaia-grape-list |
| `MADE_FROM` | ← | `wine:rebel-rebel` | supported | claim:rebel-rebel-style |

## Viticultural / biological structure

A distinct Pyrenean cultivar with low-to-moderate productivity, very small fruit, and more grey-rot susceptibility than Petit Manseng in the retained cultivar evidence.

## What CARTA is watching

The exact cross-registry biological treatment of Hondarrabi Zuri Zerratia versus Petit Courbu remains a P1 research question.

## Claims and confidence

| Claim | Status | Confidence | Statement |
|---|---|---|---|
| `claim:petit-courbu-identity` | supported | high | Plantgrape treats Petit Courbu as a distinct Pyrenean cultivar and lists no officially recognized propagation synonym in France or other EU countries on its record. |
| `claim:petit-courbu-bizkaia-name` | supported | high | The current Bizkaiko Txakolina specification presents Hondarrabi Zuri Zerratia together with Petit Courbu as a recommended/main white variety, creating a jurisdiction-specific legal-name equivalence that should not automatically be generalized into universal synonymy. |
| `claim:bizkaia-grape-list` | supported | high | The current Bizkaiko Txakolina specification lists Hondarrabi Zuri, Hondarrabi Beltza, and Hondarrabi Zuri Zerratia (Petit Courbu) as recommended/main varieties, while Gros Manseng under Izkiriot Haundi and Petit Manseng under Izkiriota Ttipia are authorized varieties subject to the specification's limits. |

## Sources

- `source:plantgrape-petit-courbu` — [Petit Courbu](https://plantgrape.fr/en/varieties/fruit-varieties/210)
- `source:euskadi-bizkaiko-pliego` — Bizkaiko Txakolina consolidated product specification (`source:euskadi-bizkaiko-pliego`)
- `source:eurlex-bizkaiko-2025-amendment` — [Approved standard amendment: Bizkaiko Txakolina / Chacolí de Bizkaia / Txakoli de Bizkaia](https://eur-lex.europa.eu/eli/C/2025/6563/oj/eng)

## Revision history

- Run 01: candidate research.
- STRATA v0.2 ingestion: accepted/normalized proof card.
