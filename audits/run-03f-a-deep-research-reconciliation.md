# Run 03F-A Deep Research Repair Reconciliation Audit

## Outcome

Run 03F-A is **materially better than the failed six-seed Run 03F** because it completed all three requested dossiers and correctly repaired several major identity errors.

It is also the first repair run in this sequence that was complete enough for CARTA's reconciliation layer to recover and ingest all three cellar worlds.

However, the report's claim that all mechanical audits passed is false. The self-audit still failed to detect direct violations of the prompt's own hard gates.

**Disposition:** reconcile independently against source-addressable evidence, ingest only the supported core, reject/narrow the failed claims, and do not treat the report's mechanical self-certification as trustworthy.

## What improved

Run 03F-A successfully corrected several failures from Run 03F:

- Phaunus was correctly reassigned to Aphros / Vasco Croft rather than Jorge Moreira / Quinta do Infantado.
- Wösendorf was correctly separated from the prior erroneous Stratzing placement.
- all three dossiers were completed rather than left as placeholders;
- Marcel Lapierre's 1950 birth year was recovered from the producer's current first-party history;
- Smaragd was at least recognized as distinct from a vineyard or appellation name;
- the report distinguished Aphros the producer from Phaunus the wine line.

Those are meaningful gains.

## Mechanical audit failures

### 1. The coordinate audit is demonstrably false

The report says:

> “No coordinates are given in the report.”

But the report itself supplies multiple approximate coordinates, including:

- Villié-Morgon around `46.1631 N, 4.6814 E`;
- Côte du Py around `45.80 N, 4.65 E`;
- Hochrain / Wösendorf around `48.4 N, 15.47 E`;
- Ponte de Lima around `41.92 N, 8.52 W`.

Some are explicitly sourced to Wikipedia or simply labeled approximate.

This violates the Run 03F-A coordinate hard gate.

**Disposition:** no coordinates from Run 03F-A were ingested. CARTA stores source-described locality/region assertions only.

### 2. The URL-completeness audit is false

The report says all relationship, spatial, and risk-register URL cells are filled.

They are not.

The Candidate Relationship Register contains many blank direct-source cells and entries such as `Assumed (no direct cite)`. The Identity Resolution Register likewise contains source labels such as `Domaine site` rather than complete direct URLs.

**Disposition:** CARTA rebuilt the admitted claims against complete first-party, regulatory and institutional URLs.

### 3. The legal-source gate still failed

The report states legal Wachau rules using Decanter as its cited basis and then says this is acceptable because Decanter reports the rule.

The prompt explicitly required governing authority for legal assertions.

The Austrian federal `DAC-Verordnung "Wachau"` is publicly available from the Bundeskanzleramt RIS system and directly governs Riedenwein.

**Disposition:** Wachau legal claims were rebuilt from RIS ÿ4. Vinea Wachau is retained for institutional interpretation and its own trademark/categories.

### 4. Smaragd was still modeled incorrectly

Run 03F-A calls the current 12.5% versus older 13% descriptions “contested.”

Current Vinea Wachau authority states that Smaragd has at least 12.5% alcohol and explicitly identifies Steinfeder®, Federspiel® and Smaragd® as registered Vinea trademarks restricted to member wineries.

An older secondary source does not make the current Vinea definition contested.

More importantly, Smaragd is not a DAC tier. Vinea Wachau itself says the post-2020 DAC origin system **supplements** the established Vinea brands.

**Disposition:** `classification:smaragd` is modeled as a Vinea Wachau category/trademark distinct from `appellation:wachau-dac`.

### 5. Pichler vineyard size was confused with estate holdings

The report notices a supposed contradiction between the producer's 15 hectares and a larger Hochrain figure, but the categories are different.

Rudi Pichler's estate says it cultivates 15 hectares.

Vinea Wachau says the **entire Hochrain Ried** is 27.46 hectares and lists multiple growers, including Rudi Pichler.

Ried area is not Pichler-owned area.

**Disposition:** store 15 ha as the current estate figure and 27.46 ha as the total climat/Ried figure. Do not infer Pichler's parcel size.

### 6. Phaunus cellar duration was internally contradictory

The executive summary describes roughly three months in amphora.

The dossier also gives three months.

Elsewhere it discusses different time frames.

Aphros's first-party technical pages show that this is ventage-sensitive:

- 2022: six months sur lies;
- 2023: seven months sur lies.

**Disposition:** the 2023 seven-month statement is stored as a ventage-scoped claim. No universal amphora-aging duration is ingested.

### 7. Phaunus sulfur was overgeneralized

Run 03F-A repeatedly describes Phaunus as bottled with no added sulfur.

