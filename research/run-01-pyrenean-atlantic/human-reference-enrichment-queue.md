# Run 01 Human Reference Enrichment Queue

**Target:** CARTA Human Reference v0.2 baseline promotion  
**Mode:** contained entity enrichment, not second-ecosystem discovery

## Purpose

Run 01 successfully discovered and normalized a relational ecosystem, but most first-generation Atlas pages do not meet the Human Reference v0.2 baseline.

The next research pass should deepen the **existing reference objects** enough that a serious wine reader can use them as a standalone resource.

New entities may enter only when they materially improve an existing profile, for example a representative wine, benchmark producer, collaborator, vineyard, appellation, or historical figure that is necessary to explain the subject. Do not follow every new node outward into another ecosystem.

## P0 producer promotion

### Alfredo Egia

Target: `profile:alfredo-egia` from `node/stub` to `baseline/published` if evidence permits.

Research gaps:

- biography and trajectory;
- vineyards, site context, tenure and fruit sourcing;
- farming;
- recurring cellar approach versus wine/vintage-specific choices;
- complete-enough grape picture;
- several representative wines;
- Hegan Egin and other meaningful projects/collaborations;
- Garay mentorship and broader documented network;
- relationship to Bizkaiko Txakolina conventions and contemporary Basque wine culture;
- current importer/distributor/access picture where useful.

### Imanol Garay

Target: `profile:imanol-garay` from `node/stub` to `baseline/published` if evidence permits.

Research gaps:

- biography and project chronology;
- Maslacq/Orthez cellar chronology;
- vineyards, tenure and fruit sourcing across France/Spain;
- farming;
- recurring cellar approach;
- grapes;
- several representative wines and projects;
- documented Richard Leroy relationship, without inflating `WORKED_WITH` into unsupported mentorship/employment;
- collaborations and cultural-transmission role;
- current importer/distributor/access picture.

### Richard Leroy

Target: create the missing producer-level machine identity as evidence warrants and build a true `profile:richard-leroy` baseline dossier.

Run 01 only needed Leroy as a professional-network node. That is not acceptable as a Human Reference producer profile.

Research:

- correct person/producer/estate/project identity;
- biography and trajectory;
- place, vineyards and sites;
- farming;
- cellar approach;
- grapes;
- representative wines;
- appellation/declassification context;
- documented work, mentorship, collaboration and influence network;
- historical/contemporary significance;
- current access only as a dated layer.

Do not reduce the dossier to the Garay relationship.

## P0 grape promotion

Target baseline profiles for:

- Petit Manseng
- Gros Manseng
- Petit Courbu
- Courbu
- Raffiat de Moncade

Every grape dossier should cover:

- readable overview;
- origin and significance;
- vineyard behavior;
- structural/sensory range;
- common, historic and emerging styles;
- history as significance rather than chronology;
- where it matters;
- representative producers;
- representative wines;
- names, synonyms and confusion risks;
- genetics with uncertainty preserved;
- current developments.

### Petit Manseng special question

Investigate the user's observation that Petit Manseng is currently having a broader **Virginia wine moment across the state**.

Treat that as a research hypothesis.

Look for:

- current planting/acreage evidence and trend where available;
- geographic spread within Virginia;
- producers making significant dry, sweet, sparkling, skin-contact, oxidative, barrel-aged, amphora or other expressions where actually evidenced;
- how Virginia's current range compares with Jurançon and other French or international expressions;
- why Virginia may be especially interested in the grape from a viticultural and climate perspective;
- which Virginia producers/wines are useful representative anchors;
- whether national wine discourse under-recognizes Virginia relative to the scale or diversity of its Petit Manseng work.

Do not assume the hypothesis is true simply because it is plausible.

## P0 geography promotion

### Countries

- France
- Spain

Do not attempt complete national encyclopedias. Provide enough orientation to make the currently represented regions/appellations intelligible and establish the national wine-law context in which they sit.

### Regions

- Béarn, explicitly historical/cultural versus Béarn AOP
- Bizkaia, as administrative/wine-cultural context

### Appellations

- Jurançon
- Irouléguy
- Pacherenc du Vic-Bilh
- Bizkaiko Txakolina

For each, add landscape, grapes, normal and notable styles, historical significance, major rules that matter, representative producers/wines, internal diversity, and current developments.

### Landscape

- Western Pyrenees

This should become CARTA's first true `landscape` Human Reference profile: physical geography, topography, hydrology, Atlantic/Pyrenean climate relationships, geology where useful, cultural continuity, and cross-border wine geographies.

Keep it distinct from the Pyrenean Atlantic ecosystem, which includes non-geographic professional relationships.

## Representative anchors

Anchors are selective teaching/reference points, not exhaustive lists or rankings.

For producer, grape, region and appellation profiles, identify a useful mix where the evidence supports it:

- historical or foundational;
- benchmark / widely recognized reference;
- contemporary;
- emerging / under-recognized;
- stylistically distinctive.

A producer can also matter as a documented community connector or cultural transmitter. Evidence of mentorship, cellar access, collaboration, introductions, knowledge sharing, scene-building, or other community-generative behavior is relevant when documented. Do not infer it from popularity.

## Human prose standard

Do not write profile openings such as:

- Why this matters in CARTA
- Why I should care
- What CARTA is watching

Write the subject as a real reference object.

Machine IDs and evidence tables belong at the bottom.

## Success gate

Promote a profile to `baseline` only when a reader encountering that subject for the first time would leave oriented about:

- what it is;
- what it is like;
- where it belongs;
- what has made it significant;
- representative people/wines/styles;
- important relationships;
- what is changing now;
- useful next rabbit holes.

If evidence remains too thin, leave the profile honestly at `node` and identify the gap.
