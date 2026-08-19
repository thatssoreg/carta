# Run 08A–C — Source-Adjudicated Research Staging

## Scope

This branch reconciles three external research handoffs against CARTA's live STRATA v0.2 authority and Run 07 Human Reference contract:

1. Run 08A — A.J. Adam / Anika / COS
2. Run 08B — Maçanita / Wasenhaus / Caves du Château d'Auvernier
3. Run 08C — Domaine de la Tournelle / Pax / Casa Coste Piane

Baseline: `main @ ee49ef64465ce5fe022cf9c6715257dca86e853d` (`Merge Run 07 Human Reference navigability closure`).

Run 08D is still outstanding. This is therefore a **staging branch**, not a final activation or Human Reference publication pass.

## Staging posture

New subjects that appear suitable for eventual Reference authority are authored as `provisional` rather than immediately `active`.

That is deliberate. Run 07 requires every active producer, country and grape to have its own explicit Human Reference disposition. Activating these worlds before the fourth parallel handoff is reconciled would either force premature projection work or recreate a partial-batch workflow.

Accordingly this branch:

- records source-addressable, adjudicated candidate authority;
- reuses current CARTA entities where they already exist;
- preserves contradictions and unresolved claims;
- does not add Human Reference profiles yet;
- does not regenerate Atlas indexes yet;
- does not change STRATA schemas;
- must not be treated as merge-ready final authority until Run 08D and the activation/projection gate are complete.

## Run 08A adjudication

### A.J. Adam / Dhroner Hofberg

Accepted:

- The Hofberg seed resolves to **Dhroner Hofberg**.
- A.J. Adam's modern estate history begins with the 2000 vintage.
- Current VDP authority identifies Andreas Adam and Barbara Gudelj as owners/cellar masters.
- Current VDP authority gives **6.40 ha**, correcting the handoff's preference for approximately five hectares as the best current figure.
- Dhroner Hofberg is represented as a vineyard; VDP identifies it as `VDP.GROSSE LAGE`.
- Existing CARTA `place:germany`, `place:mosel`, `grape:riesling` and `classification:kabinett` are reused.

Withheld / narrowed:

- Kabinett is not equated with sensory sweetness. The persistent wine identity can carry vintage-specific sweetness and technical facts later.
- Mentorship claims are not staged merely because an interview describes formative figures. They remain available for a later dedicated people/lineage pass if exact wording supports the stronger relationship.
- No duplicate Germany, Mosel, Riesling or Kabinett node is created.

### Anika / Sandhi

Accepted:

- Sandhi Vintners is the producer context for the Anika wines.
- Existing `person:rajat-parr` is reused; Sashi Moorman is staged as a new person.
- The Enz Vineyard Mourvèdre and Coteaux de Clair Grenache are represented as separate wine/site subjects.
- Enz Vineyard's 1922 Mourvèdre parcel and organic/non-irrigated farming are retained from fit trade authority.
- Coteaux de Clair is associated with **Santa Ynez Valley**, not Sta. Rita Hills. The seed's Sta. Rita Hills transcription is rejected.
- Existing `appellation:santa-ynez-valley-ava` is reused.

Withheld / narrowed:

- No `project:anika` is created. The evidence establishes a label/cuvée family, but current STRATA has no label-under predicate that would preserve that exact semantic distinction without distortion. The wines can remain inside Sandhi's composite producer world.
- The exact 2018 Grenache legal appellation remains provisional pending direct label or producer technical authority.
- No Grenache biological relationship is authored yet because this pass did not complete a fit primary ampelographic reconciliation between the seed's Grenache usage and CARTA's existing `grape:garnacha-tinta` identity.
- Sandhi is not asserted to own, lease or farm Enz or Coteaux de Clair.

### COS

Accepted:

- COS was founded in Vittoria in 1980 by Giambattista Cilia, Giusto Occhipinti and Cirino Strano; the name is formed from their surname initials.
- COS's producer world is staged in Sicily/Vittoria and linked into existing Italy authority.
- Producer material supports biodynamic **principles/practices** and extensive terracotta-vessel work.

Withheld / narrowed:

- The user's seed string `Vittoria Rosso` is only provisionally mapped to **Pithos Rosso** until the exact bottle/vintage is confirmed.
- No timeless Pithos Rosso grape composition is authored. The handoff reports a current producer 100% Nero d'Avola description against older 60/40 Nero d'Avola/Frappato trade descriptions. Vintage evolution is plausible but not proven here.
- Terracotta is not normalized as Georgian qvevri method.
- No Gravner→COS mentorship or influence edge is authored.

## Run 08B adjudication

### Maçanita Branco Reserva

Accepted:

- Maçanita Vinhos is a distinct Douro project associated with António and Joana Maçanita. Existing `person:antonio-macanita` and `place:portugal` are reused.
- Branco Reserva remains one persistent wine identity with vintage-scoped composition.
- Producer authority supports 2021 at 55% Folgasão plus 45% traditional Douro varieties.
- Producer authority supports 2023 as an undifferentiated 100% blend of traditional Douro varieties.
- Producer authority supports the 2023 direct-press / cold-settling / 40% stainless + 60% barrel / bâtonnage / 18-month protocol.
- Douro and Douro DOC are staged as new geographic/legal subjects.

Rejected / withheld:

- Retailer copy that assigns the **plain Maçanita Branco** Viosinho/Gouveio/Códega do Larinho, altitude and schist description to Branco Reserva is explicitly rejected for the Reserva.
- The reported 2010-vs-2011 founding discrepancy is not forced into a false single date.
- Old-vine ages from Os Canivéis are not transferred to Branco Reserva.

### Wasenhaus

Accepted:

- Wasenhaus is the Baden project of Christoph Wolber and Alexander Götze.
- Götze's first-person account supports a 2016 first trial vintage; trade history supports 2018 as the first-release/formal-establishment milestone. These are retained as separate chronology points rather than treated as a contradiction.
- The base `Spätburgunder` is a persistent estate-level Pinot Noir distinct from Vulkan, Kalk and named parcel bottlings.
- Current CARTA `grape:pinot-noir` and `place:germany` are reused.
- Plantgrape supports **Blauer Spätburgunder** as a German alternative name for Pinot noir; a governed name assertion is staged.
- Baden, Markgräflerland, Staufen im Breisgau and Badischer Landwein are staged.
- German Landwein law and importer context support the importance of law-driven naming constraints.

Modeling decision:

- `Badischer Landwein` is staged as an **appellation** because it is a protected geographic origin / Landweingebiet, rather than as a generic quality classification detached from place.

Withheld / narrowed:

- Burgundy employment histories are not converted into mentorship claims.
- No single whole-cluster percentage or soil-source roster is universalized across vintages.
- Organic/biodynamic practice is retained at the level the source supports; no certification is invented.

### Caves du Château d'Auvernier / Œil de Perdrix

Accepted:

- This world introduces **Switzerland** as a new CARTA country candidate.
- Château d'Auvernier is staged with Auvernier, Canton of Neuchâtel and Neuchâtel AOC.
- The current Sélection Tradition L'Œil de Perdrix is Pinot Noir with a short cuvaison, generally about one night.
- Estate continuity to 1603 is retained as producer history.

Important legal correction:

- The handoff proposed separate pseudo-classifications such as `classification:oeil-de-perdrix-neuchatel-aoc` and a Valais counterpart. CARTA does **not** stage those.
- Primary Neuchâtel law shows that Œil de Perdrix is regulated **within the Neuchâtel AOC framework**. The current cantonal system recognizes Neuchâtel as the AOC and permits geographic origin mentions such as Auvernier under specified conditions.
- The legal term is therefore carried as a jurisdiction-scoped claim inside `appellation:neuchatel-aoc`, not promoted into a duplicate shared appellation or synthetic classification family.
- Valais remains useful contextual evidence but is not expanded in this seed-only staging pass.

## Run 08C adjudication

### Domaine de la Tournelle / Fleur de Savagnin

Accepted:

- Domaine de la Tournelle is a distinct Jura producer founded by Évelyne and Pascal Clairet in 1991.
- Tournelle's Fleur de Savagnin is a distinct persistent wine from **Domaine Labet Fleur de Savagnin** despite the identical cuvée string.
- The wine is 100% Savagnin from grey marl and explicitly **ouillé / non-oxidative** in producer material.
- Existing `grape:savagnin`, `practice:ouillage`, `place:jura` and `appellation:arbois` are reused.
- Arbois municipality is staged separately from the existing legal `appellation:arbois`.

Contradiction preserved:

- The producer's French page says at least 24 months of topped élevage while the English page says at least 18 months. CARTA does not select one silently.
- The safe shared lower bound is at least 18 months, while the precise producer-language conflict remains contested.

Rejected / withheld:

- Claims that Fleur de Savagnin is sous voile are rejected against the producer's explicit topping/non-oxidative description.
- No named vineyard, parcel or geometry is fabricated.
- Arbois classification remains provisional at the persistent-wine level because some market records differ by vintage; final activation should verify label/classification scope.
- No direct Tournelle↔Labet relationship is created merely because they share region, grape, marl and a wine name.

### Pax / North Coast Syrah

Accepted:

