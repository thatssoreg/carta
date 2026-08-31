# Run 02 Beaujolais Canonical Normalization + Ingestion Audit

**Source research date:** 2026-08-30
**Source filename:** `deep-research-report(5).md`
**Original artifact SHA-256:** `0134c467ed9ef3d8328cd3aaf4f59146b2d4bfb10ede57112968397bd66c3b9d`
**Normalization target:** current CARTA machine authority and deterministic projections

## Outcome

**ACCEPTED — a durable Beaujolais authority foundation is normalized; the finished Beaujolais Atlas world remains a later editorial run.**

The research report was not imported mechanically. Existing IDs were searched first, current legal facts and mutable producer records received targeted verification, and unsupported richness was rejected or deferred.

## Decision register

| Research area | Disposition | Canonical decision |
|---|---|---|
| Beaujolais vs Beaujolais AOC | normalized | `place:beaujolais` remains the wine-region orientation entity; `appellation:beaujolais` remains the legal origin. Their roles are not collapsed. |
| Beaujolais-Villages | corrected / superseded | The August 2026 cahier governs Villages as a mention after Beaujolais. CARTA created `classification:beaujolais-villages-mention`, a legal-name assertion and a mapping to INAO denomination 2487. No `appellation:beaujolais-villages` was created. |
| 85 vs 88 communes | retained + added | The 85 figure remains scoped to Inter Beaujolais’s 2024 key-figure snapshot. The current specification’s 77 Rhône + 11 Saône-et-Loire production-area list is recorded separately as 88. No silent overwrite occurred. |
| 2024 statistics | retained existing | The existing 11,771 claimed hectares, 12-AOC institutional framing, 85 communes, 96/4 grape split and 94/4/2 color split remain dated 2024 measures. |
| Current 2026 law | accepted | Current identity, 88-commune area, 38-commune Villages area, colors, grape rules and primeur/nouveau color scope were accepted from the homologated specification. The 2026 legal hierarchy claim supersedes the old hierarchy claim for current ontology. |
| Ten crus | accepted / completed | Existing Morgon, Fleurie and Moulin-à-Vent IDs were retained. Brouilly, Côte de Brouilly, Chénas, Chiroubles, Juliénas, Régnié and Saint-Amour were added, related to Beaujolais and mapped to the pinned INAO dataset. |
| Gamay | enriched | Existing `grape:gamay-noir-a-jus-blanc` was retained and promoted to a baseline profile. `Gamay N` was added as a current legal name; Pinot × Gouais blanc parentage and current Beaujolais permission were accepted. |
| 1395 event | accepted with rejection | A historical-event entity and historical Duchy of Burgundy context were added. The one-step “banned from Burgundy and moved to Beaujolais” story is explicitly rejected; modern polygons are not used as historical territory. |
| Nouveau | accepted / bounded | Primeur/nouveau is modeled as a legal mention/classification. The 13 November 1951 turn, 1985 third-Thursday rule, mid-1980s peak near 500,000 hl and “never more than half” statement are retained from the current specification. Reputation narratives and a finished Then/Now lens are deferred. |
| Carbonic / semi-carbonic | accepted / normalized | Carbonic, semi-carbonic and whole-cluster practice identities and definitions were added. The current specification’s semi-carbonic-inspired tradition is kept separate from operative law. “All Beaujolais is carbonic” is explicitly rejected. |
| Jules Chauvet | accepted / narrowed | Chauvet is a historical person with a baseline profile. The 1963 research record and direct Lapierre guidance are accepted. “Invented carbonic maceration” is rejected. |
| Gang of Four | retained existing | The ecosystem and four existing membership edges remain informal. No pairwise collaboration edges were inferred. Blanket Chauvet mentorship is explicitly rejected; Foillard receives only a narrower influence edge. |
| Domaine Marcel Lapierre | merged into existing | Existing identity, family history, certification, sulfur caveat, Morgon wine and Chauvet-guidance claims were preserved. A first-party address-derived production-base point and semi-carbonic practice edge were added. No parcel geometry was invented. |
| Jean Foillard | accepted at baseline | A producer identity was separated from the existing person. Villié-Morgon, Morgon/Fleurie activity, Gang membership context and Chauvet influence were accepted. Conflicting acreage/certification scopes remain unresolved and are not averaged. |
| Château Thivin | accepted at baseline | Durable 1877 Geoffray tenure, Odenas/Mont Brouilly base and Côte de Brouilly/Brouilly relationships were accepted. The first-party GPS point is a production base, not estate geometry. |
| Domaine de la Grand’Cour | accepted at baseline | The 1969/1977/1989 chronology, three named Fleurie sites, Brouilly relationship and producer-described carbonic/whole-bunch protocol were accepted. Estate fruit and post-hail purchased-fruit work remain distinct. |
| Domaine des Terres Dorées | accepted with open conflict | Charnay base, southern/cru context and the 2024 operation/development transition to Domaines Roger Zannier were accepted without inferring an asset sale or retirement. The current 57 vs 37 + 18 hectare arithmetic is deliberately unresolved. |
| Métras | deferred | Yvon Métras was not ingested. Merchant-copy propagation, identity/succession ambiguity and insufficient primary evidence would make a canonical profile premature. Yvon and Jules Métras are not merged. |
| Localities | accepted selectively | Existing Villié-Morgon was reused. Fleurie, Odenas and Charnay (Rhône) were added only where they orient accepted producer bases. A full commune gazetteer was not created. |
| Named sites | accepted descriptively | Grand’Cour, Chapelle des Bois and Champagne were accepted from first-party site language and related to Fleurie. Côte du Py was retained. Names do not create polygons. |
| Mont Brouilly / Py hill | accepted descriptively | Physical-feature identities and source-described assertions were added to separate hills from appellations and sites. No standalone hill geometry was authored. |
| Producer bases | accepted at disclosed precision | Lapierre, Thivin, Grand’Cour and Terres Dorées use source-published address points; Foillard uses the official Villié-Morgon municipality point. Every marker says production/base orientation, never vineyard holdings. |
| Appellation geometry | accepted from pinned source | Seven missing cru mappings plus the Villages geographical-complement mapping were added. The existing Beaujolais, Morgon, Fleurie and Moulin-à-Vent mappings were retained. Regulatory areas remain distinct from vineyards. |
| Regional geometry | rejected | No Beaujolais regional polygon was authored. The region continues to use child-geometry-derived orientation only. |
| Terrain | retained / untouched | The merged shared terrain foundation was treated as architecture. No DEM, hillshade, contour, terrain-source or Beaujolais-specific terrain behavior was added. |
| Reference / Frontier split | retained | Durable legal, historical, scientific, first-party producer and spatial facts are Reference. Mutable access, price, availability and market observations were not introduced; no Frontier claim was needed. |

