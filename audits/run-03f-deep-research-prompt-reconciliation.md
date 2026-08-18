# Run 03F Deep Research Prompt Reconciliation Audit

## Outcome

Run 03F does **not** qualify as a completed six-seed Deep Research deliverable and should not be ingested into CARTA authority.

The prompt itself incorporated the major lessons from Run 03E, especially mechanical checks for cross-dossier contamination, source completeness, numeric contradictions, legal-source provenance, coordinates, vintage generalization, and identity consistency. The execution, however, failed a more basic requirement: completion.

Only the M. Lapierre / Morgon dossier was substantially written. The Rudi Pichler, Phaunus, Domaine de Saint Pierre, Lapostolle, and Muga dossiers were left as explicit placeholders. The registers and audit sections were likewise unfinished. Several claims in the executive summary and partial registers were therefore presented as findings without the required underlying dossiers or source-addressable evidence.

**Disposition:** no Run 03F authority is ingested. Preserve this audit, repair the research protocol, and rerun the unclosed seed work in smaller batches.

## What improved

Run 03F shows that several Run 03E lessons were incorporated into the prompt itself:

- a hard foreign-seed name scan;
- a claim-to-source completeness gate;
- a numeric contradiction scan;
- a legal-language scan;
- a coordinate/geometry gate;
- a vintage-generalization scan;
- an identity-consistency scan;
- explicit language that persistent wine identity across vintages does not mean non-vintage;
- a failed-audit rule that forbids declaring the report clean when defects remain.

The report also did one thing better than Run 03E: it did **not** falsely declare the unfinished mechanical audit clean. It explicitly said the full draft and audit were pending. That is a useful behavioral improvement.

But honesty about incompleteness does not turn an incomplete research deliverable into a successful run.

## Hard-gate failures

### 1. Five of six required dossiers were not completed

Sections 3 through 7 are placeholders:

- Rudi Pichler / Ried Hochrain Wösendorf Riesling Smaragd;
- Phaunus / Loureiro;
- Domaine de Saint Pierre / Château Renard;
- Domaines Bournet-Lapostolle / Le Petit Clos;
- Muga / Prado Enea Gran Reserva.

The final prompt explicitly stated that all six seeds must be researched and that the only acceptable final response was the completed deliverable. That requirement failed.

### 2. Registers were unfinished

The Candidate Relationship Register contains blank URL cells, placeholder ellipses, and an explicit note that remaining relations still need to be added.

The Spatial/GIS Register contains dash placeholders and incomplete sourcing.

The Claim Risk Register contains unresolved placeholder rows and claims that were never developed in a seed dossier.

The Source Ledger covers Lapierre only and explicitly says rows for the remaining seeds still need to be filled.

The claim-to-source hard gate therefore failed by construction.

### 3. The contamination audit was not performed on completed dossiers

The report says the Lapierre dossier was manually checked, then states that the other seed scans will be performed once their drafts exist.

That is not the required final cross-dossier audit. It is a note about future work.

### 4. The mechanical quality gate explicitly reports itself as incomplete

The report states:

> “Pending full draft, count incomplete.”

and:

> “The draft only contains the Lapierre dossier fully; other dossiers are placeholders. Full audit will follow completion of each.”

This is an unambiguous failed final quality gate.

## High-value spot-check corrections

Because the report asserted findings for the unfinished seeds in its executive summary and registers, a small set of targeted source checks was performed to determine whether the mechanical prompt improvements had actually prevented identity and contamination errors. They had not.

### A. M. & C. Lapierre was resolved incorrectly

Run 03F says:

> “M. = Marcel and C. = Camille.”

That is not a safe interpretation of the current producer presentation.

Domaine Marcel Lapierre's current first-party site states that Marcel's children **Mathieu Lapierre** and **Camille Lapierre** currently co-own and operate the family winery. Current trade presentation uses `M. & C. Lapierre` for the domaine under Mathieu and Camille.

First-party source:

https://www.marcel-lapierre.com/en/the-domaine/

Kermit Lynch current producer/wine presentation:

https://shop.kermitlynch.com/product/detail/22FLM10/

**Disposition:** do not ingest a Marcel-and-Camille name assertion. The producer can remain `Domaine Marcel Lapierre`; any consequential current `M. & C. Lapierre` name assertion should be sourced and interpreted in the Mathieu/Camille succession context.

