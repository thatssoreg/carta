# Run 06D — Research Reconciliation + Human Reference Closure Gate

## Scope

This branch reconciles the ChatGPT Web Run 06D handoff covering:

1. Companhia de Vinhos dos Profetas e dos Villões / Listrão dos Profetas / Vinho da Corda dos Profetas
2. Clos du Tue-Boeuf / Le Brin de Chèvre
3. JONATA / Todos

It also records a product-level failure exposed by the prior Run 06 merge: machine authority can be present while the Human Reference remains non-navigable.

Baseline: `c809b73885d79736987ce9763df3940b6942abf8`.

## 06D reconciliation

### Profetas e Villões / Porto Santo

Accepted:

- Companhia de Vinhos dos Profetas e dos Villões is the collaborative project of António Maçanita and Nuno Faria.
- The broader collaboration dates to the beginning of the pandemic / approximately 2020; the handoff's crisp 2021 founding date is not retained as the founding date of the whole project.
- 2022 Listrão dos Profetas is documented by the producer as Listrão from vines older than 80 years on limestone sandy-loam soils, with whole-bunch direct pressing, three press fractions, no SO2 until the end of fermentation, spontaneous fermentation and 11 months on lees in stainless steel and 228 L barrels.
- 2023 Vinho da Corda dos Profetas is documented as Listrão plus Caracol, using the richer final press fraction; the producer records 1,288 numbered bottles for the 2023 vintage.
- The producer explicitly identifies Listrão as Listán Blanco / Palomino Fino. CARTA therefore reuses the existing `grape:palomino-fino` identity and adds Listrão as a local name.
- `vinho da corda` is represented as a practice, not an appellation or separate ontology class.

Corrections / rejections:

- **DOP Madeira and DOP Madeirense are not one legal designation.** Portuguese regulatory material lists separate specifications for Madeira and Madeirense. The Profetas still wines are labeled D.O. Madeirense. The handoff's repeated shorthand treating these as the Madeira D.O. is rejected.
- DOP Madeira is the fortified Madeira category. The still Porto Santo wines in this seed are not modeled as DOP Madeira merely because Porto Santo lies within the Madeira autonomous region.
- The handoff's Caracol/Listán/Cedrés genetic speculation is not promoted. Caracol remains a separate grape node pending a fit primary scientific or official ampelographic source.
- Production numbers are vintage-scoped. The verified producer page records 1,288 bottles for Vinho da Corda 2023, so the handoff's 1,340-bottle figure is not universalized.
- The weak 'first certified Porto Santo wines' claim is withheld.

### Clos du Tue-Boeuf / Le Brin de Chèvre

Accepted:

- Clos du Tue-Boeuf is a Loire estate in Les Montils; Louis/Dressner identifies Thierry and Zoë Puzelat as proprietors, 14 hectares plus purchased fruit, and certified-organic farming.
- Bowler's 2024 Le Brin de Chèvre is Vin de France, 90% Menu Pineau / 10% Petit Meslier, from neighboring parcels planted in 1937 and 1950 with later massale-selection replantings.
- 2024 cellar detail is scoped to that vintage: direct press, spontaneous fermentation without sulfur in large oak, about one year in used demi-muids and Burgundy barrels, no racking, occasional lees stirring, unfined/unfiltered bottling and a minute sulfur addition.
- Menu Pineau / Orbois is treated as one grape identity with a name assertion.
- Vin de France is modeled as a national classification, not as a spatial appellation.

Corrections / rejections:

- The handoff's description of the 1937/1950 Brin de Chèvre vines as **pre-phylloxera** is rejected.
- The handoff's broad declassification chronology is not promoted. Current verified evidence supports the 2024 wine as Vin de France; earlier legal status remains vintage-specific research.
- The handoff's 2022 skin-maceration detail is not ingested in this pass because the strongest verified source surface used here is the current 2024 Bowler record. It remains a follow-up target rather than being generalized.

### JONATA / Todos

Accepted:

- JONATA's first-party history says the estate was established in 1998 when a group acquired the 600-acre property.
- E. Stanley Kroenke became sole owner in 2008.
- Matt Dees was recruited for the first vintage in 2004.
- The estate has 84 planted acres, is in Ballard Canyon AVA within Santa Ynez Valley, and JONATA states that the vineyard became officially certified organic in 2022.
- TTB establishes Ballard Canyon as an AVA on October 2, 2013 and identifies it as nested within Santa Ynez Valley.
- JONATA describes Todos as a persistent annual estate mosaic whose composition varies with vintage.
- 2022 Todos is documented first-party as 70% Syrah, 15% Petite Sirah, 10% Cabernet Sauvignon, 3% Merlot and 2% miscellaneous red and white varieties, with 20 months in 35% new / 65% neutral French oak and 2,545 cases.

