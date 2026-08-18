# CARTA Evidence Policy v0.2

CARTA is allowed to be expansive. It is not allowed to become casually certain.

## Core rule

Every material assertion must be one of four things:

1. **Supported** — evidence is sufficient for the current claim and scope.
2. **Provisional** — plausible and sourced, but evidence is incomplete, indirect, or materially imprecise.
3. **Contested** — credible sources disagree or the underlying record is unresolved.
4. **Rejected** — a tempting assertion has been investigated and should not be repeated as fact.

Unknown is not false. Missing evidence is not evidence of absence.

## Source fitness, not source prestige

CARTA does **not** use a universal source hierarchy in which a source class is automatically strong or weak for every claim.

The governing question is:

> **How fit is this source to carry this particular claim?**

Wine knowledge is often documented through importers, distributors, retailers, technical sheets, specialist reporting, producer interviews, appellation bodies, grape catalogues, government records, and community observation. Different sources are authoritative for different jobs.

Examples:

- Plantgrape or a peer-reviewed genetics paper is an excellent fit for grape identity and genetics.
- INAO or an official appellation specification is an excellent fit for current French appellation law.
- A long-standing importer or distributor may be an excellent or good fit for producer work history, cellar practice, fruit sourcing, vineyard tenure, cuvée composition, production scale, or collaboration when the information is specific, attributable, and consistent with the relationship they actually hold.
- A retailer technical sheet may be a good fit for a vintage-specific wine composition or cellar description, especially when it reproduces producer/importer technical information.
- A retailer listing is an excellent fit for a dated observation that the retailer listed a wine at a given price or quantity; it is not evidence of broad market availability.
- A forum, Reddit post, Instagram post, or community discussion may be a good fit for a dated discourse or discovery signal and a weak fit for grape genetics, legal status, ownership, or historical first/only claims.

A source class therefore describes **what the source is**, not how much CARTA trusts every statement it contains.

## Source roles

A source may support, contradict, or contextualize a claim. One source can play more than one role across different claims.

Recommended source classes:

- `primary_regulatory` — laws, appellation regulations, government registers, official filings.
- `primary_producer` — producer, estate, project, or person speaking for themselves.
- `primary_scientific` — peer-reviewed research, official grape catalogues, genetic databases, university research.
- `primary_institutional` — official institutional records or publications.
- `independent_reporting` — reported journalism, books, specialist publications.
- `trade_source` — importer, distributor, retailer, restaurant, auction, market-facing source.
- `community_source` — forum, social-media, Reddit, tasting-group, or community discussion.
- `secondary_reference` — encyclopedic or compiled reference work.

Personal observations, holdings, taste preferences, acquisition history, private watchlists, and owner-specific hypotheses belong in an external/private Lens system rather than CARTA core source records. An external Lens may reference stable CARTA IDs without becoming evidence in CARTA authority.

## Claim-level fitness

Each source reference attached to a claim may record its fitness for that claim:

- `excellent` — directly appropriate to the claim, specific, and within the source's authority or firsthand access.
- `good` — materially useful and credible for the claim, though not the strongest conceivable source.
- `limited` — relevant but indirect, incomplete, old, imprecise, or dependent on another unverified source.
- `lead_only` — useful for discovery or triangulation but not sufficient to carry the claim by itself.

Fitness is assessed at the **claim-source pair**, not assigned permanently to the source.

A trade source may therefore be `excellent` for a dated importer relationship and `lead_only` for a genetic pedigree.

## Corroboration

Corroboration is valuable, but CARTA does not demand first-person evidence for every producer claim.

One source can be enough when:

- it is highly fit to the claim;
- it is specific rather than promotional boilerplate;
- no credible source contradicts it;
- and the wording stays within the source's actual scope.

Multiple independent sources increase confidence when they add genuinely independent evidence. Repetition of the same importer copy across five retailer pages is not five independent confirmations.

