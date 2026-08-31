# François Blanchard / Le Grand Cléré

> **Navigation node:** this honest stub keeps a meaningful CARTA subject discoverable without presenting it as a finished baseline reference.

The machine graph and generated relationships below provide the current orientation. A generous subject-specific enrichment pass is required before baseline promotion.

<!-- BEGIN GENERATED CARTA NAVIGATION -->
## Explore CARTA

This section is generated from governed profile dispositions, editorial anchors, and supported graph relationships. It is not a hand-maintained second knowledge graph.

- [Loire Valley](../countries/france/regions/loire-valley.md) — region; deep reference
- [Vin de France](../classifications/vin-de-france.md) — classification; navigation node
- [France](../countries/france/README.md) — country; baseline reference
- [Touraine](../countries/france/regions/touraine.md) — region; baseline reference
- [Vouvray AOP](../countries/france/appellations/vouvray.md) — appellation; baseline reference

### Deliberately deferred anchors

- **Sauvignon** — machine authority only; no reader-facing target
<!-- END GENERATED CARTA NAVIGATION -->

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:le-grand-clere`
- **Maturity / publication:** `node` / `stub`
- **Primary entity:** `producer:le-grand-clere`

**Component entities**

- `producer:le-grand-clere`
- `person:francois-blanchard`
- `wine:a-table-blanchard`
- `vineyard:le-grand-clere`

**Representative anchors**

- `place:loire-valley`
- `place:lemere`
- `grape:sauvignon`
- `classification:vin-de-france`
- `wine:a-table-blanchard`
- `vineyard:le-grand-clere`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:a-table-2022-cellar` | `reference / —` | `supported` | `medium` | `source:blanchard-nichifutsu-2024`, `source:blanchard-vins-sains` |
| `claim:a-table-2022-identity` | `reference / —` | `supported` | `high` | `source:blanchard-nichifutsu-2024`, `source:blanchard-vins-sains`, `source:franceagrimer-vsig` |
| `claim:blanchard-ecocert-control-09` | `reference / —` | `supported` | `medium` | `source:blanchard-first-party-09`, `source:blanchard-vins-sains` |
| `claim:blanchard-farming` | `reference / 2026-08-19` | `supported` | `medium` | `source:blanchard-vins-sains` |
| `claim:blanchard-grand-clere-site` | `reference / —` | `supported` | `high` | `source:blanchard-vins-sains` |
| `claim:blanchard-producer-identity` | `reference / —` | `supported` | `high` | `source:blanchard-vins-sains`, `source:blanchard-nichifutsu-2024` |

### Sources

- `source:blanchard-first-party-09` — Le Grand-Cléré
- `source:blanchard-nichifutsu-2024` — August 2024 wine catalog — Domaine Grand Cléré / A Table !
- `source:blanchard-vins-sains` — François Blanchard — Boisson Vivante — Loire
- `source:franceagrimer-vsig` — Les Vins Sans Indication Géographique (VSIG)

</details>

### Open questions

- Reconcile the producer's preferred canonical public label over time
- Verify Ecocert certificate scope and dates from certificate-level evidence
- Do not assign Touraine appellation containment without official parcel evidence
- `claim:blanchard-ecocert-control-09` — Certificate number and exact certification dates remain open.
- `claim:blanchard-farming` — Seek the Ecocert certificate or certificate directory before assigning certification dates or scope beyond the association member declaration.
- `claim:blanchard-producer-identity` — Le Grand Cléré is retained as the canonical producer display name while Domaine Grand Cléré and Boisson Vivante remain sourced trade/name forms rather than separate producers.
<!-- END GENERATED CARTA PROVENANCE -->