Corrections / rejections:

- The handoff's `site purchased in 2000` claim is rejected in favor of JONATA's first-party 1998 history.
- The claim that Kroenke owned JONATA from its founding is rejected; first-party history places sole ownership in 2008.
- Ballard Canyon was **not created in 2001**. TTB gives an establishment date of 2013-10-02.
- **Santa Barbara County is not an AVA.** It can be a county appellation of origin. TTB distinguishes county appellations from American Viticultural Areas.
- The handoff's assumed destemmed / tank-fermentation description is rejected as unsupported. JONATA documents separate vinification of individual vineyard blocks and variable élevage, but the verified sources do not establish that assumed fermentation recipe for Todos.

## Architecture result

No STRATA v0.2 core-ontology failure is exposed by the three research worlds. Existing producer, person, wine, grape, vineyard, place, appellation, classification, practice, claim, relationship and name-assertion constructs can represent the verified authority.

However, the user-facing CARTA product has exposed a separate and concrete failure in the **Human Reference projection**.

## Human Reference navigability failure

The current Human Reference contract says that the machine graph is authority and the Atlas is the reading experience. It also says that when a graph node becomes important enough that CARTA expects a reader to click into it, it should trigger baseline enrichment.

The repository does not currently enforce that contract.

Example already present on `main`:

- `producer:weingut-keller` exists as machine authority.
- `place:germany` exists as machine authority.
- `grape:riesling` exists as machine authority.
- Keller wines exist as machine authority.
- But there is no governed `atlas/producers/weingut-keller.md` profile, no Germany country profile, and no Riesling grape profile.
- Generated producer / country / grape indexes are profile-driven, so those graph nodes remain invisible in the ordinary Atlas browsing experience.

This is not merely missing copy. It is a missing **navigability-closure invariant** between machine authority and the Human Reference.

## Required Human Reference behavior

For a published producer reference, the normal reading path should support links to the relevant Human Reference objects when those objects are represented at a useful level in CARTA. At minimum this usually means:

- country;
- region / appellation where materially relevant;
- primary grapes;
- representative wines and projects where a separate reference surface is warranted;
- documented people, producers, institutions or ecosystems when the target has Human Reference content.

Reciprocal discovery should also work. A Germany or Riesling page should be able to surface the represented producers and wines without hand-maintained duplicate lists drifting from the graph.

## Why a one-off Keller patch is insufficient

The problem predates Keller. Existing published producer profiles already reference country and grape entities that have no corresponding Human Reference surface. Patching Germany and Riesling alone would leave the same failure elsewhere.

The correct repair is a bounded repository-wide Human Reference **navigability closure pass**, not an endless sequence of manual profile exceptions.

## Proposed gate

Do not merge this Run 06D branch into `main` until the Human Reference closure pass decides and implements the navigation contract. The 06D machine authority is source-addressable and ready for validation, but adding more invisible graph nodes to `main` would knowingly deepen the user-facing gap.

## Closure pass acceptance criteria

1. Audit all active producer profiles and important producer machine nodes against Human Reference coverage.
2. Audit country, region/appellation and grape targets needed to make those producer pages navigable.
3. Decide which targets merit `baseline`, which may honestly remain `node` / `stub`, and which should remain machine-only.
4. Add a governed navigation-target mechanism rather than relying on prose alone.
5. Generate or validate links from producer pages to available country, grape, region/appellation and relationship targets.
6. Generate reciprocal discovery surfaces from graph authority where feasible.
7. Add validator rules so a future run cannot silently create a high-value producer node that disappears from the Producer index.
8. Preserve the rule that not every machine entity deserves a standalone page.
9. Evaluate whether Human Reference profile kinds need explicit `project` and/or `vineyard` surfaces. This is a projection question first, not automatically a STRATA core-ontology change.
10. Backfill the repository to the new invariant, including the Run 06 worlds already merged and this Run 06D batch.

`HUMAN REFERENCE NAVIGABILITY CLOSURE REQUIRED BEFORE FURTHER CELLAR AUTHORITY MERGES.`
