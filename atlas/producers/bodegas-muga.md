# Bodegas Muga / Prado Enea Gran Reserva

**Barrio de la Estación, Haro, Rioja Alta, Spain**

Bodegas Muga is a family winery founded in 1932 by **Isaac Muga** and **Aurora Caño**. The cellar seed **Prado Enea Gran Reserva** returns CARTA organically to the existing Rioja world while opening a Muga-specific branch around Barrio de la Estación, Gran Reserva law, in-house cooperage, and vintage-scoped Prado Enea sourcing.

## Producer and place

Muga's first-party history and the Consejo Regulador place the winery in **Barrio de la Estación, Haro**, within Rioja Alta.

CARTA treats Barrio de la Estación first as a real place and historically meaningful winery district. It does not infer bilateral collaboration among its bodegas merely from proximity.

## Prado Enea

Prado Enea Gran Reserva is modeled as one durable Muga wine identity across vintages.

For **2019**, Muga currently states:

- grapes: Tempranillo, Garnacha Tinta and Mazuelo;
- source context: high-elevation parcels in northwest Rioja Alta around Sajazarra, Cellorigo and Fonzaleche;
- fermentation in oak vats;
- at least 36 months in oak;
- fresh-egg-white clarification before bottling;
- at least 36 months of bottle aging.

Those are 2019-specific facts unless broader evidence supports continuity.

Run 03F-B's proposed 65% Haro / 35% leased-old-vine source formula was not supported by the current first-party page and was not ingested.

## Gran Reserva law

The current DOCa Rioja rule for red **Gran Reserva** requires **five years total aging**, including at least **two years in 225-litre oak** and **two years in bottle**. The remaining year can be allocated flexibly.

Muga's 2019 Prado Enea practice therefore exceeds the current legal minimum. CARTA keeps producer practice and legal minimum as separate claims.

## Mazuelo / Carignan

The Consejo Regulador lists **Mazuelo** with the synonyms Carignan, Cariñena, Mazuela and Samsó. CARTA therefore reuses the existing `grape:carignan` entity and records `Mazuelo` as a Rioja-scoped name rather than creating a duplicate biological grape.

## Corrections to Run 03F-B

The report incorrectly claimed that López de Heredia also has a wine named **Prado Enea**. That name collision is false and was rejected.

The report also carried older/importer aging numbers alongside current Muga practice without enough temporal proof. CARTA uses the current first-party 2019 record rather than averaging those figures.

## GIS status

Muga is anchored to Barrio de la Estación in Haro. The 2019 wine is source-described through Sajazarra, Cellorigo and Fonzaleche, but no parcel polygons or guessed coordinates were added.

## Explore next

Prado Enea sourcing by vintage · parcel geometry · historical release chronology · Barrio de la Estación as a historical producer cluster · Muga family succession

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:bodegas-muga`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `producer:bodegas-muga`

**Component entities**

- `producer:bodegas-muga`
- `person:isaac-muga-martinez`
- `person:aurora-cano`
- `wine:muga-prado-enea-gran-reserva`
- `classification:rioja-gran-reserva`

**Representative anchors**

- `wine:muga-prado-enea-gran-reserva`
- `appellation:rioja`
- `place:haro`
- `place:barrio-de-la-estacion`
- `classification:rioja-gran-reserva`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:mazuelo-carignan-rioja` | `reference / —` | `supported` | `high` | `source:rioja-mazuelo` |
| `claim:muga-identity` | `reference / —` | `supported` | `high` | `source:muga-family`, `source:rioja-muga` |
| `claim:prado-enea-2019-cellar` | `reference / —` | `supported` | `high` | `source:muga-prado-enea-2019` |
| `claim:prado-enea-2019-composition` | `reference / —` | `supported` | `high` | `source:muga-prado-enea-2019` |
| `claim:prado-enea-wine-identity` | `reference / 2026-08-18` | `supported` | `high` | `source:muga-prado-enea-2019` |
| `claim:rioja-gran-reserva-current` | `reference / 2026-08-18` | `supported` | `high` | `source:rioja-classification` |

### Sources

- `source:muga-family` — Muga Family
- `source:muga-prado-enea-2019` — Prado Enea Gran Reserva 2019
- `source:rioja-classification` — Clasificación de vinos DOCa Rioja
- `source:rioja-mazuelo` — Mazuelo
- `source:rioja-muga` — Bodegas Muga

</details>

### Open questions

- Extend Prado Enea vineyard sourcing and blend history vintage by vintage
- Acquire authoritative parcel geometry for relevant Sajazarra, Cellorigo and Fonzaleche sources
- Research Barrio de la Estación as a historical producer cluster without inventing bilateral relationships
<!-- END GENERATED CARTA PROVENANCE -->
