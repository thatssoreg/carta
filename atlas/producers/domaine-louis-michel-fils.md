# Louis Michel & Fils

**Chablis, France**

Louis Michel & Fils is a Chablis family domaine that presents its winegrowing history as reaching back to 1850. The cellar seed **Chablis Grand Cru Vaudésir** opens a particularly useful CARTA identity problem: Vaudésir is a named Grand Cru climat, the overarching legal appellation is Chablis Grand Cru, and Louis Michel's Vaudésir bottling is a separate durable wine identity.

## Domaine

The domaine's first-party site places Louis Michel & Fils in Chablis and describes Chardonnay as the defining grape of its wines.

It also states that the domaine vinifies exclusively in stainless steel.

Run 03E provided a more elaborate family genealogy and current-person roster than the strongest recovered evidence warrants. CARTA keeps the baseline profile centered on the producer, site, wine, grape, and legal geography until those people relationships are better sourced.

## Vaudésir: climat versus appellation

INAO publishes **Chablis Grand Cru Vaudésir** within the governing Chablis Grand Cru AOP framework. The Chablis wine board identifies Vaudésir as one of seven named Grand Cru climats.

CARTA therefore models:

- `appellation:chablis-grand-cru` as the legal appellation;
- `vineyard:vaudesir` as the named climat/site;
- `wine:louis-michel-chablis-grand-cru-vaudesir` as the Louis Michel wine.

These are related but not interchangeable identities.

## The Vaudésir climat

The Chablis wine board describes Vaudésir as approximately 15.4 hectares in a natural amphitheater, with contrasting exposures, significant clay, and Kimmeridgian marly limestone.

Louis Michel's own parcel must be kept distinct from climat-wide descriptions. The domaine describes its parcel as north-facing, with white clay and limestone, chalk on steeper parts, and browner clay toward the west. It gives planting years of 1950, 1960, and 1970.

## In the cellar

For Vaudésir, Louis Michel describes:

- no added yeasts and long indigenous-yeast fermentation in temperature-controlled tanks;
- spontaneous malolactic fermentation;
- 18 to 20 months of maturation only in stainless steel;
- bentonite fining if necessary;
- one light filtration before bottling.

These are current producer-described practices for the wine, not legal Chablis Grand Cru requirements.

## A major Run 03E correction

The research report claimed that Chablis Grand Cru legally requires 12 months in oak. That cannot survive reconciliation. The same report also described Louis Michel as making its Vaudésir only in stainless steel, and the producer explicitly confirms 18 to 20 months in stainless steel.

Run 03E also accidentally wrote that “Huet's” Grand Cru bottles were made in steel inside the Louis Michel dossier. That is direct cross-dossier contamination and was rejected.

## Spatial status

Vaudésir is anchored to Chablis Grand Cru and the right-bank Chablis landscape. CARTA does not store the report's unsupported 300–330 metre elevation or its erroneous Saint-Martin-sur-Choisille placement.

Official delimitation resources can support a future geometry ingestion pass.

## Explore next

official Vaudésir geometry · current people/leadership · parcel-level geology · Chablis Grand Cru legal specification

## Sources

Primary CARTA source records include Louis Michel & Fils' current first-party site, INAO's current Chablis Grand Cru Vaudésir page, and the Chablis wine board's Vaudésir climat reference.

<!-- BEGIN GENERATED CARTA NAVIGATION -->
## Explore CARTA

This section is generated from governed profile dispositions, editorial anchors, and supported graph relationships. It is not a hand-maintained second knowledge graph.

- [Chablis Grand Cru AOP](../countries/france/appellations/chablis-grand-cru.md) — appellation; navigation node
- [Chardonnay](../grapes/chardonnay.md) — grape; navigation node
- [France](../countries/france/README.md) — country; baseline reference
- [Domaine de Saint Pierre / Château Renard](domaine-de-saint-pierre-jura.md) — producer; baseline reference
- [Domaine Labet](domaine-labet.md) — producer; navigation node
- [Hiyu Wine Farm](hiyu-wine-farm.md) — producer; baseline reference
- [Scar of the Sea / Bassi Vineyard](scar-of-the-sea.md) — producer; baseline reference
<!-- END GENERATED CARTA NAVIGATION -->

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:domaine-louis-michel-fils`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `producer:domaine-louis-michel-fils`

**Component entities**

- `producer:domaine-louis-michel-fils`
- `vineyard:vaudesir`
- `wine:louis-michel-chablis-grand-cru-vaudesir`

**Representative anchors**

- `wine:louis-michel-chablis-grand-cru-vaudesir`
- `vineyard:vaudesir`
- `grape:chardonnay`
- `appellation:chablis-grand-cru`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:louis-michel-chablis-location` | `reference / —` | `supported` | `high` | `source:louis-michel-home`, `source:inao-chablis-grand-cru-vaudesir` |
| `claim:louis-michel-since-1850` | `reference / —` | `supported` | `high` | `source:louis-michel-home` |
| `claim:louis-michel-stainless` | `reference / 2026-08-18` | `supported` | `high` | `source:louis-michel-home`, `source:louis-michel-grand-cru` |
| `claim:louis-michel-vaudesir-cellar` | `reference / 2026-08-18` | `supported` | `high` | `source:louis-michel-grand-cru` |
| `claim:louis-michel-vaudesir-parcel` | `reference / —` | `supported` | `high` | `source:louis-michel-grand-cru` |
| `claim:louis-michel-vaudesir-plantings` | `reference / —` | `supported` | `high` | `source:louis-michel-grand-cru` |
| `claim:louis-michel-vaudesir-wine` | `reference / —` | `supported` | `high` | `source:louis-michel-grand-cru` |
| `claim:vaudesir-chablis-grand-cru` | `reference / —` | `supported` | `high` | `source:inao-chablis-grand-cru-vaudesir`, `source:chablis-vaudesir` |
| `claim:vaudesir-climat-context` | `reference / —` | `supported` | `high` | `source:chablis-vaudesir` |

### Sources

- `source:chablis-vaudesir` — Vaudésir | The Climats of Chablis
- `source:inao-chablis-grand-cru-vaudesir` — Chablis Grand Cru Vaudésir
- `source:louis-michel-grand-cru` — Chablis Grand Crus | Louis Michel & Fils
- `source:louis-michel-home` — Louis Michel & Fils

</details>

### Open questions

- Add current people only after a stronger first-party role source is recovered
- Acquire official climat geometry from the governing boundary source rather than digitizing descriptive maps
- Deepen Chablis geology at parcel resolution without projecting climat-wide descriptions onto a producer parcel
<!-- END GENERATED CARTA PROVENANCE -->