### B. Marcel Lapierre's birth year is wrong

Run 03F gives Marcel Lapierre as born in 1945.

The domaine's current first-party history states that Marcel Lapierre was born in **1950**.

Source:

https://www.marcel-lapierre.com/en/the-domaine/

**Disposition:** reject 1945.

### C. The report invented an existing CARTA Beaujolais cluster

The executive summary says Lapierre creates an organic return to CARTA's “existing Beaujolais cluster.”

Current CARTA authority contains no established Beaujolais/Lapierre/Chauvet cluster. Repository search at the Run 03F starting HEAD returned no matching existing authority for those terms.

**Disposition:** Lapierre would open a new CARTA world, not return to an existing Beaujolais cluster.

### D. Phaunus identity is materially wrong

Run 03F says Phaunus is a Lisbon-based project of **Jorge Moreira**, associated with Quinta do Infantado.

Aphros Wine's current first-party Phaunus Loureiro page identifies:

- producer: **Vasco Croft / Aphros Wine Lda.**;
- oenologues: Tiago Sampaio and Miguel Viseu;
- grape: 100% Loureiro;
- region: northwest Portugal;
- amphora fermentation details for the cited vintage.

Source:

https://aphros-wine.com/en/wines/white/phaunus-loureiro-2023/

Aphros also explicitly presents Phaunus wines within the Aphros portfolio:

https://aphros-wine.com/en/

**Disposition:** reject the Jorge Moreira / Quinta do Infantado identity chain. This is exactly the kind of producer/project resolution the Run 03F prompt was supposed to settle before expansion.

### E. Château Renard was assigned the wrong grape/color

Run 03F's executive summary calls Domaine de Saint Pierre's Château Renard a Jura **Pinot noir** label.

Current market documentation consistently identifies Château Renard as a **white Chardonnay** from Domaine de Saint Pierre / Fabrice Dodane in the Arbois context.

Useful source examples:

https://morenaturalwine.com/products/domaine-de-saint-pierre-chateau-renard-2018

https://www.lacavedespapilles.com/products/chateau-renard

**Disposition:** reject the Pinot noir characterization. The exact producer/person/site/legal model still requires a proper completed dossier before ingestion.

### F. Wösendorf geography was resolved incorrectly

Run 03F says Ried Hochrain is in Wösendorf, “Stratzing municipality.”

Vinea Wachau identifies Hochrain's town as **Wösendorf** and lists Rudi Pichler among the growers. The municipality of Weißenkirchen in der Wachau identifies Wösendorf as one of its wine villages and has a local representative for Wösendorf.

Sources:

https://www.vinea-wachau.at/en/mywachau/vineyards/vineyard-details/myw_vineyard/hochrain

https://www.weissenkirchen-wachau.at/

**Disposition:** reject the Stratzing placement.

### G. Smaragd was overstated as a DAC legal class

The report repeatedly frames Smaragd as a “Wachau DAC dry-white class” and says it is “regulatory.”

Rudi Pichler's first-party site instead describes Steinfeder®, Federspiel® and Smaragd® as quality categories established by the **Vinea Wachau regional protection association** under the Codex Wachau.

Source:

https://www.rudipichler.at/en/the-wines/

Vinea Wachau likewise presents Smaragd as one of its quality categories.

Source:

https://www.vinea-wachau.at/en/mywachau/companies/company-details/myw_company/weingut-rudi-pichler

**Disposition:** the exact relationship among Wachau DAC law, Vinea Wachau membership, protected terms, and Smaragd labeling needs regulatory reconciliation. Do not ingest “Smaragd = Wachau DAC legal class” from Run 03F.

### H. Prado Enea composition was incomplete

Run 03F identifies Prado Enea Gran Reserva as Tempranillo, Graciano, and Mazuelo.

Bodegas Muga's current Prado Enea Gran Reserva 2019 page lists:

- Tempranillo;
- Garnacha tinta;
- Mazuelo.

Source:

https://www.bodegasmuga.com/prado-enea-gran-reserva/

**Disposition:** do not universalize one vintage blend, and do not ingest the Run 03F composition claim.

### I. Rioja Gran Reserva law was oversimplified

Run 03F says Rioja Gran Reserva red is “typically 24m barrel + 36m bottle.”

