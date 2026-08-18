# STRATA Ontology v0.2

STRATA is CARTA's controlled vocabulary for entities, relationships, naming, geography, and claims. v0.2 incorporates the first Pyrenean Atlantic pilot rather than treating v0.1 as permanent law.

The pilot reinforced one principle above all others: **wine knowledge is relational, but the relationships are not interchangeable.** Geography, law, naming, genetics, mentorship, employment, collaboration, access, stylistic analogy, and cultural continuity can overlap without becoming the same thing.

## Entity families

### People and organizations

- `person`
- `producer`
- `project`
- `institution`

A person is not automatically a producer. A producer is not automatically a legal company. A project may make wine without being a standalone producer entity.

### Ecosystems

- `ecosystem`

An ecosystem is a governed analytical object that connects multiple entity types and relationship systems. It is **not automatically a geographic region**.

The Pyrenean Atlantic pilot earned this type because its explanatory boundary includes several physical/legal geographies plus a non-spatial professional network reaching outside the Pyrenees. Modeling that object as a `place` would be false.

### Biological material

- `grape`

Future revisions may add clones, rootstocks, accessions, or plant-material lots if additional pilots prove they require first-class identity.

### Wine and production

- `wine`
- `practice`

A `wine` entity represents the durable named cuvée or bottling concept across vintages. Vintage-specific differences in composition, source, production, classification, release, or other historically meaningful facts belong in dated claims, relationships, or temporal metadata on that same wine identity. CARTA does not create separate wine entities solely because the vintage changes.

### Geography

- `place`
- `vineyard`
- `appellation`
- `geographic_feature`
- `geology`

These overlap rather than forming a single forced hierarchy. A vineyard may simultaneously intersect a municipality, watershed, appellation, historical territory, geological unit, and mountain system.

`place` may carry a `place_kind` such as:

- `country`
- `administrative_region`
- `cultural_region`
- `historical_territory`
- `municipality`
- `locality`
- `wine_region`
- `analytical_region`

A cultural Basque geography, the Spanish autonomous community, and a cross-border analytical region must not be silently merged because they share a familiar label.

### History and classification

- `classification`
- `historical_event`

### Dynamic discovery

- `market_signal`

Market signals belong to the Frontier layer by default and require dates, confidence, and review logic. Scarcity, current retailer stock, importer pickup, and editorial attention are signals, not permanent measures of importance or quality.

## First-class naming assertions

v0.1 treated names partly as entity data and partly as relationships. The pilot showed that this is insufficient.

A name can be true only in a particular jurisdiction, language, legal regime, or time period without requiring CARTA to create a second biological entity.

Example:

- Bizkaiko law can pair `Hondarrabi Zuri Zerratia` with Petit Courbu.
- That legal-name fact does not require CARTA to create a duplicate grape entity merely so it can draw `SYNONYM_OF`.

Use `name-assertion.schema.json` for evidence-bound names with jurisdiction, time, status, and claim support.

`alternate_names` on an entity remains useful as lightweight display metadata, but **legal, contested, historical, or otherwise consequential naming claims should be represented through first-class name assertions**.

## Relationship families

Relationship predicates are uppercase snake case. Direction matters unless explicitly documented as symmetric.

### Identity, naming, and genetics

- `SYNONYM_OF`
- `LEGAL_ALIAS_OF`
- `HISTORIC_NAME_OF`
- `LOCAL_NAME_OF`
- `HISTORICALLY_CONFUSED_WITH`
- `PARENT_OF`
- `OFFSPRING_OF`
- `PROPOSED_PARENT_OF`
- `MUTATION_OF`
- `CLONE_OF`
- `GENETICALLY_CLOSE_TO`
- `CROSSED_WITH`

Name predicates should connect entities only when both objects genuinely warrant entity identity. Use name assertions when the object is fundamentally a name attached to an entity rather than a second entity.

Genetic claims must not be inferred from naming similarity or geographic proximity.

### Plant material and viticulture

- `HISTORICALLY_COPLANTED_WITH`
- `TRADITIONAL_IN`
- `PLANTED_AT`
- `PROPAGATED_FROM`
- `GRAFTED_FROM`
- `PERMITTED_IN`
- `RECOMMENDED_IN`
- `PROHIBITED_IN`
- `USED_BY`

### People, work, and cultural transmission

- `MENTORED_BY`
- `TRAINED_AT`
- `WORKED_FOR`
- `WORKED_WITH`
- `COLLABORATED_WITH`
- `FAMILY_OF`
- `FOUNDED`
- `SUCCEEDED_BY`
- `MEMBER_OF`
- `INFLUENCED_BY`

`WORKED_WITH`, `WORKED_FOR`, `MENTORED_BY`, and `INFLUENCED_BY` are deliberately different. A strong importer or specialist profile may substantively support these relationships when it clearly states them. First-person documentation is valuable but not a universal admission gate.

