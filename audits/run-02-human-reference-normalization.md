# Run 02 Human Reference normalization audit

**Run:** Pyrenean Atlantic Human Reference enrichment  
**Input artifact SHA-256:** `eb1e429648bbe6c3ce7fe3942d9328cbfb0b82c0239d58e741e7696c0b781ab6`  
**Disposition:** accepted as research corpus; machine appendix not ingested directly

## Outcome

Run 02 provided enough research to close the Human Reference enrichment gate, but its proposed machine packet and promotion matrix required substantial editorial normalization.

CARTA accepted the research as a source of leads and synthesis, then rebuilt machine records against the live STRATA/Human Reference v0.2 schemas.

## Profiles promoted to baseline/published

- Alfredo Egia
- Imanol Garay
- Richard Leroy
- Petit Manseng
- Gros Manseng
- Petit Courbu
- Courbu
- France
- Spain
- Béarn
- Bizkaia
- Jurançon
- Irouléguy
- Pacherenc du Vic-Bilh
- Bizkaiko Txakolina

The existing Pyrenean Atlantic ecosystem remains baseline/published.

## Profiles not promoted

### Raffiat de Moncade — node/stub

The run supplied substantially more prose than the evidence could safely support. Strong genetics and network placement remain useful, but the current sensory, viticultural, producer, legal-use, and acreage picture is too thin for a generous baseline.

### Western Pyrenees — node/queued

The landscape clearly belongs in CARTA, but Run 02 mixed western/eastern Pyrenean geography, simplified watersheds/geology, and proposed an approximate rectangular polygon. Promotion now requires a real GIS acquisition and synthesis pass.

## Important adjudications

### Producer identity and lineage

- Added a first-class `producer:richard-leroy` and composed it with the existing person record.
- Kept Imanol Garay → Richard Leroy as `WORKED_WITH`.
- Did **not** promote that edge to `WORKED_FOR` or `MENTORED_BY`.
- Did not create a direct Alfredo Egia → Richard Leroy mentorship/work edge.

### Richard Leroy

Run 02 contained multiple unsupported or contradictory biographical/cuvée claims. CARTA normalized Richard Leroy around the durable evidence:

- tiny Anjou/Rablay-sur-Layon domaine
- roughly 2.7 ha of Chenin
- Les Noëls de Montbenault
- Les Rouliers
- organic/biodynamic farming
- indigenous fermentation and barrel élevage
- historically evolving sulfur practice
- modern Vin de France context

Unverified Chardonnay and additional-cuvée claims were not accepted.

### Alfredo Egia

CARTA rejected the Run 02 claim that Egia's work should generally be described as Vin de France because the Txakoli regulator rejected his style. The profile remains grounded in the better-supported Bizkaia/Bizkaiko context.

Sulfur and cellar practice are recorded as wine/vintage-specific rather than a universal zero-sulfur producer rule.

### Imanol Garay

The accepted profile uses current trade documentation for:

- Maslacq cellar reporting
- own vines at Saint-Étienne-de-Baïgorry and near Orthez
- purchased-fruit work
- biodynamic farming
- barrels/tanks/amphorae
- vintage-variable cuvées

Run 02's speculative early-career chronology was not promoted.

### Petit Manseng genetics

The accepted genetic edge remains `GENETICALLY_CLOSE_TO Savagnin`.

Run 02's stronger parentage language was rejected.

### Virginia Petit Manseng

The current 2025 Commercial Wine Grape Report records:

- 172 reported Petit Manseng acres
- 164 bearing
- 8 non-bearing
- 314 reported tons
- approximately 10% of statewide acreage/tonnage estimated unreported

CARTA rejected the Run 02 claim that Petit Manseng is currently Virginia's second-most-planted white vinifera. In the same report, Chardonnay and Viognier have more reported acreage.

CARTA also withheld a current global “second only to Jurançon” ranking.

### Bizkaiko grape-law history

Official 2008 regulation already listed Petit Courbu, Gros Manseng, and Petit Manseng among authorized grapes.

CARTA therefore rejected the claim that those grapes were all newly introduced only in 2020-21. Later amendments still matter for current status and spelling.

### Appellation corrections

- Pacherenc du Vic-Bilh recognition is recorded from INAO as 1948, not 1975.
- Irouléguy baseline follows current INAO dry still red/rosé/white framing; unsupported claims of historically dominant sparkling wine were withheld.
- Jurançon and Pacherenc remain distinct appellations/geographies; shared grapes or sugar level do not make a vineyard interchangeable between them.

## Geometry

Run 02 supplied approximate points and polygons in its machine appendix.

**None were accepted.**

CARTA still has zero fabricated geometry records.

## Machine packet normalization

Run 02's machine appendix was not schema-compliant with the live repository. Examples included:

- old/invalid entity type names
- IDs outside current conventions
- combined maturity/publication values
- legacy Human Reference paths
- reversed or malformed relationships
- approximate polygons presented as geometry

The accepted Run 02 records were rebuilt from scratch against current schemas.

## GIS readiness

**PASS.**

The Human Reference no longer blocks GIS.

The first spatial pass should focus on Western Pyrenees and acquire real:

- elevation/terrain
- hydrology/watersheds
- geology/parent material
- country/administrative boundaries
- appellation polygons
- municipality/reference points
- producer/site anchors

The first high-value spatial test is the relationship between Garay's reported Saint-Étienne-de-Baïgorry vines and the official Irouléguy boundary.

GIS should also test the physical relationships among Balmaseda, Bizkaia, Irouléguy, Béarn, Jurançon, Pacherenc, and the western Pyrenean terrain without forcing them into one synthetic polygon.