The current Consejo Regulador classification states a **five-year total minimum**, with at least **two years in 225 L oak barrels** and **two years in bottle**. The remaining year is not universally required to be bottle time.

Source:

https://riojawine.com/es/doca-rioja/denominacion-de-origen-calificada/

**Disposition:** use current Consejo authority and preserve the difference between the legal minimum and Muga's own longer producer practice.

### J. Direct cross-run contamination survived

The Claim Risk Register contains:

> “First single-vineyard Brunello: Clos Apalta”

Clos Apalta is a Chilean seed in this run. Brunello belongs to the prior Caparzo/Montalcino world from Run 03E.

This is not merely an unsupported claim. It is a direct cross-run contamination event, and it survived the new mechanical contamination instructions.

**Disposition:** reject. Future contamination scans must include distinctive terms from recent prior runs, not only the other seeds in the current batch.

## What this run teaches us about the prompt

### The logic improved; the workload exceeded the reliable envelope

Run 03F's prompt was stronger than Run 03E's prompt in its explicit controls. But adding more controls while simultaneously increasing from four seeds to six produced a worse completed artifact.

The model spent substantial output budget on one deep Lapierre dossier and the audit scaffolding, then left five required dossiers unfinished.

The lesson is not that the mechanical gates were wrong. The lesson is that **research depth, seed count, and audit burden have to fit inside one run's completion envelope**.

### Self-audit cannot repair work that was never completed

Run 03E taught CARTA that a prose self-audit could falsely declare contaminated work clean.

Run 03F added mechanical audit instructions, but the model reached the audit before the underlying six dossiers existed. The result was more honest, but still unusable.

### Completion is now a first-class research-quality property

Future research prompts need an explicit completion budget and a smaller batch size.

A mechanically excellent audit of one complete dossier plus five placeholders is inferior to four complete dossiers that can actually be reconciled.

## Protocol change recommended

Do not move on to Wave 05 yet.

Treat Run 03F as a failed research run, not as a partially ingested authority wave.

Rerun the six seeds as **two three-seed research batches**, preserving the same cellar-seed logic:

### Run 03F-A

- M. Lapierre / Morgon
- Rudi Pichler / Ried Hochrain Wösendorf Riesling Smaragd
- Phaunus / Loureiro

### Run 03F-B

- Domaine de Saint Pierre / Château Renard
- Domaines Bournet-Lapostolle / Le Petit Clos
- Muga / Prado Enea Gran Reserva

Each batch should retain the high-value mechanical gates, but remove duplicated explanatory prose and require a compact claim/source ledger rather than a second encyclopedia inside the audit section.

The reconciliation/ingestion pass should happen only after each sub-run returns complete dossiers and passes its own completion gate.

## Next-prompt changes

Carry forward these requirements:

1. **Three seeds maximum for the next repair runs.**
2. **No placeholders, “under construction,” “to be filled,” ellipses, or future-tense completion notes are permitted anywhere in the final answer.**
3. **Before writing the executive summary, verify that all required dossier headings contain substantive research.**
4. **The final audit must count completed dossiers: `required = 3`, `completed = 3`; otherwise the run must continue researching instead of finalizing.**
5. **Extend contamination scans to the immediately preceding research wave, not just the current seed batch.** This catches events like Clos Apalta/Brunello contamination.
6. **For identity-resolution seeds, the canonical identity must be supported by a direct source before any downstream dossier claims are written.**
7. **Use the current producer page first for durable wine identity, but never universalize a vintage-specific composition or cellar protocol.**
8. **Legal/classification terms such as Smaragd and Gran Reserva require explicit separation of association rules, protected-label conventions, and government/appellation law.**
9. **Keep mechanical audit reporting compact.** The audit exists to verify the research, not to consume the space needed to complete it.
10. **If the system approaches output limits, reduce prose depth before dropping a seed. All required seeds must remain complete.**

## Assessment

Run 03F gives a nuanced answer to the prompt-quality question:

- **Yes, the prompt incorporated the major conceptual learnings from Run 03E.**
- **No, the resulting Deep Research run was not better.** It failed the completion contract and still produced several identity, legal/classification, geography, source, and contamination errors.

The next improvement is therefore architectural rather than additive: **smaller research batches, the same strong evidence gates, and a hard completion check before finalization.**

CARTA's reconciliation layer worked before ingestion by refusing to convert this incomplete report into authority. That is the correct outcome.