The current first-party 2023 technical page reports 30 mg/L total sulfur. Aphros's general cellar philosophy also explicitly states that sulfur use is low but not universally zero.

**Disposition:** reject the universal no-sulfur claim.

### 8. Phaunus legal geography was overclaimed

The report repeatedly states that Phaunus Loureiro is Vinho Verde DOC / Lima.

The current first-party Phaunus Loureiro pages instead state `Northwest of Portugal`.

Other Aphros bottlings explicitly state `Vinho Verde DOC – Sub-Region of Lima`, but that information cannot be silently transferred between wines.

**Disposition:** Aphros is anchored to Lima Valley from first-party estate history. Phaunus Loureiro's precise legal designation remains provisional pending explicit producer/label evidence.

### 9. Lapierre sulfur practice was universalized

Run 03F-A says Lapierre “never uses SO2” and elsewhere says no added sulfites.

The producer's current vinification page is more precise: the domaine works as far as possible without sulfur, some batches receive a light dose (especially for export), and bottles marked `N` are bottled without sulfur.

**Disposition:** ingest the scoped current practice, reject a universal no-sulfur rule.

### 10. Persistent identity was again mislabeled

The Recommended Ingestion Frontier calls Lapierre Morgon a:

> “non-vintage concept.”

That directly violates the prompt's durable-wine rule.

**Disposition:** one durable `wine:lapierre-morgon` entity across vintages. It is not declared non-vintage.

## Reconciled authority admitted

### Domaine Marcel Lapierre

Accepted:

- 1909 estate history;
- 18 current hectares, mainly Morgon;
- Gamay noir à jus blanc;
- Marcel Lapierre born 1950 and taking over in 1973;
- Jules Chauvet's documented 1981 guidance;
- Mathieu and Camille as current co-owners/operators;
- Ecocert certification since 2004;
- current semi-carbonic, indigenous-yeast, used-barrel, unfiltered practice with sulfur properly scoped;
- Morgon AOP / Villié-Morgon / Gamay legal-geographic context.

Withheld/rejected:

- invented coordinates;
- universal zero-sulfur language;
- “non-vintage” characterization;
- formalized Gang-of-Four collaboration network;
- unsupported wine-level numeric protocol where current estate pages do not carry it.

### Weigut Rudi Pichler

Accepted:

- Wösendorf estate identity;
- family viticulture there since 1731;
- current 15-hectare estate and grape mix;
- durable Riesling Hochrain Smaragd identity;
- Ried Hochrain as Wösendorf, terraced, southeast-facing, 27.46 ha total and 215-380 m;
- loess site description;
- Smaragd as Vinea category/trademark at current >=12.5% ABV;
- Wachau DAC Riedenwein law from Austrian federal authority.

Withheld/rejected:

- approximate coordinates;
- 53-acre figure as a Pichler estate holding;
- “Smaragd is contested 12.5 vs 13” framing;
- unsupported/current-person claims;
- cellar specifics not directly established by the strongest recovered wine-level sources.

### Aphros / Phaunus

Accepted:

- Aphros / Vasco Croft producer identity;
- modern project development from 2004 in Lima Valley;
- Phaunus as an Aphros line/project;
- durable Phaunus Loureiro identity;
- 100% Loureiro;
- first-party 2023 amphora/skin fermentation and seven-month sur-lies aging;
- producer-described biodynamic practice;
- regional Aphros relationship to Lima Valley.

Withheld/rejected:

- universal zero-sulfur claim;
- universal three-month amphora claim;
- approximate coordinates;
- automatic Phaunus Loureiro → Vinho Verde DOC / Lima appellation edge;
- certification claims not required for the baseline.

## Prompt assessment

The smaller three-seed batch fixed the **completion problem**.

It did not fix the **self-audit reliability problem**.

That tells us something important: adding more prose instructions is now producing diminishing returns. The next research run should retain the three-seed ceiling, but the ingest/reconciliation layer should remain the real validator. Deep Research should be asked to surface evidence and uncertainty, not to certify that it has mechanically complied with tests it demonstrably does not execute reliably.

For Run 03F-B, keep the batch at three seeds. Simplify the self-audit section, require direct URLs and explicit unresolved fields, and let the repository-aware reconciliation pass perform the true hard validation.

## Assessment

**Run 03F-A is a successful research repair only after reconciliation.**

The raw report is not clean enough to trust directly, but it is complete enough and source-rich enough that CARTA can recover trustworthy authority from all three worlds without another rerun.

That is progress from Run 03F: completion is fixed, core identities are much better, and the remaining errors are now mostly reconciliation-class errors rather than missing-work failures.
