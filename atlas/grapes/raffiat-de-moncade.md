# Raffiat de Moncade

**CARTA ID:** `grape:raffiat-de-moncade`  
**Type:** grape  
**Status:** active

## Why I should care

Raffiat de Moncade was the pilot's most surprising ampelographic node. Rather than remaining an obscure Béarn grape, it opens a documented lineage backward to proposed parents Gouais blanc and Bouchalès and forward to Arriloba.

## Where it fits

| Relationship | Direction | Connected entity | Status | Evidence |
|---|---:|---|---|---|
| `PROPOSED_PARENT_OF` | ← | `grape:bouchales` | supported | claim:raffiat-parentage |
| `PROPOSED_PARENT_OF` | ← | `grape:gouais-blanc` | supported | claim:raffiat-parentage |
| `MADE_FROM` | ← | `wine:ixilune` | supported | claim:ixilune-composition |
| `PARENT_OF` | → | `grape:arriloba` | supported | claim:raffiat-arriloba |

## Viticultural / biological structure

Plantgrape reports probable Gouais blanc × Bouchalès parentage. Raffiat was then crossed with Sauvignon by INRA in 1954 to create Arriloba.

## What CARTA is watching

The parentage remains explicitly proposed/probable rather than stronger certainty than the source warrants.

## Claims and confidence

| Claim | Status | Confidence | Statement |
|---|---|---|---|
| `claim:raffiat-parentage` | supported | high | Plantgrape reports Raffiat de Moncade as probably resulting from a cross between Gouais blanc and Bouchalès. |
| `claim:raffiat-arriloba` | supported | high | Arriloba was obtained by INRA in 1954 by crossing Raffiat de Moncade and Sauvignon. |
| `claim:bearn-history` | supported | high | INAO historical material records a broad older Béarn white-grape mix, vineyard decline after nineteenth-century scale, disease and wartime disruption, VDQS recognition in 1951, and AOC recognition in 1975. |

## Sources

- `source:plantgrape-raffiat` — [Raffiat de Moncade](https://plantgrape.fr/fr/varietes/varietes-a-fruits/231)
- `source:plantgrape-arriloba` — [Arriloba](https://www.plantgrape.fr/en/varieties/fruit-varieties/19)
- `source:inao-bearn` — [Béarn blanc and cahier des charges](https://www.inao.gouv.fr/produit/bearn-blanc-20046)

## Revision history

- Run 01: candidate research.
- STRATA v0.2 ingestion: accepted/normalized proof card.
