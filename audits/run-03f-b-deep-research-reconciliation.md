# Run 03F-B Deep Research Repair Reconciliation Audit

## Outcome

Run 03F-B is a **successful research substrate, not trustworthy authority by itself**.

The three-seed ceiling again worked: all three dossiers were completed and each seed produced enough useful evidence for CARTA to recover a baseline Human Reference world.

The report still failed at source precision and still contained substantive factual/identity errors. CARTA therefore reconciled the report against direct first-party, regulatory, institutional and fit-for-purpose trade sources before ingestion.

**Disposition:** ingest the supported core for Domaine de Saint Pierre / Château Renard, Clos Apalta / Le Petit Clos, and Muga / Prado Enea; reject or temporalize the overreaches; separately formalize the Gang of Four as the Beaujolais community-of-practice ecosystem requested after Run 03F-A.

## What improved

Compared with the failed six-seed Run 03F:

- all three dossiers are complete;
- the identity-first framing largely worked;
- Château Renard is correctly treated as a white Jura wine rather than Pinot Noir;
- Le Petit Clos is kept distinct from Clos Apalta;
- the Apalta legal question was researched instead of dismissed as mere marketing;
- Muga returns to existing Rioja structure without manufacturing a Muga ↔ López de Heredia collaboration edge;
- vintage variability is acknowledged more consistently.

The three-seed batch remains the right working envelope.

## What still failed

### 1. The direct-URL contract still did not actually pass

The report says its claims are anchored, but many register cells contain internal citation anchors instead of direct URLs, and the Source Ledger often gives generic domain or homepage URLs such as retailer roots rather than the actual claim-bearing page.

The research can therefore be useful while its own source-addressability audit is still false.

**Disposition:** CARTA attached clean claim-bearing URLs independently.

### 2. Château Renard was still overgeneralized as permanently 100% Chardonnay

Run 03F-B says Château Renard is always 100% Chardonnay.

The 2018 Beaune Imports record supports Chardonnay for that vintage. A 2020 iDealwine record describes Chardonnay with a small proportion of Savagnin.

That does not prove a permanent formula.

**Disposition:** one durable `wine:chateau-renard` identity; 2018 and 2020 composition are temporalized. No timeless `100% Chardonnay` claim.

### 3. Saint Pierre chronology and sulfur language remain unstable

Trade/reference sources disagree between 2011 and 2012 for Fabrice Dodane's acquisition/takeover. Sources also vary on the exact organic-certification chronology and on zero-versus-minimal sulfur wording.

Ecocert currently confirms organic certification.

**Disposition:** accept current certified-organic status; preserve the acquisition year as imprecise; do not universalize zero-sulfur cellar practice.

### 4. The Clos Apalta corporate chronology in the report contains unsupported noise

Run 03F-B includes multiple sale, reacquisition and rebranding dates around the Marnier-Lapostolle business that were not necessary to understand the seed and were not securely carried by the recovered first-party sources.

Clos Apalta's own history clearly supports Alexandra Marnier Lapostolle's 1994 Chile venture and Charles-Henri de Bournet Marnier Lapostolle's leadership since 2013.

**Disposition:** ingest the supported family/project chronology and leave unsupported corporate-sale claims out.

### 5. Apalta needs legal precision

The report's phrase `Apalta DO` points toward something real but can invite a false equivalence with European appellation structures.

Chile's Decree 56, published 25 May 2018, adds **Apalta as an Area within Valle de Colchagua**, defined by the rural locality of Apalta in the commune of Santa Cruz. Current Le Petit Clos pages use `Appellation Apalta`, and the Spanish 2022 page explicitly says `D.O. Apalta`.

**Disposition:** model `appellation:apalta` for legal-origin semantics, with a summary preserving its actual Chilean zoning status.

### 6. Le Petit Clos blend must remain vintage-specific

First-party pages show material blend changes:

- 2020: 40% Carmenère, 38% Cabernet Sauvignon, 19% Merlot, 3% Petit Verdot;
- 2021: 68% Carmenère, 16% Cabernet Sauvignon, 15% Merlot, 1% Cabernet Franc;
- 2022: 59% Carmenère, 33% Cabernet Sauvignon, 5% Merlot, 3% Cabernet Franc.

**Disposition:** durable wine identity; vintage-scoped blend claims and relationships.

### 7. Prado Enea was falsely confused with López de Heredia

Run 03F-B says that López de Heredia also has a wine named `Prado Enea`.

That is a direct identity error. CARTA's existing López de Heredia seed is Viña Gravonia, and the report provides no evidence for a López de Heredia Prado Enea.

**Disposition:** reject the name-collision claim. `Prado Enea Gran Reserva` is modeled here as a Muga wine.

### 8. Muga vineyard sourcing was over-specified

Run 03F-B proposes a 65% Haro / 35% leased-old-vine sourcing formula.

Muga's current first-party 2019 page instead identifies parcels in northwest Rioja Alta around Sajazarra, Cellorigo and Fonzaleche.

**Disposition:** use the current vintage-specific first-party sourcing context; do not ingest the 65/35 formula.

### 9. Producer practice and Rioja law are now cleanly separated

For Prado Enea 2019, Muga states at least 36 months in oak and 36 months in bottle.

Current DOCa Rioja Gran Reserva law requires five years total, with at least two years in 225 L oak and two years in bottle.

These are not contradictory. One is a producer's longer practice; the other is the legal floor.

**Disposition:** separate claims and a dedicated `classification:rioja-gran-reserva`.

### 10. Mazuelo should not create a duplicate grape

Rioja's official grape reference gives `Mazuelo` the synonyms Carignan, Cariñena, Mazuela and Samsó.

**Disposition:** reuse existing `grape:carignan` and add a Rioja-scoped `Mazuelo` name assertion.

## Gang of Four clarification

After Run 03F-A, the project explicitly clarified that the **Gang of Four matters as a historically consequential community of practice** even though it was not a formal organization.

CARTA now represents:

- `ecosystem:gang-of-four-beaujolais`
- Marcel Lapierre
- Jean Foillard
- Guy Breton
- Jean-Paul Thévenet
- Jules Chauvet as the central practice-transmission context

Kermit Lynch's account explicitly names the four, says he coined the nickname, and credits their adoption of Chauvet's methods with a dramatic change in Beaujolais wine quality and increased attention to the region.

The ecosystem does **not** imply automatic bilateral collaboration, mentorship or friendship edges among all members.

## Protocol assessment

Run 03F-B confirms the current protocol direction:

1. **Three seeds is the right batch size.**
2. Deep Research should prioritize complete, source-rich dossiers rather than spending large output budgets on self-audit ceremony.
3. Direct URLs still need independent verification in reconciliation.
4. Identity, legal structure, vintage scope and geography remain repository-gated.
5. Communities of practice should be preserved when historically explanatory, without forcing them into formal-organization semantics.

The next research wave can continue with the three-seed envelope and a compact integrity section. CARTA's repository-aware reconciliation remains the actual admission gate.
