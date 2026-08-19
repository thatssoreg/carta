# Pyrenean Atlantic

**CARTA ID:** `ecosystem:pyrenean-atlantic`  
**Type:** analytical ecosystem  
**Status:** active  
**Pilot:** Deep Research Run 01

> **What this is not:** a single appellation, government region, historical territory, or claim that the Loire is part of the Pyrenees.

## Why I should care

Run 01 found something more useful than a conventional regional survey: a **braided ecosystem** in which several different geographies and relationship systems overlap.

1. Atlantic Basque wine-law geography, especially Bizkaiko, Getariako, and Arabako Txakolina.
2. French Basque geography around Irouléguy.
3. The Béarn / Jurançon / Pacherenc wine world of the northern Pyrenean foothills.
4. A professional transmission network that reaches geographically outward to Richard Leroy in the Loire.

The national border matters enormously for law, protected names, and legal grape terminology. It is not enough to explain producer careers, collaboration, grape-name systems, technical exchange, or fruit sourcing.

## Where it fits

- [Bizkaia](../countries/spain/regions/bizkaia.md)
- [Béarn](../countries/france/regions/bearn.md)
- [Jurançon](../countries/france/appellations/jurancon.md)
- [Bizkaiko Txakolina](../countries/spain/appellations/bizkaiko-txakolina.md)
- [Irouléguy](../countries/france/appellations/irouleguy.md)
- [Pacherenc du Vic-Bilh](../countries/france/appellations/pacherenc-du-vic-bilh.md)
- [Spain](../countries/spain/README.md)
- [France](../countries/france/README.md)

## Grape / naming / genetic network

The strongest lesson is that similar-looking names do not create a family tree.

- [Petit Manseng](../grapes/petit-manseng.md) and [Gros Manseng](../grapes/gros-manseng.md) are central local grapes in Jurançon, but Run 01 did not establish a parent-offspring relationship between them.
- [Petit Courbu](../grapes/petit-courbu.md) is legally named **Hondarrabi Zuri Zerratia** in the Bizkaiko context without CARTA turning that jurisdictional equivalence into universal biological synonymy.
- [Courbu](../grapes/courbu.md) has a different naming pattern, including Hondarrabi Zuri in Spain.
- [Raffiat de Moncade](../grapes/raffiat-de-moncade.md) unexpectedly produced the cleanest pedigree thread in the pilot, reaching backward to proposed parents Gouais blanc and Bouchalès and forward to Arriloba.

## Producer and cultural-transmission network

The core documented path is deliberately typed rather than flattened into a single lineage story:

- [Alfredo Egia](../producers/alfredo-egia.md) `MENTORED_BY` [Imanol Garay](../producers/imanol-garay.md)
- Imanol Garay `WORKED_WITH` [Richard Leroy](../producers/richard-leroy.md)
- Alfredo Egia, Imanol Garay, and Gile Iturriondobeitia collaborated in Hegan Egin

CARTA does **not** ingest an Alfredo Egia → Richard Leroy mentorship or collaboration edge.

## Spatial model

| Spatial record | Kind | Precision | Status | Description |
|---|---|---|---|---|
| `spatial:pyrenean-atlantic-analytical-area` | `analytical_area` | descriptive | supported | CARTA's Run 01 analytical ecosystem braids Atlantic Basque wine-law geography, French Basque/Irouléguy geography, the Béarn/Jurançon/Pacherenc foothill wine world, and non-spatial professional relationships. It is not an official boundary. |

The first map should therefore be relational. Exact parcels and official polygons can be added when acquired, but useful spatial knowledge is already present without manufacturing precision.

## Timeline

| Date | What changed | Why it matters |
|---|---|---|
| 1936 | Sweet Jurançon recognition | Legal wine identity becomes time-bound rather than timeless. |
| 1951 | Béarn VDQS recognition | Predecessor legal stage before AOC. |
| 1954 | Arriloba created from Raffiat de Moncade × Sauvignon | Institutional breeding enters the grape network. |
| 1975 | Dry Jurançon recognition and Béarn AOC recognition | Modern legal categories diverge within an older grape landscape. |
| 2024 | Basque traditional-term rules revised | Naming remains jurisdictional and temporal. |
| 2025 | Bizkaiko amendment changes Petit Courbu / Hondarrabi Zuri Zerratia to recommended/main | A current law change directly alters the grape/appellation relationship. |
| 2026-08-18 | Rebel Rebel retail observations captured | Access is a dated Frontier signal, not a permanent fact. |

## What CARTA is watching

- Exact Garay cellar chronology: Maslacq versus older Orthez descriptions.
- Garay's Saint-Étienne-de-Baïgorry parcel relative to the Irouléguy boundary.
- Gile / Guillermo Iturriondobeitia identity crosswalk.
- More precise parcel, hydrology, geology, slope, and official appellation geometry.
- The current importer/distributor path for Garay and Hegan Egin.
- Whether repeated future research justifies first-class parcel tenure or vintage-bottling entities.

## Rejected edges

The pilot deliberately rejected or withheld:

- Alfredo Egia `MENTORED_BY` Richard Leroy
- Alfredo Egia `WORKED_WITH` Richard Leroy
- Imanol Garay `MENTORED_BY` Richard Leroy
- Petit Manseng `PARENT_OF` / `OFFSPRING_OF` Gros Manseng
- Courbu `MUTATION_OF` Courbu noir
- Virginia `CLIMATE_ANALOGUE_OF` Jurançon (analytical comparison; keep external to CARTA core)

The withheld identity, work, and genetic relationships may be reopened only with better evidence. Analytical comparison remains in external analytical layers rather than reopening as core authority.

## Why these things are connected

The ecosystem hangs together because **cultivar continuity, jurisdictional naming, mountain-and-Atlantic geography, producer mobility, collaboration, and market access repeatedly intersect**.

Law separates the landscape into protected systems. Grapes and names cross those systems. People reconnect them through work and collaboration. Markets then expose some parts of that network much more visibly than others. The useful boundary is therefore generated by explanatory relationships rather than drawn in advance on a political map.

## Research record

See [`research/run-01-pyrenean-atlantic/`](../../research/run-01-pyrenean-atlantic/).

**Last normalized against STRATA:** v0.2

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:pyrenean-atlantic`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `ecosystem:pyrenean-atlantic`

**Component entities**

- `ecosystem:pyrenean-atlantic`

**Representative anchors**

- `person:alfredo-egia`
- `person:imanol-garay`
- `person:richard-leroy`
- `grape:petit-manseng`
- `grape:petit-courbu`
- `appellation:jurancon`
- `appellation:bizkaiko-txakolina`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:pyrenean-atlantic-ecosystem-synthesis` | `reference / —` | `supported` | `medium` | `source:carta-run-01-report` |

### Sources

- `source:carta-run-01-report` — CARTA Pyrenean Atlantic Ecosystem Pilot — Deep Research Run 01

</details>

### Open questions

- Acquire true GIS geometry and richer hydrology/geology layers
<!-- END GENERATED CARTA PROVENANCE -->
