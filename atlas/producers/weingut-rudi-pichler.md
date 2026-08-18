# Weingut Rudi Pichler

**Wösendorf, Wachau, Austria**

Weingut Rudi Pichler is a Wösendorf estate whose cellar seed **Riesling Hochrain Smaragd** opens a CARTA world around Ried Hochrain, Wachau DAC, Riesling, Vinea Wachau, Codex Wachau, and the important distinction between government origin law and association-owned wine-style categories.

## Estate

The producer states that the Pichler family has practiced viticulture in Wösendorf since 1731 and currently cultivates 15 hectares. Its current breakdown is 65% Grüner Veltliner, 30% Riesling, with the balance in Weissburgunder and Roter Veltliner.

CARTA does not ingest the Run 03F-A claim that Hochrain itself represents 53 acres of Pichler holdings. Vinea Wachau records **27.46 hectares as the total Ried area**, across multiple growers including Rudi Pichler. Vineyard size is not producer holding size.

## Ried Hochrain

Vinea Wachau records Hochrain as:

- town: Wösendorf;
- total Ried size: 27.46 ha;
- altitude: 215–380 m;
- southeast aspect;
- terraced;
- first documentary evidence: 1334.

Vinea describes black soil over deep loess. Rudi Pichler's own geology page likewise identifies major loess deposits as the basis of Ried Hochrain.

These are site-wide descriptors, not coordinates or parcel boundaries for the producer's specific vines.

## Riesling Hochrain Smaragd

Rudi Pichler's first-party wine page presents **Riesling Hochrain Smaragd** as a Riesling associated with the Wösendorf top site Hochrain, with vines up to roughly forty years old.

CARTA treats this as one durable wine identity across vintages. Vintage-specific alcohol, fermentation, sulfur, or élevage data are not universalized.

## Smaragd versus Wachau DAC

This is the key ontology correction from Run 03F-A.

Rudi Pichler explicitly describes Steinfeder®, Federspiel®, and Smaragd® as quality categories established by **Vinea Wachau** under the Codex Wachau. Vinea Wachau states that these names are registered trademarks restricted to its member wineries and currently describes Smaragd as at least 12.5% alcohol by volume.

Wachau DAC is a separate government origin hierarchy. Vinea itself says the DAC system supplements its established Steinfeder, Federspiel, and Smaragd brands.

Austria's federal Wachau DAC regulation §4 governs Riedenwein: it permits Grüner Veltliner or Riesling, prohibits enrichment, requires a Ried name to be used with Wachau DAC, and requires the locality name on the main label.

CARTA therefore keeps:

- `classification:smaragd` as a Vinea Wachau category/trademark;
- `appellation:wachau-dac` as the legal origin system;
- `vineyard:ried-hochrain` as the named site;
- `place:wosendorf` as the locality;
- the Pichler wine as a separate persistent wine identity.

## Run 03F-A corrections

The research report improved substantially but still failed its own mechanical audit:

- it treated an older 13% source as creating a current “contested” Smaragd threshold even though current Vinea authority states at least 12.5%;
- it sometimes blurred Vinea rules with DAC law;
- it supplied approximate coordinates despite claiming the coordinate audit was clean;
- it confused total Ried size with estate holdings;
- it attributed detailed wine-level cellar practices more broadly than the recovered first-party wine page supports.

Those overreaches were not ingested.

## GIS status

Vinea Wachau supplies strong source-described spatial information for Hochrain. No approximate coordinates from Run 03F-A were accepted. Future work should acquire authoritative Ried geometry.

## Explore next

official Ried geometry · current Pichler leadership/personnel · wine-specific vintage technical sheets · historical interaction between Codex Wachau and post-2020 DAC labeling

## Sources

Primary CARTA sources include Rudi Pichler's current estate, wine, vineyard, and wine-style pages; Vinea Wachau's Hochrain, wine-style, and DAC pages; and Austria's federal Wachau DAC regulation.

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:weingut-rudi-pichler`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `producer:weingut-rudi-pichler`

**Component entities**

- `producer:weingut-rudi-pichler`
- `person:rudi-pichler`
- `vineyard:ried-hochrain`
- `wine:rudi-pichler-riesling-hochrain-smaragd`
- `classification:smaragd`
- `institution:vinea-wachau`

**Representative anchors**

- `wine:rudi-pichler-riesling-hochrain-smaragd`
- `vineyard:ried-hochrain`
- `grape:riesling`
- `appellation:wachau-dac`
- `classification:smaragd`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:hochrain-loess` | `reference / —` | `supported` | `high` | `source:vinea-hochrain`, `source:rudi-pichler-vineyards` |
| `claim:hochrain-site` | `reference / —` | `supported` | `high` | `source:vinea-hochrain`, `source:rudi-pichler-vineyards` |
| `claim:pichler-hochrain-wine` | `reference / —` | `supported` | `high` | `source:rudi-pichler-hochrain-wine` |
| `claim:rudi-pichler-estate` | `reference / 2026-08-18` | `supported` | `high` | `source:rudi-pichler-estate` |
| `claim:smaragd-vinea-category` | `reference / 2026-08-18` | `supported` | `high` | `source:vinea-styles`, `source:rudi-pichler-wines`, `source:vinea-wachau-dac` |

### Sources

- `source:rudi-pichler-estate` — The Rudi Pichler Estate
- `source:rudi-pichler-hochrain-wine` — Riesling Hochrain Smaragd
- `source:rudi-pichler-vineyards` — Geology and Soils
- `source:rudi-pichler-wines` — The Wines
- `source:vinea-hochrain` — Hochrain
- `source:vinea-styles` — Vinea wine styles
- `source:vinea-wachau-dac` — Wachau DAC

</details>

### Open questions

- Confirm current people/leadership beyond Rudi Pichler from first-party material
- Acquire official Ried geometry rather than inferred coordinates
- Deepen the interaction of Vinea trademarks and Wachau DAC labeling without collapsing association categories into government tiers
<!-- END GENERATED CARTA PROVENANCE -->
