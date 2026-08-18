# Imanol Garay

**CARTA ID:** `producer:imanol-garay`  
**Type:** producer  
**Status:** active

## Why this producer matters in CARTA

Imanol Garay is the central transmission node in Run 01. His work history reaches Richard Leroy, his collaborative work reaches Alfredo Egia and Gile Iturriondobeitia, and his geography spans the Maslacq/Orthez context and Saint-Étienne-de-Baïgorry.

## Place and farming footprint

| Spatial record | Kind | Precision | Status | Description |
|---|---|---|---|---|
| `spatial:imanol-garay-baigorry-vines` | `reference_location` | municipality | provisional | A recent importer profile reports about one hectare of Garay's own vines in Saint-Étienne-de-Baïgorry, described as just outside the Irouléguy appellation limits. Parcel geometry is not yet known. |
| `spatial:imanol-garay-cellar-maslacq` | `reference_location` | locality | provisional | Recent trade reporting places Garay's cellar in Maslacq. Earlier sources use Orthez or near Orthez, so this is a provisional current locality rather than an exact address. |

## Typed relationships

| Relationship | Direction | Connected entity | Status | Evidence |
|---|---:|---|---|---|
| `CELLAR_IN` | → | `place:maslacq` | provisional | claim:imanol-cellar-maslacq |
| `FARMS_IN` | → | `place:saint-etienne-de-baigorry` | provisional | claim:imanol-baigorry-vines |
| `MADE_BY` | ← | `wine:ixilune` | supported | claim:ixilune-composition |

## Key wines / projects

- [Ixilune](../wines/ixilune.md)

## What CARTA is watching

The current principal cellar locality remains provisional because recent Maslacq reporting and older Orthez descriptions do not yet have a producer-confirmed chronology. Parcel tenure also remains more nuanced than the current relationship schema can fully express.

## Claims and confidence

| Claim | Status | Confidence | Statement |
|---|---|---|---|
| `claim:imanol-cellar-maslacq` | provisional | medium | Recent trade reporting locates Imanol Garay's cellar in Maslacq, while earlier trade sources described it as Orthez or near Orthez; this appears to reflect changing or imprecise locality descriptions rather than evidence of two simultaneous main cellars. |
| `claim:imanol-baigorry-vines` | provisional | medium | A recent importer profile reports about one hectare of Garay's own vines in Saint-Étienne-de-Baïgorry, just outside the Irouléguy appellation limits, plus another hectare near Orthez. |
| `claim:ixilune-composition` | supported | medium | Imanol Garay's Ixilune has been documented in different vintages as a blend centered on Raffiat de Moncade with Petit Manseng and Petit Courbu, and sometimes Gros Manseng; blend proportions and maceration vary by vintage. |

## Sources

- `source:beattie-imanol` — [Imanol Garay, Maslacq, Pyrénées-Atlantiques](https://www.beattieandroberts.com/producers/imanol-garay)
- `source:sourceimports-imanol-2022` — [Newsletter June 2022: Imanol Garay](https://thesourceimports.com/newsletter-june-2022/)
- `source:orange-imanol-2022` — [Imanol Garay, the emotions of a wine](https://www.orangewines.es/en/imanol-garay/)

## Revision history

- Run 01: candidate research.
- STRATA v0.2 ingestion: accepted/normalized proof card.