## Existing authority deliberately preserved

- `place:beaujolais`
- `appellation:beaujolais`
- `appellation:morgon`
- `appellation:fleurie`
- `appellation:moulin-a-vent`
- `grape:gamay-noir-a-jus-blanc`
- `grape:chardonnay`
- `producer:domaine-marcel-lapierre` and its person/wine relationships
- `person:jules-chauvet`
- `ecosystem:gang-of-four-beaujolais` and its four informal membership edges
- all official 2024 quantitative measures
- existing INAO Beaujolais/Morgon/Fleurie/Moulin-à-Vent geometry mappings

## Subtractive decisions

The run does not canonize:

- “Beaujolais is granite”
- “all Beaujolais is carbonic”
- a simple 1395 migration story
- “Nouveau ruined Beaujolais”
- “natural wine saved Beaujolais”
- Chauvet as inventor or universal mentor
- organic practice as certification
- an averaged Foillard acreage
- producer appellation as cellar address
- a cuvée/site name as vineyard ownership or geometry
- geology/elevation as flavor causality
- a Yvon/Jules Métras identity merge

## Projection boundary

Human Reference now exposes the legal structure, Gamay, the 1395 event, Nouveau, cellar-method distinctions, Chauvet and the five producer anchors at baseline depth. Atlas native subjects and producer points may expand deterministically from the accepted authority.

The run does not author a Beaujolais hero thesis, five-pillar `regional_world`, Questions Worth Following, Nouveau lens, terrain moments or acceptance-tour UI.
