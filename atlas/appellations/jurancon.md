# Jurançon

**CARTA ID:** `appellation:jurancon`  
**Type:** appellation  
**Status:** active

## Why I should care

Jurançon is a legal wine system and a physical foothill landscape. It is central to Run 01 because Petit Manseng and Gros Manseng are principal local grapes there, while the official landscape description gives CARTA a concrete oceanic/Pyrenean site context.

## Typed relationships

| Relationship | Direction | Connected entity | Status | Evidence |
|---|---:|---|---|---|
| `TRADITIONAL_IN` | ← | `grape:gros-manseng` | supported | claim:jurancon-manseng-core-grapes |
| `LOCATED_IN` | → | `place:france` | supported | claim:jurancon-country |
| `TRADITIONAL_IN` | ← | `grape:petit-manseng` | supported | claim:jurancon-manseng-core-grapes |

## Spatial representation

| Spatial record | Kind | Precision | Status | Description |
|---|---|---|---|---|
| `spatial:jurancon-source-described-area` | `source_described_area` | descriptive | supported | INAO describes Jurançon as hillside and terrace viticulture in the Pyrenean foothills under oceanic influence, with a warm dry southerly wind frequent in autumn. |

## What CARTA is watching

Official polygon geometry has not yet been ingested. Current legal text is time-bound and should be versioned as future amendments appear.

## Claims and confidence

| Claim | Status | Confidence | Statement |
|---|---|---|---|
| `claim:jurancon-terrain-law` | supported | high | INAO describes Jurançon as hillside viticulture at the Pyrenean foothills under an oceanic climate with a frequent warm, dry southerly autumn wind; sweet wines were recognized in 1936 and dry Jurançon in 1975, with hand harvesting linked to high-trained vines and steep terrain. |
| `claim:jurancon-manseng-core-grapes` | supported | high | INAO describes Petit Manseng and Gros Manseng as the principal local grape varieties of Jurançon. |
| `claim:jurancon-country` | supported | high | Jurançon is a French AOP documented by INAO. |

## Sources

- `source:inao-jurancon` — [Jurançon](https://www.inao.gouv.fr/produit/jurancon-23319)

## Revision history

- Run 01: candidate research.
- STRATA v0.2 ingestion: first human-readable appellation surface.
