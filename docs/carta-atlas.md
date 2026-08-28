# CARTA Atlas

CARTA Atlas is the geographic way into CARTA.

It should feel familiar before it feels novel: a person can begin with the world, orient to a country, understand ordinary geography, and then move through wine regions, subregions, appellations, places, vineyards, producers, grapes, and relationships at progressively finer scales.

The goal is not to make another decorative wine map. The goal is to make wine geography easier to understand while letting CARTA's deeper spatial, temporal, relational, legal, terroir, and ampelographic knowledge become visible when it is useful.

## Human experience

A useful CARTA Atlas should let someone:

- start with recognizable world and country geography;
- learn wine geography in relation to cities, rivers, mountains, coasts, borders, and neighboring regions;
- zoom naturally from country to wine region to subregion to appellation and, where evidence supports it, vineyard or parcel scale;
- click a mapped feature and understand what it is without leaving the map;
- move from a mapped feature into the Human Reference for deeper reading;
- search for places, appellations, grapes, producers, and other CARTA subjects;
- see uncertainty and incomplete spatial knowledge honestly rather than through invented precision;
- eventually explore how geography, names, classifications, producers, plantings, and relationships change through time.

## Semantic zoom

The Atlas should reveal the right information at the right scale rather than display every label and boundary at once.

At broad scales, countries and major wine regions matter. At closer scales, subregions and appellations become useful. At local scales, communes, vineyards, parcels, producer locations, terrain, and other detailed features may appear when CARTA has defensible data for them.

This is a presentation rule, not a new authority layer. What appears at each zoom level is derived from governed CARTA records and sourced geographic data.

## STRATA as the layer system

STRATA gives the Atlas its deeper structure:

- **Space** — ordinary geography, wine regions, boundaries, containment, proximity, terrain, and mapped locations.
- **Time** — historical boundaries, changing names and classifications, producer movement, plantings, and other dated geography.
- **Relationships** — selected graph relationships that become meaningful when viewed spatially.
- **Appellations** — legal wine geography and its nested or overlapping structures.
- **Terroir** — elevation, slope, aspect, geology, soils, hydrology, climate, and related evidence-backed layers.
- **Ampelography** — grape occurrence, legal authorization, naming, historical distribution, and relationships to places and producers.

The default map should remain understandable without turning every STRATA layer on. Depth should be available, not imposed.

## Authority and geometry

CARTA Atlas is a projection of CARTA, not a second source of truth.

Geographic truth can exist without digital geometry. CARTA may know that one appellation sits within another before it possesses either polygon. Likewise, a producer may be reliably associated with a municipality without CARTA knowing an exact vineyard point.

When geometry is used, it must retain provenance. Each adopted spatial dataset should have a documented source, license, geographic meaning, precision, and appropriate CARTA linkage.

Two rules apply:

> **No geometry without provenance. No geometry inference merely for visual completeness.**

> **Absence of geometry is not absence of spatial knowledge.**

## Technical direction

The first interactive Atlas implementation is expected to use MapLibre and open or appropriately licensed geographic data. GeoJSON is a practical early interchange and prototype format; source datasets may arrive as Shapefile, GeoPackage, GeoJSON, APIs, or other GIS formats.

The long-term delivery format may evolve as scale requires it. The durable requirement is that map features remain linked to stable CARTA entity IDs and that the visual layer can be regenerated from governed authority and documented spatial sources.

## Prototype standard

A prototype should already be useful to a human being. It should not exist merely to demonstrate that a map can render.

The first useful Atlas should therefore provide recognizable geographic orientation, meaningful wine-region navigation, semantic zoom, clickable CARTA-linked features, and a clear path into Human Reference. Experimental code and incomplete coverage are acceptable. Project-internal language, fake precision, and visually impressive but informationally empty interactions are not.
