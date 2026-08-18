# Petit Manseng

**CARTA ID:** `grape:petit-manseng`  
**Type:** grape  
**Status:** active

## Why I should care

Petit Manseng is one of the best bridges in Run 01 between place, grape physiology, law, style, and the Virginia Lens. It can accumulate substantial sugar while retaining unusually high acidity, and the pilot places it across both Jurançon and Bizkaiko legal contexts without pretending those places are interchangeable.

## Identity and naming

| Name | Kind | Jurisdiction | Status | Evidence |
|---|---|---|---|---|
| Izkiriota Ttipia | `legal_name` | `appellation:bizkaiko-txakolina` | supported | claim:bizkaia-grape-list |

## Where it fits

| Relationship | Direction | Connected entity | Status | Evidence |
|---|---:|---|---|---|
| `MADE_FROM` | ← | `wine:ixilune` | supported | claim:ixilune-composition |
| `TRADITIONAL_IN` | → | `appellation:jurancon` | supported | claim:jurancon-manseng-core-grapes |
| `GENETICALLY_CLOSE_TO` | → | `grape:savagnin` | supported | claim:petit-manseng-savagnin |
| `PERMITTED_IN` | → | `appellation:bizkaiko-txakolina` | supported | claim:bizkaia-grape-list |
| `MADE_FROM` | ← | `wine:rebel-rebel` | supported | claim:rebel-rebel-style |

## Viticultural / biological structure

Very small berries, strong sugar accumulation with high acid retention, vigor requiring thoughtful training, and strong grey-rot resistance in the retained Plantgrape evidence.

## What CARTA is watching

The exact genetic relationship to Gros Manseng remains unresolved in this corpus. Virginia comparisons remain Lens material unless site-level evidence earns a stronger analogy.

## Claims and confidence

| Claim | Status | Confidence | Statement |
|---|---|---|---|
| `claim:petit-manseng-origin-traits` | supported | high | Plantgrape places Petit Manseng's origin in Pyrénées-Atlantiques and describes very small berries, very high acid retention despite strong sugar concentration, vigor requiring trellising/long pruning, and very strong grey-rot resistance. |
| `claim:petit-manseng-savagnin` | supported | high | Plantgrape reports published genetic analyses indicating Petit Manseng is closely related to Savagnin; this is a closeness claim, not a resolved parent-offspring statement in the evidence captured here. |
| `claim:bizkaia-grape-list` | supported | high | The current Bizkaiko Txakolina specification lists Hondarrabi Zuri, Hondarrabi Beltza, and Hondarrabi Zuri Zerratia (Petit Courbu) as recommended/main varieties, while Gros Manseng under Izkiriot Haundi and Petit Manseng under Izkiriota Ttipia are authorized varieties subject to the specification's limits. |
| `claim:jurancon-manseng-core-grapes` | supported | high | INAO describes Petit Manseng and Gros Manseng as the principal local grape varieties of Jurançon. |
| `claim:virginia-pm-performance` | supported | high | Virginia Tech trials found Petit Manseng's loose clusters and very small berries associated with very low fruit-rot incidence in test years, while older Virginia trials documented high Brix alongside substantial retained acidity. |
| `claim:virginia-pm-ripening-2025` | supported | high | A 2025 Virginia Tech study reported Petit Manseng total soluble solids increasing from 8.0 to 23.6 Brix while titratable acidity declined from 25 to 10.8 g/L, with acid depletion plateauing about two weeks after sugar accumulation plateaued in the studied fruit. |

## Sources

- `source:plantgrape-petit-manseng` — [Petit Manseng](https://www.plantgrape.fr/en/varieties/fruit-varieties/211)
- `source:euskadi-bizkaiko-pliego` — Bizkaiko Txakolina consolidated product specification (`source:euskadi-bizkaiko-pliego`)
- `source:eurlex-bizkaiko-2025-amendment` — [Approved standard amendment: Bizkaiko Txakolina / Chacolí de Bizkaia / Txakoli de Bizkaia](https://eur-lex.europa.eu/eli/C/2025/6563/oj/eng)
- `source:inao-jurancon` — [Jurançon](https://www.inao.gouv.fr/produit/jurancon-23319)
- `source:vt-viticulture-2004` — [Viticulture Notes: Petit Manseng in Virginia](https://www.sites.ext.vt.edu/newsletter-archive/viticulture/04december/04december.html)
- `source:vt-enology-123` — [Enology Notes 123: Petit Manseng](https://enology.fst.vt.edu/EN/123.html)
- `source:vt-ripening-2025` — [Ripening Kinetics and Grape Chemistry of Virginia Petit Manseng and Chardonnay](https://vtechworks.lib.vt.edu/items/4cb9fee2-f229-4f56-9c22-be1fb7f11001)

## Revision history

- Run 01: candidate research.
- STRATA v0.2 ingestion: accepted/normalized proof card.
