# Domaine Marcel Lapierre

**Villié-Morgon, Beaujolais, France**

Domaine Marcel Lapierre is a family estate in Villié-Morgon whose current first-party history dates the domaine to 1909. The cellar seed **Morgon** opens a CARTA world around Gamay, Morgon AOP, Villié-Morgon, the Lapierre family, Jules Chauvet, organic farming, and the estate's carefully qualified low-intervention cellar practice.

## Estate and people

The domaine states that Michel Lapierre arrived in Villié-Morgon in 1909 and that Marcel Lapierre was born in 1950. Marcel took over the family business in 1973. The estate records 1981 as the point when, under the guidance of Jules Chauvet, Marcel decided to vinify without added sulfur and moved toward organic cultivation without chemical fertilizers or weedkillers.

Marcel died after the 2010 harvest. Mathieu Lapierre had joined in 2004, Camille Lapierre joined in 2013, and the siblings currently co-own and operate the winery.

CARTA records the Chauvet connection as evidenced influence/guidance.

CARTA also now models the **Gang of Four** as `ecosystem:gang-of-four-beaujolais`: an informal community of practice associated with Marcel Lapierre, Jean Foillard, Guy Breton and Jean-Paul Thévenet, named by Kermit Lynch and historically connected to the adoption of Chauvet-associated methods. It is **not** represented as a formal organization, and its existence does not create automatic bilateral `COLLABORATED_WITH` edges among the four producers.

## Estate, grape, and appellation

The current domaine page describes 18 hectares planted to **Gamay noir à jus blanc**, mainly in Morgon with several plots in Beaujolais.

INAO describes Morgon as a red AOP and one of the ten Beaujolais crus. Its geographic area is limited to the commune of Villié-Morgon around the Py hill, and INAO identifies Gamay as the grape from which Morgon is produced.

CARTA represents:

- Domaine Marcel Lapierre as the producer;
- Domaine Marcel Lapierre Morgon as a persistent wine identity across vintages;
- Morgon AOP as the legal appellation;
- Villié-Morgon as the municipality;
- Gamay noir à jus blanc as the grape.

Persistent identity does not mean non-vintage.

## Farming and cellar

The estate says all plots have been worked according to organic principles since the 1980s and that the vines have been **Ecocert-certified since 2004**.

Its current vinification page describes:

- hand harvest;
- whole bunches moved into vat;
- semi-carbonic maceration;
- indigenous yeasts;
- no acidification, chaptalization, enzymes, or similar additives;
- Morgon finishing fermentation and aging in used barrels;
- no filtration.

The sulfur story requires precision. The estate says it works as far as possible without sulfur, but also states that some batches receive a light sulfur dose, especially for international markets. Bottles marked `N` are bottled without sulfur. CARTA therefore does **not** encode “Lapierre never uses sulfur” as a universal rule.

## Geography and GIS status

CARTA anchors the estate at Villié-Morgon and Morgon within Beaujolais. INAO provides current geographic documentation and mapping resources for the appellation.

No approximate winery coordinate, Côte du Py point, or hand-drawn parcel polygon from Run 03F-A was accepted.

## Run 03F-A corrections

The research report was completed, but several self-audit claims failed reconciliation:

- it said no coordinates appeared while repeatedly supplying approximate coordinates;
- it generalized zero-sulfur practice beyond the producer's own current wording;
- it mixed whole-cluster and destemming descriptions;
- it called the persistent Morgon identity a “non-vintage concept” in the ingestion frontier;
- it overreached from contextual Beaujolais narratives toward unsupported bilateral collaboration edges.

Those claims were narrowed or rejected before ingestion.

The historical significance of the Gang of Four itself is retained separately as a community-of-practice ecosystem.

## Explore next

official Morgon climat geometry · Lapierre parcel holdings by climat · vintage-scoped Morgon élevage details · independent producer profiles for Foillard/Breton/Thévenet · direct bilateral relationship evidence where it exists

## Sources

Primary CARTA sources are Domaine Marcel Lapierre's current estate and viticulture/vinification pages plus INAO's current Morgon AOP record. Kermit Lynch is used as a fit-for-purpose specialist trade source for the historically influential Gang of Four community-of-practice framing.

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:domaine-marcel-lapierre`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `producer:domaine-marcel-lapierre`

**Component entities**

- `producer:domaine-marcel-lapierre`
- `person:marcel-lapierre`
- `person:mathieu-lapierre`
- `person:camille-lapierre`
- `person:jules-chauvet`
- `wine:lapierre-morgon`

**Representative anchors**

- `wine:lapierre-morgon`
- `grape:gamay-noir-a-jus-blanc`
- `appellation:morgon`
- `place:villie-morgon`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:gang-of-four-beaujolais-community` | `reference / —` | `supported` | `high` | `source:kermit-gang-of-four` |
| `claim:lapierre-cellar-current` | `reference / 2026-08-18` | `supported` | `high` | `source:lapierre-vinification` |
| `claim:lapierre-chauvet-guidance` | `reference / —` | `supported` | `high` | `source:lapierre-domaine` |
| `claim:lapierre-current-owners` | `reference / 2026-08-18` | `supported` | `high` | `source:lapierre-domaine` |
| `claim:lapierre-estate-identity` | `reference / 2026-08-18` | `supported` | `high` | `source:lapierre-domaine` |
| `claim:lapierre-morgon-wine` | `reference / —` | `supported` | `high` | `source:lapierre-domaine`, `source:inao-morgon` |
| `claim:lapierre-organic-certification` | `reference / 2026-08-18` | `supported` | `high` | `source:lapierre-vinification` |
| `claim:marcel-lapierre-1950-2010` | `reference / —` | `supported` | `high` | `source:lapierre-domaine` |
| `claim:morgon-aop` | `reference / —` | `supported` | `high` | `source:inao-morgon` |

### Sources

- `source:inao-morgon` — Morgon ou Morgon cru du Beaujolais
- `source:kermit-gang-of-four` — Jean Foillard — Côte du Py / Beaujolais context
- `source:lapierre-domaine` — The Domaine Marcel Lapierre
- `source:lapierre-vinification` — Viticulture and Vinification

</details>

### Open questions

- Acquire authoritative parcel-level geometry and clarify Lapierre holdings by Morgon climat
- Separate current wine-level cellar protocols from estate-wide practice by vintage where useful
- Research Foillard/Breton/Thévenet relationships only from direct evidence rather than 'Gang of Four' shorthand
<!-- END GENERATED CARTA PROVENANCE -->