- Pax Wines currently identifies Pax and Pamela Mahle as sole owners.
- The PAX brand history dates to 2000 in first-party material.
- The producer library establishes the persistent **Syrah, North Coast** identity for 2017–2022.
- Existing `grape:syrah`, `place:california` and `place:united-states` are reused.
- North Coast AVA is staged from current eCFR authority.
- Pax's general organic/sustainable sourcing and ambient-fermentation language is retained without synthesizing blanket vineyard certification.

Correction / restraint:

- The external handoff extended the wine through 2023 from trade material. The producer's current library exposes 2017–2022 but does not list a 2023 North Coast Syrah. CARTA therefore stages the first-party-confirmed 2017–2022 range and does **not** infer discontinuation from the 2023 absence.
- Wind Gap, old Pax Wine Cellars and Donelan succession are not encoded until their legal/project boundaries are independently reconciled.

### Casa Coste Piane / Frizzante…Naturalmente

Accepted:

- Casa Coste Piane is staged as a producer in Santo Stefano di Valdobbiadene, Veneto.
- The exact seed is staged as Valdobbiadene Prosecco DOCG `Frizzante…Naturalmente`.
- Producer material supports Glera, soft pressing, white vinification, winter clarification and spontaneous spring bottle refermentation.
- Current producer analysis gives 11% ABV, 1 g/L residual sugar and 48 mg/L total SO2.
- Current farming claims support no herbicide, predominantly manual work and low-impact plant-protection treatments without asserting organic certification.
- Glera and Conegliano Valdobbiadene–Prosecco DOCG are staged as new subjects.

Terminology guardrail:

- `Frizzante`, bottle refermentation, `col fondo`, ancestral method, pét-nat, traditional method and `sui lieviti` are not collapsed into one practice or synonym set.
- `sui lieviti` is not applied to this exact Frizzante merely because the broader DOCG system regulates bottle-refermented wines.
- `Naturalmente` remains wine/label wording, not a practice entity.

Withheld:

- The handoff's trade-supported 95% Glera + 5% unidentified grapes is not staged as composition. The first-party producer page supports Glera but does not require CARTA to guess the remaining trade-reported fraction.
- No sulfur-free or organic-certified claim is authored.

## Existing authority reused

This staging pass deliberately reuses existing CARTA subjects including:

- `person:antonio-macanita`
- `person:rajat-parr`
- `place:portugal`
- `place:germany`
- `place:mosel`
- `place:italy`
- `place:france`
- `place:jura`
- `place:california`
- `place:united-states`
- `appellation:arbois`
- `appellation:santa-ynez-valley-ava`
- `grape:riesling`
- `grape:pinot-noir`
- `grape:savagnin`
- `grape:syrah`
- `classification:kabinett`
- `practice:ouillage`

No duplicate node is created simply to make a research handoff self-contained.

## Human Reference activation gate

Run 07's navigability invariant remains binding.

After Run 08D arrives, the final reconciliation pass must:

1. reconcile Run 08D against the then-current `main` and this staged authority;
2. run a collision check for newly created subjects and names;
3. decide which staged entities become `active`, remain `provisional`, or are rejected/deprecated;
4. give every newly activated **producer**, **country** and **grape** its own explicit Human Reference disposition;
5. create honest stubs where reader navigation is useful without pretending baseline depth;
6. add reciprocal anchors to existing Riesling, Pinot Noir, Savagnin, Syrah, Germany, Portugal, Italy, France and United States worlds where authority supports them;
7. create at minimum a Switzerland country surface if `place:switzerland` is activated;
8. run `python scripts/validate_data.py --write-human-reference`;
9. run `python scripts/validate_data.py` and all relevant repository validation;
10. inspect generated indexes and `Explore CARTA` navigation before any merge.

The current branch intentionally stops before those steps.

## Architecture result

The nine research worlds stress:

- label/cuvée identity nested under a producer;
- same-named wines made by different producers;
- persistent wines with vintage-changing grape composition and site sourcing;
- law-driven informal vineyard naming;
- cantonal wine-law terminology;
- bottle-refermented Frizzante terminology;
- new-country expansion;
- legal appellation vs physical geography;
- biological grape identity vs jurisdictional naming.

All accepted facts can be represented by existing STRATA v0.2 entities, dated claims, relationships, name assertions and Human Reference projection rules.

`NO CONCRETE STRATA v0.2 REPRESENTATION FAILURE FOUND.`

## Merge status

`RUN 08A–C SOURCE-ADJUDICATED STAGING COMPLETE.`

`RUN 08D + FINAL ACTIVATION / HUMAN REFERENCE PROJECTION REQUIRED BEFORE MERGE AS CANONICAL AUTHORITY.`
