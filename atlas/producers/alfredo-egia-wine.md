# Alfredo Egia Wine

**CARTA ID:** `producer:alfredo-egia-wine`  
**Type:** producer  
**Status:** active

## Why this producer matters in CARTA

Alfredo Egia's producer work is a key Run 01 node because it connects Balmaseda/Bizkaia, Petit Manseng and Petit Courbu, a three-person collaboration, and a contemporary stylistic expression that sits inside the Basque legal world without being reducible to a generic Txakoli stereotype.

## Place and farming footprint

| Spatial record | Kind | Precision | Status | Description |
|---|---|---|---|---|
| `spatial:alfredo-egia-balmaseda` | `reference_location` | municipality | supported | Producer work is associated with vineyards in and around Balmaseda, Bizkaia. This is municipality/locality-level placement, not a vineyard point. |

## Typed relationships

| Relationship | Direction | Connected entity | Status | Evidence |
|---|---:|---|---|---|
| `FARMS_IN` | → | `place:balmaseda` | supported | claim:alfredo-balmaseda |
| `MADE_BY` | ← | `wine:rebel-rebel` | supported | claim:rebel-rebel-style |

## Key wines / projects

- [Rebel Rebel](../wines/rebel-rebel.md)

## What CARTA is watching

Exact vineyard parcels and current geometry are not yet ingested. The producer entity remains distinct from the person Alfredo Egia and from the Hegan Egin project.

## Claims and confidence

| Claim | Status | Confidence | Statement |
|---|---|---|---|
| `claim:alfredo-balmaseda` | supported | high | Alfredo Egia's producer work is associated with vineyards in Balmaseda within Bizkaiko Txakolina. |
| `claim:rebel-rebel-style` | supported | medium | Current importer descriptions document whole-cluster direct pressing, spontaneous barrel/amphora fermentation, extended lees aging, some intentionally untopped élevage, and very low or no added sulfur depending on vintage, making Rebel Rebel structurally atypical relative to the light, brisk txakoli stereotype without proving it is historically unprecedented. |

## Sources

- `source:sager-alfredo` — [Alfredo Egia](https://www.sagerandwine.com/alfredoegia)
- `source:sourceimports-alfredo-2022` — [Newsletter March 2022: Alfredo Egia and Imanol Garay](https://thesourceimports.com/newsletter-march-2022/)
- `source:pellicle-alfredo-2025` — [Txakolí, Creativity, and Subversion in Basque Country, Spain](https://www.pelliclemag.com/home/2025/4/29/the-devils-crayon-txakol-creativity-and-subversion-in-basque-country-spain)

## Revision history

- Run 01: candidate research.
- STRATA v0.2 ingestion: accepted/normalized proof card.