`INFLUENCED_BY` remains especially high-risk because stylistic resemblance, proximity, importer overlap, or fandom cannot establish transmission by themselves.

### Ownership and commerce

- `OWNED_BY`
- `ACQUIRED_BY`
- `IMPORTED_BY`
- `DISTRIBUTED_BY`
- `BUYS_FRUIT_FROM`
- `SOLD_TO`

Parcel tenure remains an open question. The pilot showed that owned vines, rented/farmed vines, and purchased fruit can coexist and should not be collapsed.

### Production and wine

- `MADE_BY`
- `FARMED_BY`
- `FERMENTED_BY`
- `BOTTLED_BY`
- `MADE_FROM`
- `USES_PRACTICE`
- `AGED_IN`

These exist so CARTA can distinguish grower, fermenter, bottler, label, and producer roles when they differ.

### Geography and containment

- `LOCATED_IN`
- `FARMS_IN`
- `FARMS_PARCEL`
- `CELLAR_IN`
- `WITHIN_APPELLATION`
- `WITHIN`
- `OVERLAPS`
- `ADJACENT_TO`
- `UPSTREAM_OF`
- `DOWNSTREAM_OF`
- `WITHIN_WATERSHED`
- `ON_SLOPE_OF`
- `SHARES_GEOLOGY_WITH`
- `CROSSED_BY_BORDER`
- `FORMERLY_WITHIN_TERRITORY`

Spatial intersection may be calculated by GIS, but a calculated intersection is not automatically a cultural, historical, legal, or causal relationship.

### Law, classification, and history

- `CREATED_BY`
- `REVISED_BY`
- `SUPERSEDED_BY`
- `CLASSIFIED_AS`
- `DECLASSIFIED_FROM`
- `BOUNDARY_CHANGED_BY`
- `RENAMED_AS`
- `LEGAL_AT_TIME`
- `OWNED_AT_TIME`
- `LOCATED_WITHIN_AT_TIME`

### Comparison and interpretation

- `STYLISTIC_NEIGHBOR_OF`
- `STRUCTURAL_ANALOGUE_OF`
- `CLIMATE_ANALOGUE_OF`
- `SITE_ANALOGUE_OF`

These are analytical edges, not identity or lineage. They require an explicit comparison basis and should usually live outside CARTA core in an external analytical layer, or enter Reference only as carefully governed, evidence-backed claims.

## Spatial knowledge in v0.2

CARTA now distinguishes **geometry** from **spatial assertion**.

### Geometry

Use `geometry.schema.json` when actual geometry exists: a point, line, polygon, parcel, official boundary, or other mappable object with source and precision.

### Spatial assertions

Use `spatial-assertion.schema.json` when useful geographic knowledge exists but exact geometry does not.

Supported representation kinds include:

- `reference_location` — a reliable locality or address-level placement without pretending it is a vineyard point;
- `source_described_area` — an authoritative or credible textual description of an area whose geometry has not yet been acquired;
- `cultural_area` — a sourced cultural geography;
- `historical_area` — a sourced historical geography;
- `analytical_area` — an explicitly analytical construct;
- `network_anchor` — a spatial anchor used to show where a non-spatial relationship touches the map.

This allows CARTA to represent "Garay's vines are reported in Saint-Étienne-de-Baïgorry, just outside the Irouléguy boundary" without inventing parcel coordinates.

A spatial assertion can later point to one or more actual geometry records when better data is acquired.

## Prohibited inference rules

The graph must not create a lineage edge solely because two entities:

- are geographically close;
- share an importer or distributor;
- appear in the same retailer or restaurant;
- use the same grape;
- taste similar;
- are discussed together in trade media;
- share an appellation;
- are popular in the same subculture.

CARTA should be capable of recording a tempting-but-unsupported edge as rejected evidence rather than silently deleting the question.

## Pilot-earned changes adopted in v0.2

The Pyrenean Atlantic pilot earned the following changes:

1. **Source fitness is claim-specific.** Source class is descriptive, not a trust caste.
2. **Jurisdictional name assertions are first-class.** Legal naming should not create duplicate biological entities.
3. **Places have semantic kinds.** Country, municipality, cultural region, historical territory, wine region, and analytical region are not interchangeable.
4. **Source-described spatial knowledge is first-class.** Useful geography does not require fabricated geometry.
5. **Ecosystems are first-class analytical objects.** An ecosystem may connect multiple geographies plus non-spatial networks.
6. **The human-readable Atlas is a required projection.** Machine authority must remain inspectable by humans in GitHub.

## Open ontology questions after Run 01

The next ingestion and future pilots should continue testing whether STRATA needs first-class treatment for:

- clone or accession;
- vineyard parcel distinct from vineyard;
- lease/tenure relationships;
- importer portfolio as an entity;
- climate zone or mesoclimate;
- sensory structure as a governed concept;
- availability observation versus market signal.

Do not add these merely because they are imaginable. Let repeated evidence earn the complexity.
