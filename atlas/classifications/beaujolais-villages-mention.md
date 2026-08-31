# Beaujolais Villages mention

**A governed mention inside Beaujolais, not a second CARTA appellation**

The Beaujolais specification homologated in August 2026 states that **Villages** may follow the name Beaujolais. It also lists 38 communes whose grapes may qualify for the mention.

CARTA therefore represents `Beaujolais Villages` as a legal-name assertion on a classification/mention identity. It deliberately does not create `appellation:beaujolais-villages`.

## Why it still has geometry

INAO publishes a distinct geographical-complement source feature for Beaujolais Villages. CARTA governs that feature under the mention identity, preserving a useful legal map surface without changing the ontology.

The polygon is a cartographic representation of the qualifying regulatory area. It is not a vineyard map, quality tier or sensory zone.

## Dated counts

The current legal area lists 38 communes. The official 2024 regional snapshot reported 85 wine-growing communes and counted Beaujolais-Villages within a 12-AOC institutional presentation. Those dated figures are retained as exactly that; they do not override the 2026 specification’s identity model.

<!-- BEGIN GENERATED CARTA NAVIGATION -->
## Explore CARTA

This section is generated from governed profile dispositions, editorial anchors, and supported graph relationships. It is not a hand-maintained second knowledge graph.

- [Beaujolais](../countries/france/regions/beaujolais.md) — region; baseline reference
- [Chardonnay](../grapes/chardonnay.md) — grape; navigation node
- [France](../countries/france/README.md) — country; baseline reference
- [Gamay noir à jus blanc](../grapes/gamay-noir-a-jus-blanc.md) — grape; baseline reference
<!-- END GENERATED CARTA NAVIGATION -->

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:beaujolais-villages-mention`
- **Maturity / publication:** `baseline` / `published`
- **Primary entity:** `classification:beaujolais-villages-mention`

**Component entities**

- `classification:beaujolais-villages-mention`

**Representative anchors**

- `appellation:beaujolais`
- `place:beaujolais`
- `grape:gamay-noir-a-jus-blanc`
- `grape:chardonnay`

<details>
<summary>Machine claims and sources</summary>

### Material claims

| Claim | Layer / observed | Status | Confidence | Sources |
|---|---|---|---|---|
| `claim:beaujolais-current-legal-structure-15` | `reference / 2026-08-20` | `supported` | `high` | `source:beaujolais-cahier-2026`, `source:legifrance-beaujolais-2026` |
| `claim:beaujolais-villages-38-communes-15` | `reference / 2026-08-20` | `supported` | `high` | `source:beaujolais-cahier-2026`, `source:inao-beaujolais-villages` |

### Sources

- `source:beaujolais-cahier-2026` — Cahier des charges de l’appellation d’origine contrôlée Beaujolais
- `source:inao-aires-geographiques-siqo-2026-08-24` — Délimitation des aires-géographiques des SIQO — 2026-08-24 snapshot
- `source:inao-beaujolais-villages` — Beaujolais Villages rouge
- `source:legifrance-beaujolais-2026` — Arrêté du 5 août 2026 homologuant le cahier des charges de l’appellation d’origine contrôlée Beaujolais

</details>

### Open questions

- Keep consumer-facing institutional shorthand distinct from the current cahier’s identity model
<!-- END GENERATED CARTA PROVENANCE -->