For producer-world facts, ask whether the source is likely to have direct working access to the information. A specialist importer who visits a grower and publishes a detailed technical profile may be more useful for cellar and vineyard facts than a generic lifestyle interview.

## Confidence

Use a four-level scale:

- `high`
- `medium`
- `low`
- `unknown`

Confidence belongs to a claim, not to an entity or source class as a whole.

Confidence should consider:

- source fitness;
- specificity;
- corroboration;
- independence of corroborating sources;
- recency when the fact can change;
- scope precision;
- and credible contradictions.

## High-risk claim categories

Require especially careful sourcing and narrow wording for:

- first, oldest, only, invented, revived, discovered;
- parentage and genetic identity;
- ownership and succession;
- legal status and appellation permissions;
- exact vineyard boundaries;
- mentorship, apprenticeship, or influence;
- farming certifications and chemical-input claims;
- causal claims linking site, grape, farming, or cellar choices to sensory outcomes.

High-risk does **not** mean "primary source required." It means the evidence must be fit to the claim, the wording must match the evidence, and uncertainty must remain visible.

For mentorship/work history specifically, CARTA should distinguish `WORKED_WITH`, `WORKED_FOR`, `TRAINED_AT`, `MENTORED_BY`, and `INFLUENCED_BY`. A credible importer or specialist profile can support one of these when it states the relationship clearly. CARTA should not automatically downgrade a well-attested `WORKED_WITH` relationship merely because a formal employment record is unavailable.

## Trade-source discipline

Importer, distributor, and retailer sources are normal and legitimate wine evidence when used appropriately.

They can substantively support claims about:

- producer biography and work history;
- vineyard and fruit sourcing;
- cellar location;
- farming and cellar practice;
- cuvée composition;
- vessel and élevage;
- collaboration;
- importer representation;
- distribution and market access;
- production or allocation details when clearly stated and dated.

They should be treated more cautiously for:

- genetics and biological identity;
- appellation law;
- legal ownership;
- historical first/only claims;
- certification status outside the source's stated scope;
- broad causal claims.

When a trade source is the best publicly available source, CARTA should use it transparently rather than manufacture a permanent `provisional` penalty for the absence of a source class that may never exist online.

## Temporal discipline

Every time-sensitive claim should include `observed_at` and, where applicable, `valid_from` / `valid_to`.

A retailer listing proves that a listing existed when observed. It does not prove broad market availability.

A producer portfolio proves representation at the relevant time. It does not prove current stock.

A current appellation rule does not establish the historical rule.

A current cellar location does not erase an earlier cellar location.

## Claims versus hypotheses

Personal and production-development questions are valuable, but they belong outside CARTA core in an external/private Lens until tested.

Example:

> Petit Manseng may offer a useful Virginia model for retaining both acidity and textural mass under warm-season conditions.

That can be a private Lens hypothesis. It should not become a universal Reference claim without evidence defining site, vintage, ripeness, farming, and winemaking scope. If later research earns a Reference claim, the accepted claim must be supported independently of the private Lens record.

## Contradiction handling

Never average incompatible claims into a synthetic fact.

Instead:

- preserve each claim;
- attach its source;
- record claim-level source fitness;
- mark the conflict;
- state what evidence would resolve it;
- assign current confidence separately.

## Geography and provenance

CARTA applies the same source-fitness rule to geography.

Official GIS is preferred for legal boundaries when available, but useful spatial knowledge is not limited to official polygons. CARTA may preserve reliable locality references, approximate/source-described areas, cultural/historical geographies, and analytical ecosystem geographies as long as the representation type and precision are explicit and no false coordinate or boundary precision is invented.

## Discovery and semantic saturation

Research agents may follow evidence-backed relationships beyond a seed list. They should stop expanding when new nodes are predominantly peripheral, weakly evidenced, or duplicative rather than materially improving understanding of the ecosystem.

Fame, proximity, importer overlap, stylistic similarity, or social-media visibility alone are not sufficient reasons to create lineage or influence edges.
