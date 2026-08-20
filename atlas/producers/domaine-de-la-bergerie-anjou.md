# Domaine de la Bergerie / Clos de la Bergerie

> **Navigation node:** this honest stub keeps a meaningful CARTA subject discoverable without presenting it as a finished baseline reference.

The machine graph and generated relationships below provide the current orientation. A generous subject-specific enrichment pass is required before baseline promotion.

<!-- BEGIN GENERATED CARTA NAVIGATION -->
## Explore CARTA

This section is generated from governed profile dispositions, editorial anchors, and supported graph relationships. It is not a hand-maintained second knowledge graph.

- [Chenin Blanc](../grapes/chenin-blanc.md) — grape; navigation node
- [Loire Valley](../countries/france/regions/loire-valley.md) — region; navigation node
- [France](../countries/france/README.md) — country; baseline reference
<!-- END GENERATED CARTA NAVIGATION -->

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:domaine-de-la-bergerie-anjou`
- **Maturity / publication:** `node` / `stub`
- **Primary entity:** `producer:domaine-de-la-bergerie-anjou`

**Component entities**

- `producer:domaine-de-la-bergerie-anjou`
- `person:anne-guegniard`
- `person:marie-guegniard`
- `wine:bergerie-clos-de-la-bergerie`
- `vineyard:la-bergerie-champ-sur-layon`

**Representative anchors**

- `place:loire-valley`
- `place:champ-sur-layon`
- `appellation:coteaux-du-layon`
- `grape:chenin-blanc`
- `wine:bergerie-clos-de-la-bergerie`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:bergerie-clos-2022` | `reference / —` | `supported` | `high` | `source:bergerie-clos-2022` |
| `claim:bergerie-family-history` | `reference / —` | `supported` | `high` | `source:bergerie-estate`, `source:bergerie-martines` |
| `claim:bergerie-martines-import` | `reference / 2026-08-19` | `supported` | `medium` | `source:bergerie-martines` |
| `claim:bergerie-organic-27ha` | `reference / 2026-08-19` | `supported` | `high` | `source:bergerie-estate`, `source:bergerie-martines` |
| `claim:bergerie-source-site` | `reference / —` | `supported` | `high` | `source:bergerie-clos-2022` |
| `claim:coteaux-du-layon-law` | `reference / 2026-08-19` | `supported` | `high` | `source:inao-coteaux-du-layon` |

### Sources

- `source:bergerie-clos-2022` — Coteaux du Layon Le Clos de la Bergerie 2022
- `source:bergerie-estate` — Domaine de la Bergerie — estate and family history
- `source:bergerie-martines` — Domaine de la Bergerie
- `source:inao-coteaux-du-layon` — Coteaux du Layon

</details>

### Open questions

- Resolve La Bergerie's exact site type, boundary and cadastral status before any WITHIN_APPELLATION assertion
- Obtain producer or bottle authority for exact 2022 residual sugar, alcohol, sulfur, filtration and fining
- `claim:bergerie-source-site` — Do not infer enclosure, cadastral identity, ownership, exact boundary or WITHIN_APPELLATION status from the word Clos or the source line La Bergerie.
<!-- END GENERATED CARTA PROVENANCE -->
