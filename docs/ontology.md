# STRATA Ontology v0.1

STRATA is CARTA's initial controlled vocabulary for entities and relationships. It is deliberately explicit because a useful wine knowledge graph must distinguish relationships that casual wine discourse often collapses.

## Entity families

### People and organizations

- `person`
- `producer`
- `project`
- `institution`

A person is not automatically a producer. A producer is not automatically a legal company. A project may make wine without being a standalone producer entity.

### Biological material

- `grape`

Future schema revisions may add clones, rootstocks, accessions, or plant-material lots if the pilot proves they require first-class identity.

### Wine and production

- `wine`
- `practice`

A wine can represent a named cuvée or bottling concept. Vintage-specific manifestations should be added only when the distinction materially matters.

### Geography

- `place`
- `vineyard`
- `appellation`
- `geographic_feature`
- `geology`

These overlap rather than forming a single forced hierarchy. A vineyard may simultaneously intersect a municipality, watershed, appellation, historical territory, geological unit, and mountain system.

### History and classification

- `classification`
- `historical_event`

### Dynamic discovery

- `market_signal`

Market signals belong to the Frontier layer by default and require dates, confidence, and expiry/review logic.

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

`INFLUENCED_BY` is high-risk and requires stronger evidence than stylistic similarity, proximity, importer overlap, or fandom.

### Ownership and commerce

- `OWNED_BY`
- `ACQUIRED_BY`
- `IMPORTed_BY`
- `DISTRIBUTED_BY`
- `BUYS_FRUIT_FROM`
- `SOLD_TO`

Canonical spelling for import relationship is `IMPORTED_BY`; capitalization errors should fail validation.

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

Spatial intersection may be calculated by GIS, but a calculated intersection is not automatically a cultural, historical, or legal relationship.

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

These are analytical edges, not identity or lineage. They require an explicit comparison basis and should usually live in Lens or carefully governed Reference claims.

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

## Open ontology questions for the pilot

The Pyrenean Atlantic pilot should specifically test whether STRATA needs first-class types for:

- clone or accession;
- vineyard parcel distinct from vineyard;
- historical territory distinct from place;
- vintage bottling distinct from wine/cuvée;
- importer portfolio as an entity;
- climate zone or mesoclimate;
- sensory structure as a governed concept;
- availability observation versus market signal.

Do not add these preemptively. Let the pilot earn the complexity.
