# Run 01 STRATA v0.2 Ingestion Audit

**Pilot:** Pyrenean Atlantic  
**Source research date:** 2026-08-18  
**Normalization target:** STRATA v0.2  
**Original uploaded report SHA-256:** `8b0cc935d9901e001ba35b7d7668aa8770729c325c0b9dcfd15e5b3066d14fce`

## Outcome

**PASS — accepted for first CARTA ingestion with explicit normalization.**

The Run 01 packet was not imported mechanically. It was re-read against STRATA v0.2, validated record by record, cross-reference checked, and used to generate the first Human Atlas proof set.

## Packet received

- 36 entity candidates
- 29 relationship candidates
- 25 claim candidates
- 27 source records
- 0 geometry records

## Accepted normalized authority

- 39 entities
- 31 relationships
- 30 claims
- 29 sources
- 7 first-class name assertions
- 8 source-described spatial assertions
- 0 fabricated geometry records

The normalized counts exceed the candidate counts because STRATA v0.2 required explicit country/ecosystem orientation, dedicated naming records, dedicated spatial assertions, and a small number of claims needed to repair evidence linkage.

## Material normalization decisions

### 1. Trade evidence is evaluated by claim fitness

The Garay → Richard Leroy `WORKED_WITH` relationship is accepted as **supported, medium confidence**.

Multiple independent trade sources directly state the work relationship. Under v0.2, the absence of a first-person employment record does not demote fit-for-claim importer/trade evidence by default.

CARTA still does **not** accept:

- `WORKED_FOR`
- `MENTORED_BY`

for Garay → Leroy because the exact arrangement remains unresolved.

### 2. Jurançon grape edges were repaired before ingestion

The candidate relationships:

- Petit Manseng `TRADITIONAL_IN` Jurançon
- Gros Manseng `TRADITIONAL_IN` Jurançon

originally cited `claim:jurancon-terrain-law`, whose statement concerned landscape and legal history rather than the grape relationship itself.

A dedicated `claim:jurancon-manseng-core-grapes` was added from the INAO source before those edges were accepted.

### 3. Consequential names moved into first-class name assertions

Legal grape names are no longer carried only as display aliases.

Accepted name assertions include:

- Petit Manseng → Izkiriota Ttipia in Bizkaiko
- Gros Manseng → Izkiriot Haundi in Bizkaiko
- Petit Courbu → Hondarrabi Zuri Zerratia in Bizkaiko
- Courbu → Gros Courbu in France
- Courbu → Hondarrabi Zuri in Spain

The unresolved Gile / Guillermo Iturriondobeitia crosswalk was **not** accepted as an alias.

### 4. Current Bizkaiko legal status was version-checked

A current EUR-Lex amendment source was added to preserve the 2025 change making Hondarrabi Zuri Zerratia (Petit Courbu) a recommended/main variety.

This prevents older Basque Government pages from silently overriding the newer legal state.

### 5. Spatial knowledge was ingested without fake geometry

No vineyard point, appellation polygon, or parcel geometry was invented.

STRATA v0.2 spatial assertions now preserve:

- Alfredo Egia / Balmaseda locality-level placement
- Garay / Maslacq current-cellar reporting with Orthez conflict retained
- Garay / Saint-Étienne-de-Baïgorry vineyard locality relative to Irouléguy
- Jurançon source-described landscape
- Bizkaiko source-described legal area
- Irouléguy source-described legal area
- the Pyrenean Atlantic analytical area
- Richard Leroy as a geographically distant network anchor

## Deferred / unresolved

The following remain open rather than being narratively repaired:

- exact Garay cellar move chronology;
- Garay parcel geometry relative to Irouléguy;
- Gile / Guillermo identity crosswalk;
- parcel tenure distinctions;
- vintage-specific wine/bottling identity;
- structured availability observations;
- exact hydrology, geology, slope, and official GIS layers.

## Unsupported edges not ingested

- Alfredo Egia `MENTORED_BY` Richard Leroy
- Alfredo Egia `WORKED_WITH` Richard Leroy
- Imanol Garay `MENTORED_BY` Richard Leroy
- Imanol Garay `WORKED_FOR` Richard Leroy
- Petit Manseng parent/offspring relationship with Gros Manseng
- Courbu `MUTATION_OF` Courbu noir
- Virginia `CLIMATE_ANALOGUE_OF` Jurançon

## Validation

The normalized files were checked for:

- JSON Schema compatibility with STRATA v0.2;
- duplicate IDs;
- relationship subject/object existence;
- claim/source cross-reference integrity;
- name assertion entity/jurisdiction/claim integrity;
- spatial assertion entity/anchor/source/claim integrity;
- entity back-reference integrity.

**Result: zero validation or cross-reference errors.**

## Human Atlas proof set

The first ingestion generates readable GitHub pages for:

- Pyrenean Atlantic ecosystem
- Spain and France
- Bizkaia and Béarn
- Jurançon, Bizkaiko Txakolina, Irouléguy, Pacherenc du Vic-Bilh
- Petit Manseng, Gros Manseng, Petit Courbu, Courbu, Raffiat de Moncade
- Alfredo Egia Wine and Imanol Garay
- Alfredo Egia, Imanol Garay, Richard Leroy, Gile Iturriondobeitia
- Hegan Egin
- Rebel Rebel and Ixilune
- navigation indexes

Machine-readable records remain authoritative when a discrepancy appears.
