# Western Pyrenees

**France and Spain**

The Western Pyrenees are the physical and cultural landscape CARTA needs in order to understand how the Basque wine regions, Irouléguy, Béarn, Jurançon, and adjacent foothill systems relate in space.

This page is deliberately **not yet a baseline reference**.

Run 02 produced enough orientation to prove the landscape belongs in CARTA, but it also overreached: it mixed eastern and western features, simplified watersheds, asserted geology too broadly, and supplied an approximate rectangular polygon. None of that geometry was accepted.

## What we know

The western end of the Pyrenees is strongly shaped by Atlantic weather, steep relief, heavy rainfall, complex drainage, and rapid transitions between coast, mountain, valley, and foothill environments.

Wine regions on both sides of the France-Spain border share parts of that physical system while remaining legally, culturally, and historically distinct.

The landscape is therefore a better home for cross-border physical questions than the [Pyrenean Atlantic ecosystem](../ecosystems/pyrenean-atlantic.md), which also includes non-spatial professional relationships extending as far as Richard Leroy in the Loire.

## What GIS needs to establish

### Terrain

- defensible western scope
- elevation model
- slope
- aspect
- major passes and mountain barriers
- coastal-to-foothill transitions

### Hydrology

- watershed divides
- Nive, Adour/Gave and relevant Spanish/Basque drainage systems
- upstream/downstream relationships
- how valleys organize settlement and viticulture

### Climate

- Atlantic precipitation gradient
- temperature and growing-season patterns
- diurnal behavior where data supports it
- exposure to maritime versus interior air masses

### Geology

- authoritative geological units
- flysch, limestone/marl, schist and other parent materials only where the geological map actually supports them
- no region-wide “soil type” shortcuts

### Wine-law overlays

- Bizkaiko Txakolina
- Irouléguy
- Jurançon
- Pacherenc du Vic-Bilh
- relevant neighboring appellations as the map expands

### Producer/site anchors

- Alfredo Egia / Balmaseda
- Imanol Garay / Maslacq
- Garay's reported Saint-Étienne-de-Baïgorry vines
- Orthez
- representative Jurançon and Irouléguy sites

## Geometry policy

CARTA will not draw one invented polygon and call it “Western Pyrenees.”

The landscape may ultimately be represented through a combination of:

- terrain-derived extent
- watershed systems
- cultural/historical regions
- official administrative boundaries
- appellation polygons
- editorial scope notes

Those layers can overlap without being forced into one shape.

## Candidate GIS authorities

The next pass should prioritize authoritative/open sources such as:

- IGN and French government geodata
- INAO/appellation geometry where available
- Basque Government / Spanish open geodata
- national geological and hydrological agencies
- Copernicus or equivalent elevation/land-cover layers where useful

OpenStreetMap may support reference points, but it should not replace official appellation or geological geometry.

## Explore next

[Pyrenean Atlantic ecosystem](../ecosystems/pyrenean-atlantic.md) · [Bizkaia](../countries/spain/regions/bizkaia.md) · [Irouléguy](../countries/france/appellations/irouleguy.md) · [Jurançon](../countries/france/appellations/jurancon.md) · [Béarn](../countries/france/regions/bearn.md)

<!-- BEGIN GENERATED CARTA PROVENANCE -->
## Record & provenance

This section is generated from CARTA machine authority. Edit the governed records, then run `python scripts/validate_data.py --write-human-reference`.

- **Profile:** `profile:western-pyrenees`
- **Maturity / publication:** `node` / `queued`
- **Primary entity:** `geofeature:western-pyrenees`

**Component entities**

- `geofeature:western-pyrenees`

<details>
<summary>Machine claims and sources</summary>

### Material claims

No material machine claims are recorded for this profile yet.

### Sources

No source records are projected for this profile yet.

</details>

### Open questions

- Define defensible scope from real terrain, watershed and cultural layers
- Acquire authoritative DEM, hydrology, geology and administrative/appellation geometries
- Do not use the Run 02 approximate rectangle as geometry
<!-- END GENERATED CARTA PROVENANCE -->
