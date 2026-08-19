# Hofgut Falkenstein

**Niedermennig, Saar, Mosel, Germany**

Hofgut Falkenstein is a family-scale Riesling estate in Niedermennig in the Saar wine region, within the larger Mosel wine world. Erich Weber and his son Johannes Weber are the core people in the current producer story. For CARTA, Falkenstein is especially useful because its cask-by-cask bottling culture and German quality-test numbering create a real identity problem that must be solved without fragmenting one named wine into separate vintage entities.

## People & estate

First-party and importer material describe Hofgut Falkenstein as the work of **Erich Weber** and **Johannes Weber**. CARTA represents them as people working within the same producer identity and avoids inventing a corporate or mentorship structure beyond the available evidence.

## Saar, Mosel & Niedermennig

The estate is based at **Niedermennig** in the **Saar**. CARTA currently models Saar as a wine-region place within the Mosel wine world rather than pretending it is a separate current appellation.

The seed wine comes from **Niedermenniger Sonnenberg**, which is represented as a vineyard identity. Exact parcel geometry remains a future GIS task.

## Farming

Importer documentation describes the Webers as avoiding herbicides and artificial fertilizers and using cow manure in the vineyards. CARTA records those specific practices rather than promoting the estate to an unsupported organic or biodynamic certification claim.

## In the cellar

Hofgut Falkenstein describes ambient/native yeast fermentation and bottling of many wines cask by cask. Importer material adds the central role of old **1,000-liter fuder** in Riesling fermentation and élevage.

This combination makes individual casks important without automatically making each cask, AP number, or vintage a new wine identity.

## Niedermenniger Sonnenberg Riesling Kabinett trocken

CARTA represents **Hofgut Falkenstein Niedermenniger Sonnenberg Riesling Kabinett trocken** as one durable named wine identity. A documented 2024 example carries the cask name **Munny** and **AP 9**.

Those are vintage/lot-level identifiers that can live in temporal claims. They are not a reason to create `wine:...-2024` or separate AP-number wine entities.

## Kabinett and AP numbers

German Wine Act §20 is important here. It treats **Kabinett** as a Prädikat, requires an official **Amtliche Prüfungsnummer** for Prädikatswein, and provides that Kabinett is awarded only when enrichment has not been performed.

Run 03D incorrectly equated `AP` with a cask number. CARTA explicitly rejects that. The AP number is an official quality-test number. A producer may separately use cask names or numbers, and the two systems must not be conflated.

## Riesling

The seed wine is Riesling, and current Falkenstein evidence strongly supports Riesling as the central grape in this reference. CARTA does not claim the entire estate is literally 100% Riesling without stronger evidence for the whole current portfolio.

## Explore next

Niedermenniger Sonnenberg · Saar/Mosel legal geography · Riesling · Kabinett · cask naming and AP-number chronology

## Sources

Primary CARTA source records include Hofgut Falkenstein, Piedmont Wine Imports, German Wine Act §20, and a documented 2024 Sonnenberg Kabinett trocken trade listing.

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:hofgut-falkenstein`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `producer:hofgut-falkenstein`

**Component entities**

- `producer:hofgut-falkenstein`
- `person:erich-weber`
- `person:johannes-weber`
- `vineyard:niedermenniger-sonnenberg`
- `wine:hofgut-falkenstein-niedermenniger-sonnenberg-riesling-kabinett-trocken`

**Representative anchors**

- `wine:hofgut-falkenstein-niedermenniger-sonnenberg-riesling-kabinett-trocken`
- `grape:riesling`
- `vineyard:niedermenniger-sonnenberg`
- `place:saar`
- `classification:kabinett`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:falkenstein-cellar` | `reference / —` | `supported` | `high` | `source:falkenstein-home`, `source:piedmont-falkenstein` |
| `claim:falkenstein-farming` | `reference / —` | `supported` | `high` | `source:piedmont-falkenstein` |
| `claim:falkenstein-identity` | `reference / —` | `supported` | `high` | `source:falkenstein-home`, `source:piedmont-falkenstein` |
| `claim:falkenstein-sonnenberg-wine` | `reference / —` | `supported` | `high` | `source:kerler-falkenstein-sonnenberg-2024` |

### Sources

- `source:falkenstein-home` — Hofgut Falkenstein
- `source:kerler-falkenstein-sonnenberg-2024` — 2024 Munny #9 Hofgut Falkenstein — Niedermenniger Sonnenberg Kabinett trocken
- `source:piedmont-falkenstein` — Hofgut Falkenstein

</details>

### Open questions

- Acquire Sonnenberg parcel geometry and fuller vineyard-site authority
- Build a durable cask-name/AP-number chronology without fragmenting wines by vintage
- Deepen Saar/Mosel legal-geographic modeling with German regulatory sources
<!-- END GENERATED CARTA PROVENANCE -->
