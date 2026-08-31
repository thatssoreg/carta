# CARTA Atlas Beaujolais Regional Foundation Research Handoff

## Foundations and editorial direction

**Executive verdict**

The finished Beaujolais Atlas world should fundamentally be about **how apparent sameness fractures into meaningful difference**.

Beaujolais is unusually well suited to CARTA because the region initially looks simple: one grape occupies 96% of the 2024 regional grape distribution, red wine represented 94% of production in that same official snapshot, and the public regional hierarchy is commonly taught as Beaujolais, Beaujolais-Villages, and ten crus. Yet nearly every part of that simplification needs a second look. The physical region crosses Paleozoic granite, schist, metamorphic and volcano-sedimentary formations in the north, younger limestone-rich sedimentary formations in the south, piedmont deposits toward the Saône, substantial changes in altitude and slope, and more than 300 soil variants identified by the regional terroir program. One dominant grape therefore does not produce one place, one rule, or one cellar script. fileciteturn17file0L2-L2 citeturn18view3turn1search3turn1search1

The strongest thesis is:

> **Beaujolais shows what happens when one dominant grape is asked to carry many places, techniques, markets and reputations at once. The map matters precisely because the grape changes so little.**

That thesis is stronger than “Beaujolais is Gamay,” because Gamay is the constant rather than the explanation. It is stronger than “Beaujolais is granite,” because official geological work explicitly demonstrates a much more heterogeneous substrate. It is stronger than “Beaujolais is carbonic,” because carbonic maceration, semi-carbonic maceration, whole-cluster handling and conventional yeast fermentation are distinct techniques, none of which is a universal legal requirement. It is stronger than “Beaujolais is Nouveau,” because primeur represented a historically enormous but never total share of regional production. It is also stronger than “Beaujolais is natural wine,” because Chauvet, Lapierre, Foillard and their peers explain an important transformation in regional culture without exhausting the histories of Château Thivin, southern Beaujolais, Chardonnay, négociants, cooperatives, conventional cellar approaches or the crus themselves. citeturn18view2turn11search0turn11search10

This makes Beaujolais different from **Jura**. Jura teaches plurality through several grapes, overlapping appellation families and visibly divergent cellar traditions. Beaujolais can teach plurality through the opposite condition: one overwhelmingly dominant grape encountering many legal origins, geological contexts, producer choices and reputation regimes. The existing Jura implementation should remain a comparison and regression case, not a prose template. fileciteturn13file0L2-L2

It is also different from **Béarn / Jurançon**. That world is organized around wet Atlantic foothills, autumn drying conditions, local Manseng varieties and divergent dry/sweet legal paths. Beaujolais is less a “physical paradox resolved by wine law” than a lesson in **spatial specificity, technique and reputation under apparent varietal uniformity**. The shared architecture explicitly permits that difference. fileciteturn14file0L2-L2

Beaujolais is the right next proof because it simultaneously stress-tests region versus appellation, overlapping legal geography, a dominant grape, named sites without safe vineyard polygons, producer-base mapping, informal networks, succession, techniques that are often mistakenly universalized, mass-market cultural history, modern natural-wine history, and a strong cross-region Burgundy route.

**The existing five-pillar `regional_world` contract is sufficient. No Beaujolais-specific frontend or new regional abstraction is justified.** Jura and Béarn already proved that the five pillars, data-authored map-click priority, glossary, producer points, native subjects, reversible context returns and data-authored regional prose can support different regional personalities. fileciteturn13file0L2-L2 fileciteturn14file0L2-L2

The only potential generalization should be reconciled with the separate terrain run: if that architecture does not already support **data-authored camera/terrain moments tied to subjects**, Beaujolais provides a strong reusable requirement. That need should not be implemented independently here.

**Current CARTA baseline**

At repository inspection, live `main` matched the editorial-foundation state described in the prompt. The repository continues to enforce one machine authority with Human Reference and Atlas as projections; spatial truth must not be invented merely to improve presentation. fileciteturn2file0L2-L2 fileciteturn3file0L2-L2

| Coverage area | Assessment | Current state | Handoff |
|---|---|---|---|
| Beaujolais regional profile | **Already strong** | Correctly treats the region label as an orientation anchor derived from child geometry, not a regional polygon. Correctly foregrounds one dominant grape and many places. | Preserve architecture and epistemic caution. Rewrite editorial thesis for finished world. fileciteturn8file0L2-L2 |
| 2024 vineyard measures | **Strong, dated** | 11,771 ha claimed, 12-appellation institutional framing, 85 “wine-growing communes,” 96% Gamay, 4% Chardonnay, 94% red, 4% white, 2% rosé. | Keep as **2024 measures**, never silently promote to 2026 current values. fileciteturn17file0L2-L2 |
| Twelve-AOC wording | **Needs legal correction** | Inter Beaujolais’s institutional framing says 12 AOCs/appellations. | Current August 2026 Beaujolais cahier legally treats `Villages` as a mention following AOC Beaujolais, rather than establishing a separate current specification. Learner shorthand and strict legal identity must be distinguished. citeturn19view0turn20search8 |
| Commune count | **Scope conflict, not factual contradiction** | 2024 regional claim says 85 wine-growing communes. | Current 2026 Beaujolais legal geographical area lists 77 Rhône communes plus 11 Saône-et-Loire communes, 88 total. These measure different things and dates. Preserve both with scope. fileciteturn17file0L2-L2 citeturn18view3 |
| Ten crus | **Strong** | Brouilly, Côte de Brouilly, Chénas, Chiroubles, Fleurie, Juliénas, Morgon, Moulin-à-Vent, Régnié, Saint-Amour. | Preserve. Give uneven depth according to teaching role. fileciteturn8file0L2-L2 |
| Broad colors | **Strong, now legally stronger** | Existing copy says Beaujolais and Villages contexts can be red, white or rosé. | Current 2026 Beaujolais specification confirms all three; `nouveau`/`primeur` is red or rosé only. citeturn19view0turn18view0 |
| Morgon | **Strong baseline, thin law/site depth** | Existing native guide correctly distinguishes legal origin from style and identifies Côte du Py without making it the whole appellation. | Deepen legal rules, six named local sites, geology and producer plurality. fileciteturn9file0L2-L2 |
| Gamay | **Usable node, insufficient native subject** | Current Human Reference is explicitly a navigation stub. | Must become baseline native grape treatment before finished Beaujolais world. fileciteturn10file0L2-L2 |
| Geology | **Strong caution, thin teaching resolution** | Current page correctly rejects “Beaujolais = granite.” | Replace generic caution with a minimal contrast model grounded in official geological work. fileciteturn8file0L2-L2 |
| Lapierre | **Strong baseline** | History, current family operation, organic certification, current semi-carbonic workflow and sulfur caveat are unusually well reconciled. | Reuse, do not re-research from scratch. Add spatial base only at defensible precision. fileciteturn11file0L2-L2 |
| Jules Chauvet | **Usable relationship, insufficient dossier** | Direct Lapierre guidance is supported. | Add separate historical figure authority and sharply distinguish direct guidance from diffuse influence. |
| Gang of Four | **Strong ecosystem treatment** | Correctly informal, attributed to Kermit Lynch, and does not infer pairwise collaboration. | Preserve exactly this ontology discipline. fileciteturn12file0L2-L2 |
| Wider producer world | **Missing** | Region is currently overly dependent on Lapierre/Gang route. | Add a deliberately mixed teaching roster. |
| Nouveau / primeur | **Missing as a regional historical mechanism** | Baseline references production proportions but does not yet teach the history. | Major Culture + Rules + Time component. |
| Cellar-method distinctions | **Missing** | No robust native carbonic/semi-carbonic teaching layer. | Add glossary and producer contrast. |
| Succession | **Thin** | Lapierre succession already strong. | Add Terres Dorées and selectively Foillard/Métras only where evidence is clean. |
| Localities and sites | **Thin** | Villié-Morgon and Côte du Py are present conceptually. | Add only wine-meaningful places; geometry remains conservative. |
| Terrain | **Pending shared infrastructure** | Separate run underway. | Use the terrain brief in this handoff after reconciliation. |
| Cross-region route | **Missing for Beaujolais** | Burgundy is already a native Atlas world. | Gamay’s Burgundian legal history is the strongest evidence-backed bridge. |

**Correction and risk register**

| Existing or common claim | Evidence finding | Status | Recommended treatment | Best source |
|---|---|---|---|---|
| “Beaujolais has twelve AOCs.” | Inter Beaujolais legitimately uses a 12-appellation regional framing, but the August 2026 Beaujolais cahier defines `Villages` as a mention following AOC Beaujolais. | **Needs qualification** | Use “Beaujolais, its Villages level/mention, and ten crus” in legal teaching. A 12-part regional navigation set remains pedagogically defensible if provenance states the institutional framing. | 2026 Beaujolais cahier. citeturn19view0turn20search7 |
| “Beaujolais has 85 communes.” | 85 is the 2024 regional count of wine-growing communes; the current 2026 legal geographical area contains 88 communes. | **Scoped, not contradictory** | Keep 85 only as dated 2024 regional measure. Use 88 for current legal geographical-area commune scope. | CARTA 2024 claim; 2026 cahier. fileciteturn17file0L2-L2 citeturn18view3 |
| “96% Gamay, 4% Chardonnay.” | Strong official 2024 grape-distribution snapshot. | **Reusable** | Preserve observation date and denominator. Never write “Beaujolais is currently 96% Gamay” without date. | Inter Beaujolais key figures via current CARTA source. fileciteturn19file0L2-L2 |
| “94% red, 4% white, 2% rosé.” | Strong official 2024 production-color split. | **Reusable** | Keep dated and separate from legal color permissions. | CARTA machine claims. fileciteturn17file0L2-L2 |
| “The ten crus are in northern Beaujolais.” | Useful orientation, but not a geological or stylistic definition of “north.” | **Reusable, broad** | Keep as learner orientation, then immediately show internal geological/terrain differences. | Inter Beaujolais / current profile. fileciteturn8file0L2-L2 |
| “Beaujolais is granite.” | Official terroir work reports more than 300 soil variants associated with about 15 principal rock types. Current legal text contrasts northern Paleozoic rocks with southern Triassic/Jurassic sedimentary formations. | **Rejected as generalization** | Granite is one important formation, not the regional substrate. | Inter Beaujolais terroir study; 2026 cahier. citeturn1search1turn18view3 |
| “Morgon is granite.” | Morgon includes substantial granite but also “blue stone”/metamorphic-volcano-sedimentary contexts and piedmont material; Inter Beaujolais summarizes 52% granite, 37% blue stone, 11% piedmont deposits. | **Rejected as complete account** | Teach Côte du Py and Corcelette as contrasting local contexts without soil-to-flavor causality. | Inter Beaujolais Morgon. citeturn1search16 |
| “Côte du Py is Morgon.” | Côte du Py is an important named site associated with Py hill, not the whole appellation. | **Rejected as equivalence** | Keep separate appellation, hill and wine-site identities. | INAO + current CARTA Morgon. citeturn24view0 fileciteturn9file0L2-L2 |
| “All Beaujolais is carbonic.” | Carbonic, semi-carbonic and whole-cluster fermentation are distinct. Current Beaujolais law describes semi-carbonic as regional custom in its causal link section but does not make it a universal required vinification. | **Rejected** | Teach technique separately from law. | OIV/AWRI; 2026 cahier. citeturn11search0turn11search10turn18view3 |
| “Traditional Beaujolais fermentation is carbonic.” | Too broad. Lapierre’s first-party material says semi-carbonic; Dutraive describes whole bunches in CO₂-saturated tanks; Terres Dorées has long provided a destemmed, non-carbonic counterexample. | **Overbroad** | Use producer-specific practices and dated scopes. | Producer sources. fileciteturn11file0L2-L2 citeturn13search0turn25search13 |
| “Jules Chauvet invented carbonic maceration.” | Chauvet researched and wrote about fermentation and carbonic maceration; a 1963 scientific paper predates the later producer movement but does not make him the inventor of the mechanism. | **Rejected** | Present him as researcher, merchant/taster and transmission figure. | 1963 research record. citeturn11search4 |
| “Chauvet mentored all four members of the Gang of Four.” | Direct guidance is first-party evidenced for Marcel Lapierre. For Foillard, importer language supports following Chauvet’s teachings. Group membership alone cannot establish bilateral mentorship. | **Rejected as blanket claim** | `INFLUENCED_BY` where evidence supports it; `MENTORED_BY` only with direct evidence. | Lapierre; Kermit Lynch. fileciteturn11file0L2-L2 citeturn12search9 |
| “Gang of Four was an organization.” | It is an importer-coined nickname for an informal producer cluster. | **Rejected** | Preserve ecosystem/community-of-practice treatment. | Current CARTA + Kermit Lynch. fileciteturn12file0L2-L2 |
| “Every Gang-of-Four member used one identical protocol.” | Lynch describes broad shared values, not an enforceable protocol. Producer methods vary and change. | **Rejected** | Never infer practice edges from membership. | Kermit Lynch; CARTA evidence policy. citeturn12search9 fileciteturn5file0L2-L2 |
| “Natural wine saved Beaujolais.” | Low-intervention producers materially changed international attention and producer culture, but regional history also includes crus, négociants, cooperatives, Nouveau, conventional estates and legal evolution. | **Rejected as totalizing causal narrative** | Frame natural-wine producers as important historical agents inside a plural story. | Kermit Lynch; regional history. citeturn12search9turn1search2 |
| “Nouveau ruined Beaujolais.” | Nouveau grew dramatically to about 500,000 hl in the mid-1980s but, according to the current specification, never exceeded half of total production. Evidence does not support a simple single-cause “ruin.” | **Rejected** | Teach global market success plus later reputation tension without a decline/redemption myth. | 2026 Beaujolais cahier. citeturn18view2 |
| “The year’s cheapest novelty became the reference point for modern natural wine.” | “Cheapest” is unsourced; “reference point” is ambiguous; direct Nouveau-to-natural-wine causality is not established. | **Reject candidate wording** | Replace with a question about how an early-release wine came to shape perception of a region whose crus and later low-intervention movement tell different, overlapping stories. | 2026 legal history + producer-network evidence. citeturn18view2turn12search9 |
| “Gamay was banned from Burgundy in 1395 and moved to Beaujolais.” | Philip the Bold’s 1395 ordinance did target Gamay in ducal territory, but enforcement was resisted and the episode does not document a one-step migration into Beaujolais or a clean modern Burgundy/Beaujolais border story. | **Reject one-sentence mythology** | Teach the ordinance as a historical attempt to police variety and vineyard economy. | Serious historical reporting based on scholarship. citeturn7search4turn7search3turn7search6 |
| “The 1395 edict simply ordered Pinot instead.” | Serious historical analysis notes that the text and its context are more complex than the standard Pinot-versus-Gamay fable. | **Reject simplification** | Bind exact historical-event wording to scholarship before ingestion. | Historical scholarship/reporting. citeturn7search3turn7search4 |
| “Lapierre never uses sulfur.” | Estate says it works without sulfur where possible but permits light doses for some batches; `N` identifies bottles without sulfur. | **Rejected** | Preserve current CARTA’s narrowed wording. | Lapierre first party. fileciteturn11file0L2-L2 |
| “Lapierre is organic, therefore always certified organic since the 1980s.” | First-party distinction: organic-principle farming dates to the 1980s; Ecocert certification dates to 2004. | **Correct only when separated** | Keep practice history and certification date as separate claims. | Lapierre first party. fileciteturn11file0L2-L2 |
| “Foillard took over in 1980/1981/1982.” | Public sources conflict. A 2025 independent report gives 1981; trade pages give other dates. | **Contested** | Use 1981 provisionally if needed, with explicit source; do not manufacture precision through averaging. | 2025 independent reporting. citeturn12search3turn12search2 |
| “Foillard has 14/20/23 ha.” | Sources conflict and may reflect different dates, estate/managed acreage or copy lag. | **Contested** | Date each figure or omit current area until reconciled. | Kermit Lynch vs 2025 reporting. citeturn12search9turn12search3 |
| “Foillard is certified organic.” | Current reporting indicates substantial organic practice but not blanket estate certification. | **Reject blanket certification** | Describe farming practice only within source scope. | 2025 reporting. citeturn12search3 |
| “Foillard was directly mentored by Chauvet.” | Current evidence in this run supports following Chauvet’s teachings, not a proven formal bilateral mentorship. | **Too strong** | `INFLUENCED_BY` is safer. | Kermit Lynch. citeturn12search9 |
| “Yvon Métras is based in Fleurie.” | Multiple merchant sources identify bottling/base at Bize, Vauxrenard while his most famous holdings/wines are strongly associated with Fleurie. | **Identity/geography risk** | Do not use Fleurie appellation as cellar location. Vauxrenard is a base lead, not yet a primary-sourced exact GIS point. | Merchant bottle information. citeturn25search14turn25search17 |
| “Yvon to Jules Métras is a completed estate succession.” | Merchant sources indicate Jules began independently in 2014 and later worked/took over family vines, but evidence is not clean enough to collapse their identities or define a completed transfer. | **Provisional / unresolved** | Keep Yvon and Jules separate producer identities. Do not create full succession edge yet. | Merchant reporting only. citeturn25search15turn25search16 |
| Métras “1898 vines” / extreme vine ages | Multiple merchant pages repeat nearly identical copy. | **Lead only** | Do not treat repetition as corroboration. Require producer, cadastral, viticultural or independent evidence. | Merchant propagation cluster. citeturn25search4turn25search9turn25search17 |
| “A named cuvée proves ownership of Grille Midi or La Madone.” | Label/site association does not prove title, tenancy or exact boundary. | **Rejected inference** | Record only the supported producer-site relationship type and source. | Evidence policy. fileciteturn5file0L2-L2 |
| “High elevation makes wine fresh.” | Elevation is measurable; sensory causation requires much more context. | **Rejected causal shortcut** | Terrain may show altitude, slope and exposure; copy must stop at physical context unless a separate causal claim is evidenced. | CARTA evidence doctrine. fileciteturn5file0L2-L2 |

**Recommended regional thesis**

**Primary thesis**

> **One dominant grape makes the differences harder to ignore. Beaujolais is a region where Gamay runs through broad regional wine, steep crus, limestone country, granite and “blue stone,” Nouveau, cellar experiments and changing producer networks. The grape stays recognizable; the meanings around it keep moving.**

**Hero kicker**

> **One grape · many places · a reputation still moving**

**Learner-facing opening paragraph**

> Gamay covers almost all of the vineyard, which is exactly why the map matters. Move from the limestone country of the south toward the older rocks and steeper hills of the north, from Beaujolais into a cru, or from a wine made for November release to a cellar working for something slower, and the same grape keeps entering a different argument. Beaujolais is not one style. It is a place where geography, rules, technique, trade and people have repeatedly changed what the region means.

The thesis beats **Gamay** alone because the grape is the controlled variable. It beats **granite** because the geology is demonstrably heterogeneous. It beats **Nouveau** because primeur is a powerful historical mechanism but never the total regional output. It beats **carbonic** because cellar techniques vary. It beats **natural wine** because the Lapierre/Chauvet network becomes more intelligible when placed beside Château Thivin, Domaine de la Grand’Cour, southern Chardonnay and Terres Dorées rather than treated as the endpoint of history. citeturn18view2turn1search1turn13search0turn25search0

**Questions Worth Following**

| Question | Kicker | Starting subject | Route / payoff | Required claim support | Ready now? |
|---|---|---|---|---|---|
| **How can one grape make the map more important, not less?** | 96% Gamay · ten crus · ground that refuses one slogan | `place:beaujolais` | 2024 grape share → Gamay → broad Beaujolais → Morgon/Côte de Brouilly/Fleurie → geology contrasts. Payoff: varietal sameness heightens spatial difference. | 2024 grape measure; cru legal origins; regional geology; Gamay native subject. | **Yes after Gamay enrichment.** fileciteturn17file0L2-L2 citeturn1search1 |
| **How did a wine designed for release within weeks come to shape how the whole region was recognized?** | Nouveau · global success · a reputation bigger than one style | `place:beaujolais` | 19th-century early trade → 1951 permission → 1985 third Thursday → mid-1980s volume → current primeur rule → crus. Payoff: Nouveau was huge, but never the whole region. | Current legal history; current Nouveau share; trade/reputation interpretation. | **Yes, with cautious reputation wording.** citeturn18view2turn1search0 |
| **What does “carbonic” actually tell you about a Beaujolais?** | Whole bunches · CO₂ · several cellar paths | `practice:carbonic-maceration` candidate/native practice | OIV mechanism → semi-carbonic distinction → Lapierre → Grand’Cour → Terres Dorées counterexample. Payoff: technique is not appellation identity. | OIV/AWRI definitions; dated producer practice claims. | **Yes after glossary/practice authority.** citeturn11search0turn11search10turn13search0turn25search13 |
| **What did the 1395 Gamay ordinance actually change, and what did it not?** | Burgundy law · Beaujolais mythology · one grape crosses the border | `grape:gamay-noir-a-jus-blanc` | Gamay → historical event → Burgundy → return to modern Beaujolais. Payoff: legal action, economic history and later regional mythology separate. | Historical event entity/claims; serious scholarship; Burgundy native subject. | **Yes after event ingestion.** citeturn7search3turn7search4turn7search6 |
| **Why does one hill carry two cru names?** | Mont Brouilly · two legal areas · one terrain anchor | `geographic_feature:mont-brouilly` candidate | Terrain → Brouilly → Côte de Brouilly → Château Thivin. Payoff: physical landform and legal origin are separate but spatially legible. | Hill feature, both AOC geometries, Thivin base. | **Yes after terrain reconciliation.** citeturn14search9turn2search0 |

**Five-pillar world architecture**

| Pillar | Pillar thesis | Learner outcome | Recommended components | Known subjects | Missing authority | Map opportunity | Do not include |
|---|---|---|---|---|---|---|---|
| **Place** | One continuous wine landscape contains major physical and legal changes. | Understand Saône-facing slopes, western hills, north/south geological shorthand and where it fails. | Regional orientation; Mont Brouilly; Py hill/Morgon; Fleurie/Chiroubles slope context; southern Pierres Dorées; Saône edge. | `place:beaujolais`, `appellation:morgon`; likely existing appellation IDs. | Local geographic-feature/site entities; geology claims. | Region fit → terrain anchor → cru geometry. | Invented regional polygon; vineyard shading from AOC polygons. |
| **Grapes & Wines** | Gamay dominates plantings but does not define one style or one legal permission. | Separate grape identity, legal encépagement, wine color, Nouveau and cellar technique. | Gamay native dossier; Chardonnay/white route; 2024 grape shares; broad color split; primeur vs non-primeur; carbonic glossary. | `grape:gamay-noir-a-jus-blanc`, `grape:chardonnay`, `wine:lapierre-morgon`. | Gamay genetics/history; practice entities; white-Beaujolais anchors. | Explore grape while holding map; optional “Go to Burgundy” route. | Flavor stereotype cards; implication that Gamay is legally sole grape everywhere. |
| **People** | Producers changed what Beaujolais could mean, but no one network owns the story. | Understand low-intervention transmission, canonical continuity, cellar alternatives and succession. | Lapierre; Foillard; Thivin; Grand’Cour/Dutraive; Terres Dorées; Chauvet. | Lapierre and Chauvet people already partly present. | Other producer entities/profiles/relationships. | Honest base markers; Explore vs Go. | Ranking; cult-price logic; every Gang member simply because of nickname. |
| **Culture** | Beaujolais reputation has been repeatedly remade through urban markets, Nouveau, networks and trade. | Connect Lyon/Paris, primeur, négociants, producer networks and changing prestige. | Lyon market; Paris/Nouveau; 1951/1985 timeline; Gang of Four context; cooperative history; Then/Now Nouveau. | Gang ecosystem. | Market/cultural claims; historical event entities where useful. | Lyon/Paris rabbit-hole lines only when graphically useful, otherwise native subject transitions. | Nostalgia; “Nouveau bad, natural wine good.” |
| **Rules** | Legal names tell you origin and permitted production, not quality or a mandatory cellar recipe. | Distinguish Beaujolais, Villages mention, commune indications, crus, primeur and vineyard parcels. | Current 2026 Beaujolais rule; 10 cru guides; colors; grape permissions; Nouveau timing; overlap lesson. | `appellation:beaujolais`, `appellation:morgon`. | Latest current specs/reconciliation for remaining crus. | Data-authored click priority; retain context polygons. | Twelve identical law cards; carbonic presented as legal rule. |

## Landscape, geology and appellation geography

**Physical landscape and terrain brief**

The legally defined Beaujolais geographical area extends along the eastern edge of the Massif Central above the Saône valley, between Lyon and Mâcon. The August 2026 Beaujolais specification describes an approximately **55 km north-south** vineyard corridor, roughly **15 to 20 km east-west**, with the legal-area landscape spanning approximately **180 to 550 m** elevation. The same specification places the Saône plain to the east and the Monts du Beaujolais to the west. citeturn18view3

The useful physical lesson is not “north high, south low.” It is a repeated west-east transition from higher, hillier country toward the Saône plain, crossed by local valleys and hills, combined with a north-south geological change. The learner should see why vines cluster on slopes and lower hill country while the higher western landscape becomes greener and less continuously viticultural, but Atlas should not shade unplanted land as vineyard merely because it is inside a wine region. citeturn1search14

**Terrain anchors**

| Anchor | Why it matters | Terrain treatment | Claim posture |
|---|---|---|---|
| **Mont Brouilly** | A distinct 485 m hill physically anchors both Brouilly and Côte de Brouilly; Côte de Brouilly occupies slopes on the mountain while Brouilly surrounds it more broadly. | Close oblique or hillshade moment showing hill form plus both legal outlines. | Strong physical/legal record. No sensory causality. citeturn14search9turn2search0 |
| **Py hill / Côte du Py** | Morgon’s legal area surrounds Py hill; Côte du Py is one important named local site, not synonymous with Morgon. | Terrain close-up with Morgon polygon, hill label and non-polygon site label until authoritative site geometry exists. | Strong hill/place relationship; site polygon withheld. citeturn24view0turn1search16 |
| **Fleurie slopes** | Fleurie occupies steep Monts du Beaujolais slopes overlooking the Saône and is one commune. | Show eastern opening, village and slope break. | Strong orientation; do not add “feminine/elegant because slope” language. citeturn14search3 |
| **Chiroubles** | Cru geography is especially useful for understanding higher hill-country viticulture. | Compare its vertical position with neighboring Fleurie and Morgon. | Physical comparison only. citeturn2search3 |
| **Juliénas / Mont de Bessay** | Demonstrates that northern cru geology and relief are not one granite template. | Terrain moment paired with geology layer if available. | Strong physical anchor. citeturn1search4turn3search2 |
| **Southern Pierres Dorées / Charnay** | Provides the strongest terrain/geology counterpoint to the northern-cru stereotype and gives Chardonnay a spatial home. | Quiet rolling-hill view rather than dramatic relief effect. | Use limestone/sedimentary record, not sensory outcome. citeturn18view3turn25search0 |
| **Saône-facing eastern edge** | Makes Beaujolais’s ordinary geography intelligible and explains why several cru descriptions orient toward the plain. | Keep Saône and plain visible at region/cru transitions. | Orientation only. citeturn14search14turn14search3 |

**Recommended camera/view sequence**

Start with the existing child-geometry-derived regional fit, not an authored Beaujolais shape. Move next to an eastward-readable view that keeps the Saône plain and Monts du Beaujolais together. The first dramatic terrain moment should be Mont Brouilly because the same hill immediately explains the difference between a physical feature and two legal wine areas. A second terrain moment should move to Morgon/Py. A third, quieter move should travel south to Charnay/Pierres Dorées so terrain is not accidentally equated with “cru quality.”

**Record versus interpretation**

Record may state location, hill height when sourced, slope orientation described by INAO, legal boundaries, altitude, geological unit and adjacency.

Interpretation may say, for example, “Mont Brouilly is a useful place to see why a hill and an appellation are not the same object,” because that reading rests on visible legal and physical facts.

Prohibited shortcuts include “higher equals fresher,” “south-facing means riper wine,” “blue stone produces minerality,” “granite makes floral Gamay,” or any equivalent terrain-to-flavor claim without separate evidence.

**Geology / soil teaching model**

Official Beaujolais research is the right foundation because it actively undermines the one-word granite story. Inter Beaujolais reports more than 300 soil variants developed from roughly 15 principal rock types and a geological history extending hundreds of millions of years. The current Beaujolais specification provides an especially useful regional simplification: older Paleozoic formations dominate the northern half, while younger Triassic and Jurassic sedimentary formations become important in the south. citeturn1search1turn18view3

| Geographic context | Geological evidence | Source | Learner value | Mapping potential | Caveat |
|---|---|---|---|---|---|
| **Northern hill country** | Granite, porphyry, schist and volcano-sedimentary/metamorphosed formations occur across Paleozoic terrain. | Current Beaujolais cahier. citeturn18view3 | Immediately breaks “the north is granite” into an older-rock family. | Strong if BRGM/official terroir vectors can be licensed and reconciled. | Do not map one generalized “granite north.” |
| **Morgon, Py vs Corcelette/Douby** | Official regional summary gives a mix of granite, “blue stone” and piedmont deposits; Py sits in the non-granite story while Corcelette/Douby are useful granite contexts. | Inter Beaujolais Morgon. citeturn1search16 | One cru alone disproves one-soil identity. | Appellation geometry strong; site geometry currently weak. | Percentages are regional-program simplification, not parcel-level truth. |
| **Mont Brouilly / Côte de Brouilly** | “Blue” dioritic/volcanic and metamorphic formations are important alongside granite sectors. | INAO/official Beaujolais context. citeturn6search5turn2search0 | Physical hill + distinctive geology + legal split is unusually teachable. | High terrain and geology value. | “Blue stone” is vernacular shorthand requiring translation. |
| **Juliénas and northern edge** | Schist, dioritic/volcanic, sandstone and clay-bearing contexts complicate the granite shorthand. | Inter Beaujolais Juliénas. citeturn1search4 | Demonstrates diversity at the northern end rather than only north-versus-south. | Medium. | Avoid converting official broad categories into flavor predictions. |
| **Eastern foot / piedmont** | Colluvial/alluvial or piedmont deposits occur where slopes relax toward the Saône. | Morgon and regional legal sources. citeturn1search16turn18view3 | Helps explain upslope/downslope differences without implying every low area is vineyard. | High if source resolution is sufficient. | A geological deposit is not a planted-vineyard layer. |
| **Southern Beaujolais / Pierres Dorées** | Younger Triassic/Jurassic sedimentary formations, especially limestone-bearing contexts, contrast with the Paleozoic north. | 2026 Beaujolais cahier; Terres Dorées current estate context. citeturn18view3turn25search0 | Provides the strongest spatial counterexample to “Beaujolais = granite” and gives Chardonnay meaningful geography. | High at regional teaching scale. | “Clay-limestone” must not become a taste adjective. |

**Implementation guidance:** terrain/geology should answer **“what is under and around this place?”**, not “what must this wine taste like?” A geology layer may explain diversity, drainage context, parent material and how appellation geography intersects physical formations. It must not generate sensory predictions.

The detailed Inter Beaujolais terroir material is valuable as a source, but **redistribution/reuse rights for detailed maps were not established in this run**. Do not scrape institutional graphics into Atlas. BRGM material should enter only after dataset-specific provenance and license reconciliation.

**Appellation matrix**

A major legal correction precedes this table. The public regional shorthand remains “12 appellations,” but the **current August 2026 Beaujolais specification treats `Villages` as a mention attached to AOC Beaujolais**, together with `supérieur`, commune provenance names and `primeur`/`nouveau`. That legal fact should be visible in Rules even if the learner navigation continues to present Beaujolais-Villages as one familiar regional origin level. citeturn19view0turn20search8

For the crus, current INAO pages identify them as red AOPs centered on Gamay. Historical and harmonized cru specifications also allow narrow legacy mixed plantings of Aligoté B, Chardonnay B and Melon B under tightly bounded conditions rather than establishing those grapes as ordinary modern blending alternatives. Before machine ingestion of accessory-grape wording, the later implementation should reconcile each current 2024 cahier directly rather than copy one cru’s transitional clause across all ten. citeturn22search4

| Appellation / learner origin | Scope / communes | Colors | Grapes | Meaningful rules | Geometry | Depth recommended |
|---|---|---|---|---|---|---|
| **Beaujolais** | Current legal geographical area: 88 communes, 77 Rhône + 11 Saône-et-Loire. | Red, rosé, white. | White: Chardonnay B only. Red/rosé: Gamay N principal; accessory list includes Aligoté, Chardonnay, Gamay de Bouze, Gamay de Chaudenay, Melon, Pinot Gris, Pinot Noir under defined proportions. | `supérieur`; `Villages`; specified commune provenance; `primeur`/`nouveau` red/rosé only. 2026 minimum planting density 5,000 vines/ha. | Existing INAO geographic-area geometry. | **regional-world major**. citeturn17view0turn18view0turn19view1 |
| **Beaujolais followed by Villages** | 38 communes in current 2026 specification. | Red, rosé, white. | Same legal encépagement framework as Beaujolais; white Chardonnay only. | Legally a current Beaujolais mention, not a separate current cahier. Nouveau/primeur possible for red/rosé. | Existing INAO representation should be reconciled to current legal identity. | **regional-world major**. citeturn17view0turn20search8 |
| **Brouilly** | Cercié, Charentay, Odenas, Quincié-en-Beaujolais, Saint-Étienne-la-Varenne, Saint-Lager. | Red only. | Gamay N principal; reconcile current legacy accessory clause before ingesting details. | No Nouveau. Mont Brouilly relationship essential; `Pisse Vieille` is a specific named legal/local label context requiring exact current clause before learner copy. | Existing INAO. | **enhanced guide**. citeturn14search9turn6search2 |
| **Côte de Brouilly** | Cercié, Odenas, Quincié-en-Beaujolais, Saint-Lager, on Mont Brouilly. | Red only. | Gamay N principal; legacy accessory provision needs current-spec reconciliation. | Distinguish physical hill from legal area. | Existing INAO. | **regional-world major** because terrain. citeturn2search0 |
| **Chénas** | Chénas and La Chapelle-de-Guinchay. | Red only. | Gamay N principal. | No Nouveau; legal origin crosses Rhône/Saône-et-Loire departmental boundary. | Existing INAO. | **basic native guide**. citeturn14search15 |
| **Chiroubles** | Chiroubles. | Red only. | Gamay N principal. | Terrain/elevation context more important than quantitative rule cards. | Existing INAO. | **enhanced guide**. citeturn2search3 |
| **Fleurie** | Fleurie. | Red only. | Gamay N principal. | Current cahier homologated 20 Feb 2024. Treat named sites separately from AOP. | Existing INAO. | **regional-world major** for producer/site/current classification story. citeturn14search3 |
| **Juliénas** | Juliénas, Jullié, Emeringes, Pruzilly. | Red only. | Gamay N principal. | Four-commune cru; northern geology is unusually mixed. | Existing INAO. | **basic native guide**. citeturn3search2 |
| **Morgon** | Villié-Morgon only. | Red only. | Gamay N principal. | Six culturally important named local sectors; no cellar method legally defines Morgon. | Existing INAO. | **regional-world major**. citeturn24view0turn1search16 |
| **Moulin-à-Vent** | Romanèche-Thorins and Chénas. | Red only. | Gamay N principal. | Cross-department geography and named-site tradition merit site-specific follow-up; no Nouveau. | Existing INAO. | **enhanced guide**. citeturn6search0 |
| **Régnié** | Régnié-Durette plus specified parcels in Lantignié. | Red only. | Gamay N principal. | Youngest cru recognition, 1988; partial-commune geography is a useful precision lesson. | Existing INAO. | **basic native guide**. citeturn14search14 |
| **Saint-Amour** | Saint-Amour-Bellevue. | Red only. | Gamay N principal. | Saône-et-Loire cru at northern edge; no need to center Valentine’s Day marketing. | Existing INAO. | **basic native guide**. citeturn3search6 |

All ten cru specifications should be ingested from their **current** legal texts before rules are surfaced beyond the robust common facts of red-only status, cru geography and Gamay’s principal role. The 2024 homologations are current for the crus reviewed here; INAO records subsequent EU communications for several in 2025-2026. citeturn24view0turn14search3

**Map overlap / click-priority recommendation**

The actual structure supports a **data-authored specificity priority**, with one important legal nuance.

At geographical-area level, the current Beaujolais legal area encompasses communes that also contain crus. The current Villages mention covers 38 northern communes, including several cru communes. INAO polygons represent regulatory geographical areas, not approved vineyard parcels, and current CARTA already has this distinction built into Atlas. citeturn17view0 fileciteturn6file0L2-L2

Recommended click priority:

> **cru > Beaujolais with Villages mention > Beaujolais**

This should mean “select the most specific useful mapped origin under the cursor,” not “declare that every square meter in the broad polygon is legally interchangeable or eligible for every designation.”

When a cru wins the click:

* retain Beaujolais as regional/legal context;
* retain Villages context where the mapped geometries actually overlap;
* visually de-emphasize rather than erase those broader outlines;
* disclose that displayed INAO geometry is regulatory geographical area, not approved parcel or planted vineyard;
* allow the learner to step back to the broader origin without losing viewport.

The priority belongs in release/editorial data exactly as Jura and Jurançon already established. No `if region === "Beaujolais"` branch is warranted. fileciteturn13file0L2-L2 fileciteturn14file0L2-L2

A further implementation correction is needed: the current map model may contain a separate `Beaujolais-Villages` geometry/identity inherited from INAO/source conventions, while current 2026 law treats Villages as a mention under Beaujolais. **Do not delete useful geometry. Reconcile legal identity and presentation aliasing.** That is a data/identity problem, not a frontend exception.

## Grapes, wine styles, cellar practice and historical change

**Gamay dossier**

**Identity and naming.** CARTA already uses `Gamay noir à jus blanc` as its human-facing grape identity, while current French legal texts use the code `gamay N`. These are naming contexts around the same principal Beaujolais cultivar, not separate grapes. The existing grape profile is currently only a navigation node and should be promoted to baseline before the regional world ships. fileciteturn10file0L2-L2

**Genetics.** Genetic research identifies Gamay noir among the important offspring of **Pinot × Gouais blanc**. Chardonnay is another independent offspring of the same parental varieties. The useful cross-region insight is therefore not merely that Gamay and Chardonnay happen to grow near one another: they share the same two parental varieties while developing very different regional histories. citeturn8search1

**Current Beaujolais role.** The official 2024 regional distribution was 96% Gamay and 4% Chardonnay. That is a dated planting/distribution measure, not a legal definition. Current Beaujolais law permits other accessory varieties in red/rosé within specified limits, while the ten crus center legally on Gamay. fileciteturn17file0L2-L2 citeturn19view1

**Viticultural traits.** The 2026 Beaujolais cahier explicitly discusses Gamay as sufficiently fertile that short pruning has historically been used to control production. Early budbreak/ripening and frost sensitivity are well-established ampelographic subjects but were not independently reconciled to a primary cultivar database during this run. Those additional traits should be sourced directly from VIVC/Plantgrape/INRAE before machine ingestion rather than copied from generic wine references. citeturn18view3

**Burgundy relationship.** The 1395 ordinance issued under Philip the Bold is historically real, but the mythology surrounding it is too tidy. Serious historical work indicates the action targeted Gamay in the duke’s territory amid quality, agricultural and economic concerns; enforcement faced resistance and later reiteration. The edict does **not** by itself prove that Gamay was simply expelled from “Burgundy” in the modern regional sense and transplanted to Beaujolais. citeturn7search3turn7search4turn7search6

**Misconceptions to correct in the native subject**

“Gamay tastes like Beaujolais Nouveau,” “Gamay requires carbonic maceration,” “Gamay is the only legal red grape anywhere in Beaujolais,” “Gamay moved to Beaujolais because of one 1395 ban,” and “one grape means one terroir expression” should all be explicitly rejected or narrowed.

**Cross-region opportunities**

The strongest is Gamay → 1395 historical event → Burgundy. A second, quieter route is Gamay genetics → Chardonnay → Burgundy, but it should only become a graph route if CARTA’s current relationship ontology can express the shared parentage without inventing an unsupported “similar wine” relationship.

**Chardonnay and other color/style routes**

Chardonnay deserves meaningful treatment, but as a **minority that reveals structure**, not as an obligatory “other grape” card.

The 2024 regional distribution places Chardonnay at 4%. More importantly, the current August 2026 Beaujolais specification makes Chardonnay B the **sole grape for white AOC Beaujolais**, while white is legally possible for Beaujolais with the Villages mention as part of that same specification. Red and rosé use Gamay N as principal grape with accessory varieties. fileciteturn17file0L2-L2 citeturn19view0turn19view1

This supports three learner payoffs:

1. The 96% Gamay figure describes plantings/distribution, not every legally possible wine.
2. Southern Beaujolais and its limestone-rich contexts make Chardonnay spatially legible instead of treating it as an anomaly.
3. Domaine des Terres Dorées gives a producer route that connects southern geography, Chardonnay, a non-carbonic red-wine cellar tradition and current succession/management change. The current estate description reports 9 ha of Chardonnay among its southern holdings. citeturn25search0

White Beaujolais therefore belongs in **Grapes & Wines** and **Place**, but not as a sixth Question Worth Following unless additional time-series evidence demonstrates a larger historical change.

Rosé matters primarily for legal literacy and Nouveau: current Beaujolais law allows rosé and permits `primeur`/`nouveau` for red and rosé, not white. citeturn19view0

**Beaujolais ↔ Burgundy through Chardonnay** is valid as a grape/place route, but the historical Gamay route has far more distinctive learner payoff. **Beaujolais ↔ Jura through Chardonnay** is currently weaker: the grape alone does not establish a compelling relationship, and CARTA should not force a route merely because both worlds contain Chardonnay.

**Nouveau / primeur historical dossier**

The current 2026 Beaujolais specification itself contains an unusually useful official historical narrative. It notes a pre-existing 19th-century practice in which early Beaujolais could move quickly to distributors and cafés/restaurants in Paris and Lyon. In 1951 the regional winegrowers sought permission to release wine before the general 15 December date; an administrative note dated 13 November 1951 provided the regulatory opening associated with the official birth of the modern Beaujolais Nouveau phenomenon. The consumer-release convention reached the **third Thursday of November in 1985**. citeturn18view2

| Period | Law / trade / culture | Finding | Atlas treatment |
|---|---|---|---|
| **19th century** | Trade practice | Early wines already moved rapidly toward urban distributors and hospitality in Lyon and Paris. | Culture context, not “Nouveau invented in 1951.” citeturn18view3 |
| **Postwar period** | Regulation | Producers sought earlier release than the general December date. | Rules + Time. |
| **13 Nov 1951** | Law | Administrative permission opened the modern regulated primeur phenomenon. | Timeline hinge. citeturn18view2 |
| **1960s onward** | Market | Volumes rose rapidly. | Trade/history. |
| **Mid-1980s** | Market | Current official specification reports about **500,000 hl**, while stating primeur never exceeded half of total Beaujolais production. | Then state. citeturn18view2 |
| **1985** | Law/culture | Consumer release standardized to the third Thursday of November. | Rules + IYKYK candidate. citeturn18view2 |
| **Current rule** | Law | Primeur/nouveau red or rosé; 2026 specification also revises inter-warehouse circulation timing around 35 days after harvest start, with an alternative tied to 38 days before the third Thursday. | Current Rules card, dated 2026. citeturn18view1turn20search1 |
| **Current regional scale** | Market/culture | Inter Beaujolais currently describes Nouveau as more than 20% of regional production and more than 160,000 hl annually. | Now state, explicitly current institutional estimate. citeturn1search0 |

**Market interpretation.** Nouveau was not a fringe gimmick. Its mid-1980s scale made it globally consequential while the official historical record itself makes clear it never represented the entire crop. That coexistence is much more useful than a “Nouveau destroyed the region” story. citeturn18view2

**Georges Duboeuf.** His commercial role in expanding Nouveau’s international visibility is historically significant enough to warrant eventual treatment, but this run did not secure a sufficiently strong first-party archival or independent specialist source set for a CARTA-grade candidate claim. Do not use Duboeuf as a load-bearing historical agent in the minimum release until that dossier is completed. This omission does not block the Nouveau timeline because the legal and volume history is independently strong.

**Reputational interpretation.** The defensible argument is that enormous awareness of Nouveau gave one particular early-release style unusual power over the category’s public identity. It is not defensible from the current evidence to say Nouveau alone caused later low prestige, or that the cru/natural-wine revival was a direct reaction to Nouveau.

**Verdict on the original “reputation inversion” question:** reject the proposed wording.

Best evidence-supported version:

> **How did a wine designed for release within weeks come to shape how the whole region was recognized?**

A sharper optional follow-up:

> **What gets hidden when one of Beaujolais’s most successful wines becomes shorthand for Beaujolais itself?**

That question has a real payoff: the learner moves from Nouveau law and volume into Morgon, Mont Brouilly, Gamay, producers and sites instead of being told that the reputation was simply “wrong.”

**Carbonic / semi-carbonic dossier**

These terms must be separated with more precision than normal wine shorthand allows.

**Carbonic maceration** involves intact grapes held in a carbon-dioxide-rich, oxygen-poor environment. Intracellular metabolism begins inside intact berries. OIV recognizes CO₂ atmosphere as central to the method; after the carbonic phase, pressing and conventional alcoholic fermentation can complete the process. citeturn11search0turn11search1

**Semi-carbonic maceration** typically does not require the tank to be filled with externally supplied CO₂. Whole clusters are loaded into the vessel; berries at the bottom can rupture under weight and begin yeast fermentation, producing CO₂ that changes the atmosphere around intact berries above. Some intracellular metabolism therefore occurs alongside ordinary yeast fermentation. It is related to carbonic maceration but not identical. citeturn11search10

**Whole-cluster fermentation** says something about whether stems and intact bunches enter the fermenter. It does not, by itself, tell the learner whether the ferment is truly carbonic or semi-carbonic.

**Intracellular fermentation/metabolism** is the berry-level anaerobic process occurring before the berry is conventionally crushed/pressed.

**Native fermentation** concerns the source/management of fermentative microorganisms. It is independent of whether clusters are whole or destemmed and independent of carbonic atmosphere.

**Added CO₂** is a process choice that helps distinguish intentionally established carbonic conditions from semi-carbonic environments generated by fermentation.

**Temperature, extraction and élevage** are additional independent dimensions. “Carbonic” does not tell a learner maceration length, extraction intensity, aging vessel or sulfur regime.

**Regional tradition.** The 2026 Beaujolais specification describes a Beaujolais vinification tradition “inspired by semi-carbonic maceration,” which is useful historical context, but this appears in the description linking product and geography rather than as a universal requirement that every qualifying wine undergo semi-carbonic fermentation. citeturn18view3

**Producer contrast**

* Lapierre currently describes whole bunches and semi-carbonic maceration, with indigenous yeast and a carefully qualified sulfur approach. fileciteturn11file0L2-L2
* Domaine de la Grand’Cour describes whole bunches entering CO₂-saturated tanks, a useful more explicitly carbonic producer example. citeturn13search0
* Terres Dorées provides the counterexample: its established red-wine method has included sorting, destemming/crushing and conventional yeast fermentation rather than the regional semi-carbonic shorthand. Current ownership/management change means practice claims must remain dated. citeturn25search13turn25search3

**Recommended Atlas treatment:** **glossary first, Culture/People second. Do not make this a sensory Tell.** The strongest learner lesson is that a familiar regional word is less universal than it sounds.

**Jules Chauvet dossier**

Chauvet belongs in CARTA as a **historical person whose significance exceeds one estate**.

He should be presented as a Beaujolais wine merchant and technically/scientifically engaged researcher and taster whose work included fermentation and sensory questions. A 1963 scientific publication involving Chauvet demonstrates substantive research activity around Beaujolais carbonic maceration and acid metabolism. That is strong evidence for technical engagement, not evidence that he invented carbonic maceration. citeturn11search4

His importance to the finished world is transmission:

* Marcel Lapierre’s first-party history directly describes Chauvet’s guidance around the 1981 change in the domaine’s farming/cellar approach. This is the strongest bilateral relationship currently available. fileciteturn11file0L2-L2
* Kermit Lynch’s Foillard material describes Foillard as following Chauvet’s teachings, which supports influence/adoption more safely than formal mentorship. citeturn12search9
* Lynch groups Lapierre, Foillard, Breton and Thévenet around Chauvet-associated methods, but that ecosystem-level history cannot create four separate mentorship edges automatically. fileciteturn12file0L2-L2

**Chronological treatment**

1. Chauvet’s professional and research work predates the better-known 1980s producer movement.
2. Scientific publication evidence shows technical engagement by the early 1960s. citeturn11search4
3. Lapierre identifies 1981 as a direct turning point under Chauvet’s guidance. fileciteturn11file0L2-L2
4. Later producers adopted or shared parts of a Chauvet-associated vocabulary, but transmission was not necessarily identical, bilateral or synchronous.

Avoid “father of natural wine,” “inventor of sulfur-free Beaujolais,” “mentor to every natural winemaker” and similar hagiographic formulations.

**Gang of Four reassessment**

The existing CARTA model is fundamentally correct and should be preserved. fileciteturn12file0L2-L2

**Genuinely evidenced**

Kermit Lynch identifies Marcel Lapierre, Jean Foillard, Guy Breton and Jean-Paul Thévenet as the four growers he grouped under the nickname and links the group to Chauvet-associated farming and cellar ideas. The current CARTA ecosystem appropriately records informal membership rather than a formal institutional identity. citeturn12search9

**Nickname / merchant framing**

“Gang of Four” is explicitly a Kermit Lynch framing. Attribution is part of the fact. The nickname should not be written as though the four formally constituted themselves under it or as though all Beaujolais producers use the term in the same way.

**What membership means**

It supports an ecosystem-level statement that these four became associated in an influential importer narrative around a shared period of Beaujolais practice change and a Chauvet-linked intellectual context.

**What it does not mean**

It does not establish identical cellar protocols, identical sulfur use, mutual friendship between every pair at every time, ownership relationships, collaborations, formal membership rules or direct mentorship from Chauvet to each person.

**Supportable direct relationships**

Marcel Lapierre → Jules Chauvet: direct guidance/influence, high confidence from Lapierre first party.

Foillard → Chauvet: influence/adoption of teachings, medium-high confidence from specialist importer.

The other producer-to-Chauvet and producer-to-producer edges should remain unasserted until independent evidence exists.

**Best Atlas use:** Culture route and historical ecosystem, not the primary definition of modern Beaujolais.

## People, localities, sites and cultural routes

**Producer teaching roster**

Five producers are sufficient for the first finished release. This is deliberately smaller than the candidate pool because each producer has a distinct job and defensible evidence.

| Producer | Base | Appellation/site context | Teaching job | Historical/cultural role | Spatial precision | Evidence strength | Recommended depth |
|---|---|---|---|---|---|---|---|
| **Domaine Marcel Lapierre** | Villié-Morgon | Morgon; broader Beaujolais; Côte du Py context | Chauvet transmission, semi-carbonic practice, sulfur precision, succession | Core low-intervention historical agent without turning into whole-region proxy | Municipality for map until exact base is re-verified | **Very high**, first party + INAO | **deep/native** |
| **Jean Foillard** | Villié-Morgon | Morgon; Côte du Py | Individualize one Gang member; demonstrate evidence conflicts around acreage/certification/mentorship | Major international natural-wine/cru reference | Municipality only initially | **Medium-high but conflicting on mutable facts** | **baseline/native** |
| **Château Thivin** | Odenas | Côte de Brouilly / Mont Brouilly | Canonical producer outside natural-wine cluster; terrain + continuity | Geoffray family since 1877, long multigenerational Côte de Brouilly reference | Municipality unless first-party address ingested | **High** for history/place | **baseline/native**. citeturn13search15 |
| **Domaine de la Grand’Cour / Famille Dutraive** | Fleurie | Fleurie, Grand’Cour, Chapelle des Bois, Champagne; Brouilly | Fleurie, carbonic cellar path, estate holdings vs purchased fruit, weather adaptation and family continuity | Connects low-intervention culture to a different producer history than Gang shorthand | Municipality initially | **Very high**, first party | **deep/native**. citeturn13search0turn13search4 |
| **Domaine des Terres Dorées** | Charnay | Southern Beaujolais; Beaujolais/white; several northern crus | Limestone south, Chardonnay, non-carbonic cellar counterexample, 2024 management transition | Essential counterweight to natural/cru-only story | **Exact public address available** | **High current institutional + operator source** | **deep/native**. citeturn25search0turn25search3 |

**Why not Breton and Thévenet in the first five?** They remain important Gang-of-Four members and should stay discoverable through the ecosystem, but including all four would spend scarce regional teaching space repeating the same network before CARTA has independent dossiers proving distinct jobs.

**Why not Yvon/Jules Métras in the first five?** They are culturally compelling, especially for Fleurie/Vauxrenard, named-site and succession stories, but source propagation and identity/succession ambiguity are precisely the hazards this run was asked to resolve. Their exclusion is an evidence-quality decision, not an assessment of importance.

**Why Thivin and Terres Dorées matter.** Without them, the regional story would effectively say that historical relevance culminates in natural wine. Thivin makes Mont Brouilly and long family continuity visible. Terres Dorées makes southern limestone, Chardonnay, destemming/non-carbonic practice and a contemporary management transition visible. citeturn13search15turn25search0turn25search3

**Producer dossiers**

**Domaine Marcel Lapierre**

**Identity and people:** family estate in Villié-Morgon. Estate history dates family presence to 1909. Marcel took over in 1973. The estate identifies 1981 as the turning point under Jules Chauvet’s guidance. Marcel died after the 2010 harvest; Mathieu had joined in 2004 and Camille in 2013; the siblings currently co-own/operate. fileciteturn11file0L2-L2

**Vineyards:** current domaine material reports 18 ha of Gamay, mainly Morgon with additional Beaujolais plots. That is an estate-wide present claim, not a site-by-site ownership map. fileciteturn11file0L2-L2

**Farming:** organic-principle cultivation since the 1980s; Ecocert certification since 2004. Keep those distinct. fileciteturn11file0L2-L2

**Cellar:** current first-party treatment includes hand harvest, whole bunches, semi-carbonic maceration, indigenous yeast, used-barrel completion/aging for Morgon and no filtration. Sulfur is minimized but not universally absent. `N` identifies no-added-sulfur bottling within the estate’s current code. fileciteturn11file0L2-L2

**Wine to know:** Domaine Marcel Lapierre Morgon, already modeled as a persistent wine identity.

**Cultural job:** most defensible direct bridge from Chauvet to the later low-intervention Beaujolais story.

**Unresolved:** parcel-level holdings by named site and exact cellar coordinate should remain unasserted. The existing CARTA run explicitly rejected hand-drawn/approximate parcel and winery geometry. fileciteturn11file0L2-L2

**Jean Foillard**

**Identity:** Morgon producer strongly associated with Côte du Py and the Gang-of-Four importer narrative. citeturn12search9

**Chronology:** public sources disagree on 1980, 1981 and 1982 as the establishment/takeover point. A 2025 independent profile gives 1981 and an initial 4 ha. This should not be “resolved” by averaging dates. citeturn12search3turn12search2

**Vineyard scale:** current public figures conflict materially. Kermit Lynch describes nearly 14 ha, while a 2025 report describes 23 ha. These may reflect different dates or operating scopes, but that explanation itself is not yet evidenced. **Omit a timeless estate-hectare number.** citeturn12search9turn12search3

**Farming:** 2025 reporting describes roughly 80% of plots under organic practice and explicitly complicates blanket certification claims. Do not write “certified organic estate.” citeturn12search3

**Chauvet:** Kermit Lynch says Foillard followed Chauvet’s teachings. Treat as `INFLUENCED_BY`, not proven direct mentorship. citeturn12search9

**Wine/site anchor:** Côte du Py is the useful anchor, but a cuvée/site association does not establish parcel ownership geometry.

**Fleurie fruit:** the run did not resolve vintage-specific estate/rented/purchased fruit claims to CARTA standard. Keep outside minimum profile.

**Cultural job:** demonstrate why individualizing a producer matters even after the Gang-of-Four ecosystem is known.

**Château Thivin**

**Identity/location:** historic Côte de Brouilly estate in Odenas on Mont Brouilly. First-party material presents the Geoffray family’s tenure from 1877 across six generations. citeturn13search15

**Teaching job:** Thivin is the strongest first-release counterweight to the idea that the only important modern Beaujolais lineage is Chauvet → natural wine. Its pedagogical strength is continuity: one estate makes Mont Brouilly, Côte de Brouilly, long family stewardship and conventional/canonical regional reputation visible at the same time.

**Terrain relationship:** much stronger than a generic “benchmark producer” card. Clicking Thivin should leave the learner able to see Mont Brouilly and Côte de Brouilly.

**Farming/cellar:** do not import generic current practice from merchants. The later profile should use current first-party technical pages before asserting certification, sulfur policy or a timeless recipe.

**Wines:** one representative Côte de Brouilly estate wine is sufficient for baseline. No need for full range.

**Succession:** family continuity is historically useful, but individual generational handoffs should be represented only where dates and roles are explicitly sourced.

**Domaine de la Grand’Cour / Famille Dutraive**

**Identity:** Fleurie estate. First-party material says Jean Dutraive bought the domaine in 1969; Jean-Louis joined his father in 1977 and took over in 1989. citeturn13search0turn13search4

**Holdings:** first-party material describes approximately 9 ha in Fleurie across Grand’Cour, Chapelle des Bois and Champagne, plus about 1.6 ha of Brouilly family property at Charentay/Vuril. These are source-described estate relationships, not permission to draw parcel polygons. citeturn13search0

**Cellar:** whole bunches are loaded without destemming/crushing into CO₂-saturated tanks; no sulfur is added at vatting and fermentation is native according to the current estate account. This makes Grand’Cour a better true carbonic teaching example than generic regional prose. citeturn13search0

**Adaptation and fruit sourcing:** major hail losses in 2016 and 2017 led Jean-Louis and children Lucas, Justin and Ophélie to buy grapes for separate family wines from selected parcels. This is an excellent CARTA case for separating estate vineyards from purchased fruit. citeturn13search0

**Cultural job:** Fleurie, family transition, environmental disruption, purchased-fruit honesty and cellar technique in one dossier.

**Domaine des Terres Dorées / Jean-Paul Brun / Domaines Roger Zannier**

**Identity and current status:** a major identity correction is required. From the 2024 harvest, Jean-Paul Brun entrusted operational management/development of Domaine des Terres Dorées at Charnay to Domaines Roger Zannier. Zannier’s September 2024 announcement says Brun would accompany the new operation for five years while concentrating on the wines. Therefore, “Jean-Paul Brun currently runs Domaine des Terres Dorées exactly as before” is stale. citeturn25search1turn25search3

**Base:** 565 Route d’Alix, 69380 Charnay, an exact current public visitor/business address. citeturn25search0

**Current vineyard picture:** Rhône Tourisme reports 57 ha total; 37 ha around the domaine with 25 ha Gamay, 9 ha Chardonnay, 2 ha Pinot Noir and 1 ha Roussanne; it separately reports 18 ha across Fleurie, Moulin-à-Vent, Brouilly and Morgon. Note that 37 + 18 does not equal 57. **Do not invent the disposition of the remaining 2 ha.** citeturn25search0

**Cellar history:** Jean-Paul Brun’s established red-wine approach has provided an important Beaujolais counterexample to semi-carbonic shorthand, including destemming/crushing and conventional fermentation in concrete for wines such as L’Ancien. Practice after the 2024 management transition should be treated as current only when the new operation confirms continuity. citeturn25search13turn25search3

**Wines:** L’Ancien, a representative Beaujolais Blanc/Chardonnay, and one cru are enough. Do not create a catalogue.

**Cultural job:** southern Beaujolais, Chardonnay, an alternative cellar script and a live transition in producer identity.

**Producer-base GIS register**

| Producer | Base locality | Exact / municipality / approximate | Evidence | Proposed point treatment | Vineyard confusion risk |
|---|---|---|---|---|---|
| Domaine Marcel Lapierre | Villié-Morgon | **Municipality** | First party and current CARTA. fileciteturn11file0L2-L2 | Municipality-level producer-base marker with honest precision. | **High** if marker is mistaken for Morgon holdings or Côte du Py parcels. |
| Jean Foillard | Villié-Morgon | **Municipality** | Specialist importer/current reporting. citeturn12search9turn12search3 | Municipality-level base until exact public production address is independently confirmed. | **High**, especially Côte du Py. |
| Château Thivin | Odenas | **Municipality** in minimum release | First-party estate location. citeturn13search15 | Odenas producer-base marker; refine to public cellar address only with direct source. | **High**, because Mont Brouilly/Côte de Brouilly holdings should not become the point. |
| Domaine de la Grand’Cour | Fleurie | **Municipality** | First-party estate material. citeturn13search0 | Fleurie base marker. | **High**, due multiple named Fleurie holdings and Brouilly property. |
| Domaine des Terres Dorées | Charnay | **Exact public business address** | Rhône Tourisme, current. citeturn25search0 | Exact-address producer-base point: 565 Route d’Alix. | **Very high**, because estate also controls/works vineyards across several crus. |
| Yvon Métras, research lead only | Bize, Vauxrenard | **Merchant-reported bottler location** | Current retailer bottle data. citeturn25search14turn25search17 | **Do not map in minimum release** until primary/strong independent confirmation. | **Extreme**, because famous Fleurie site names routinely get conflated with base. |

Every point should explicitly mean **cellar/production/business base**, never “the vineyard.”

**Commune and locality register**

| Locality | Proposed treatment | Why it earns a CARTA role |
|---|---|---|
| **Villié-Morgon** | Native place/locality | Entire Morgon legal geographical area; Lapierre and Foillard base context; Py hill route. citeturn24view0 |
| **Fleurie** | Native place/locality | Cru and commune coincide; Grand’Cour; strong named-site culture; terrain. citeturn14search3 |
| **Odenas** | Native locality if Thivin/Brouilly world is deepened | Château Thivin base plus Brouilly/Côte de Brouilly overlap around Mont Brouilly. citeturn2search0turn14search9 |
| **Charnay** | Native locality | Southern Beaujolais/Pierres Dorées and Terres Dorées/Chardonnay route. citeturn25search0 |
| **Chiroubles** | Native locality | Commune and cru coincide; useful high-hill comparison with Fleurie/Morgon. citeturn2search3 |
| **Vauxrenard** | Node initially | Useful western/higher landscape context and Métras research lead, but not essential until Métras authority improves. |
| **Romanèche-Thorins** | Native/basic locality | Moulin-à-Vent geography and Saône-et-Loire/northern edge orientation. citeturn6search0 |
| **Lantignié** | Node/basic | Beaujolais commune-name culture and partial Régnié overlap make it legally interesting. citeturn14search14turn20search15 |
| **Lyon** | Cross-region/cultural anchor, not “Beaujolais commune” | Durable historical market and hospitality relationship. citeturn1search2turn1search11 |

Do not create all 88 legal-area communes merely because the list exists.

**Site / lieu-dit register**

| Site | Type | Commune | Appellation | Evidence | Geometry availability | Recommended CARTA treatment |
|---|---|---|---|---|---|---|
| **Côte du Py** | Named wine site/slope associated with Py hill | Villié-Morgon | Morgon | INAO identifies Py hill; Inter Beaujolais identifies Côte du Py among six named Morgon lieux-dits. citeturn24view0turn1search16 | No defensible site polygon currently adopted by CARTA. | Keep existing site identity, **non-geometric unless authoritative site geometry is acquired**. Consider separate Py hill geographic-feature identity if useful. |
| **Corcelette** | Named Morgon lieu-dit | Villié-Morgon | Morgon | Inter Beaujolais official named-site list. citeturn1search16 | Not established. | Source-described site node; no polygon. |
| **Douby** | Named Morgon lieu-dit | Villié-Morgon | Morgon | Inter Beaujolais official list. citeturn1search16 | Not established. | Optional, only if needed for geology contrast. |
| **Les Charmes** | Named Morgon lieu-dit | Villié-Morgon | Morgon | Inter Beaujolais official list. citeturn1search16 | Not established. | Optional node. |
| **Grand’Cour** | Producer-held named Fleurie site | Fleurie | Fleurie | Domaine de la Grand’Cour first party. citeturn13search0 | Not established. | Source-described producer-site relationship, no polygon. |
| **Chapelle des Bois** | Named Fleurie site | Fleurie | Fleurie | Grand’Cour first party. citeturn13search0 | Not established. | Same. |
| **Champagne** | Named Fleurie site | Fleurie | Fleurie | Grand’Cour first party. citeturn13search0 | Not established. | Same; protect against confusion with Champagne region. |
| **Grille Midi** | Likely Fleurie named vineyard/lieu-dit | Fleurie | Fleurie | Recurs in Métras merchant material. citeturn25search4turn25search14 | **Not established.** | Lead only. Require official/cadastral plus wine-domain semantic reconciliation. |
| **La Madone** | Ambiguous landmark/site/cuvée naming | Fleurie | Fleurie | Fleurie landscape is strongly associated with the Madone/chapel; Métras uses the name in wine/site context. citeturn22search5turn25search4 | **Not established.** | Do not create a vineyard polygon. Resolve whether CARTA needs landmark, lieu-dit and wine identities separately. |
| **Mont Brouilly** | Physical hill | Odenas/Cercié/Quincié/Saint-Lager context | Brouilly + Côte de Brouilly | INAO. citeturn14search9turn2search0 | Terrain/basemap feature, not wine-site polygon. | `geographic_feature` candidate, highly recommended. |

**Cultural lenses**

| Lens | Recommendation | Exact proposed use | Evidence | Failure mode / limitation | Learner payoff |
|---|---|---|---|---|---|
| **The Tell** | **Do not use as a regional tasting Tell.** | Possible legal-literacy Tell: “A cru name tells you a more specific red Beaujolais origin; it does not tell you that the wine was carbonically fermented.” | INAO cru law + cellar evidence. citeturn24view0turn11search10 | Could become a dry law fact rather than a true recognition clue. | Useful only if UI needs a label-reading Tell. |
| **IYKYK** | **Strong** | `Gang of Four` is a Kermit Lynch nickname for Lapierre, Foillard, Breton and Thévenet, not an official producer organization or quality tier. | Kermit/CARTA ecosystem. fileciteturn12file0L2-L2 | Treating importer vocabulary as universal local self-description. | Translates insider shorthand without gatekeeping. |
| **IYKYK** | **Strong, producer-specific** | On Lapierre bottles, `N` is the estate’s current code for bottling without sulfur. | Lapierre first party. fileciteturn11file0L2-L2 | Must never be generalized to Beaujolais labels or “natural quality.” | Turns a house code into useful literacy. |
| **Same Energy** | **Hold, not first-release essential** | Beaujolais ↔ Jura as producer-led low-intervention cultures. | Some broad cultural parallels exist. | Too easy to become “cult natural wine regions are alike,” which ignores law, grapes, cellar traditions and independent historical development. | Use later only with a concrete mechanism. |
| **Then / Now** | **Strong** | Mid-1980s Nouveau: about 500,000 hl and a huge regional market presence. Now: official regional material reports >160,000 hl and >20% of production. | 2026 cahier + current Inter Beaujolais. citeturn18view2turn1search0 | These figures use different dates and should not be presented as a precise percentage decline calculation. | Makes category reputation visibly temporal. |
| **Then / Now** | **Strong, producer level** | Terres Dorées before/after the 2024 transfer of operational management to Domaines Roger Zannier, with Brun remaining involved for a stated transition period. | Zannier/Rhône Tourisme. citeturn25search0turn25search3 | Do not translate “entrusted operational management” into sale/retirement unless documented. | Shows succession as a living change rather than genealogy trivia. |

**Succession and temporal register**

| Date / period | Transition | Evidence status | Then / Now suitability |
|---|---|---|---|
| 1909 | Lapierre family history begins its Villié-Morgon estate story with Michel Lapierre’s arrival. | Strong first party. fileciteturn11file0L2-L2 | Context only. |
| 1973 | Marcel Lapierre takes over family business. | Strong first party. | Useful in Lapierre timeline. |
| 1981 | Lapierre identifies Chauvet-guided farming/cellar turn. | Strong first party. | Excellent producer-level hinge. |
| 2004 | Mathieu Lapierre joins. | Strong first party. | Succession build-up. |
| 2010 | Marcel dies after harvest. | Strong first party. | Major transition. |
| 2013 | Camille joins; current siblings co-own/operate. | Strong first party. | **Ready Then/Now.** |
| 1969 | Jean Dutraive purchases Grand’Cour. | Strong first party. citeturn13search0 | Context. |
| 1977 / 1989 | Jean-Louis Dutraive joins / takes over. | Strong first party. | **Ready.** |
| 2016-2017 | Hail losses contribute to purchased-fruit family projects involving next generation. | Strong first party. | Strong Time story, not pure succession. |
| 1981, provisional | Foillard takeover/start according to strongest current independent report; sources disagree. | **Contested date.** citeturn12search3turn12search2 | Not suitable until resolved. |
| 1988 | Yvon Métras first vinifications, according to repeating merchant sources. | Medium/lead. citeturn25search4 | Not yet. |
| 2014 | Jules Métras begins own winemaking identity according to merchants. | Medium/lead. citeturn25search15turn25search16 | Keep distinct identities; not yet a clean succession pair. |
| Harvest 2024 | Terres Dorées operational management/development entrusted to Domaines Roger Zannier; Brun to accompany transition for five years. | Strong current operator/institutional. citeturn25search0turn25search3 | **Excellent Then/Now.** |

**Cross-region rabbit-hole register**

| Rank | Beaujolais subject | Destination | Bridge | Important difference | Relationship type | Ready? |
|---|---|---|---|---|---|---|
| **1** | Gamay | Burgundy | 1395 ducal ordinance and longer Burgundy/Gamay history | A historical attempt to police a grape is not evidence of a clean migration into modern Beaujolais. | **Real historical-event route**, not Same Energy | **Ready after claim/event ingestion.** citeturn7search3turn7search4 |
| **2** | Gamay | Chardonnay → Burgundy | Both are Pinot × Gouais offspring | Shared parentage does not imply shared viticulture, wine style or regional identity. | **Real biological/genetic route** if ontology supports shared parentage | **Nearly ready.** citeturn8search1 |
| **3** | Southern Beaujolais / Chardonnay | Burgundy/Mâconnais | Chardonnay + geographic adjacency north of Beaujolais | Beaujolais white remains governed by Beaujolais law, not Burgundy law. | Geographic/grape route | **Ready at broad Burgundy level; Mâconnais native-depth depends on existing authority.** |
| **4** | Low-intervention producer culture | Jura | Producer agency, low-intervention international culture | Different grapes, different historical cellar scripts, different legal/reputation structures. | **Same Energy only** | **Not first-release ready.** |
| **5** | Chauvet/carbonic research | Other carbonic traditions | Technical mechanism | Same mechanism can exist without same geography or culture. | Practice route | **Future.** |

## Authority, evidence and acquisition registers

**Candidate claim register**

Candidate IDs below are intentionally new handoff IDs, not assertions that these records already exist.

| Candidate ID | Subject | Statement | Layer | Status | Confidence | Observed / valid time | Source IDs |
|---|---|---|---|---|---|---|---|
| `cand:beaujolais-legal-spec-2026` | `appellation:beaujolais` | The current Beaujolais AOC specification was homologated by order of 5 Aug 2026 and published 20 Aug 2026. | Reference/legal | supported | high | valid from Aug 2026 | `cand-source:beaujolais-cdc-2026` citeturn20search7 |
| `cand:beaujolais-villages-mention-2026` | `appellation:beaujolais` | The current specification defines `Villages` as a mention following the name Beaujolais. | Reference/legal | supported | high | 2026 | same. citeturn19view0 |
| `cand:beaujolais-current-geo-communes` | `appellation:beaujolais` | Current legal geographical area covers 77 Rhône and 11 Saône-et-Loire communes. | Reference/legal/geography | supported | high | 2026 | same. citeturn18view3 |
| `cand:beaujolais-villages-38-communes` | `appellation:beaujolais` | The Villages mention’s current area covers 38 communes. | Reference/legal | supported | high | 2026 | same. citeturn17view0 |
| `cand:beaujolais-colors-2026` | `appellation:beaujolais` | Beaujolais with or without Villages/commune provenance can be white, rosé or red. | Reference/legal | supported | high | 2026 | same. citeturn19view0 |
| `cand:beaujolais-primeur-colors-2026` | `appellation:beaujolais` | `primeur`/`nouveau` is reserved to red and rosé. | Reference/legal | supported | high | 2026 | same. citeturn19view0 |
| `cand:beaujolais-white-chardonnay-2026` | `appellation:beaujolais` | White Beaujolais is Chardonnay B only. | Reference/legal | supported | high | 2026 | same. citeturn19view1 |
| `cand:beaujolais-red-rose-encepagement-2026` | `appellation:beaujolais` | Gamay N is principal for red/rosé; specified accessory grapes are tightly proportioned. | Reference/legal | supported | high | 2026 | same. citeturn19view1 |
| `cand:beaujolais-physical-range-2026` | `place:beaujolais` | Legal-area description runs about 55 km north-south, 15-20 km east-west, approximately 180-550 m. | Reference/geography | supported | high | 2026 source | same. citeturn18view3 |
| `cand:beaujolais-geology-two-families` | `place:beaujolais` | Older Paleozoic formations dominate the northern geological family; younger Triassic/Jurassic sedimentary formations become important southward. | Reference/geology | supported | high | current legal text | same. citeturn18view3 |
| `cand:beaujolais-terroir-mosaic` | `place:beaujolais` | Regional terroir research distinguishes >300 soil variants related to about 15 major rock types. | Reference/geology | supported | high | study current by 2018/2020 | `source:beaujolais-terroirs` + candidate expanded terroir source. citeturn1search1 |
| `cand:nouveau-1951` | `appellation:beaujolais` / historical event | 13 Nov 1951 administrative action enabled early commercialization associated with modern Beaujolais Nouveau. | Reference/history/legal | supported | high | 1951 | 2026 cahier. citeturn18view2 |
| `cand:nouveau-third-thursday-1985` | same | Consumer release moved to third Thursday of November in 1985. | Reference/history/legal | supported | high | from 1985 | same. |
| `cand:nouveau-mid1980s-volume` | same | Nouveau/primeur volume reached about 500,000 hl in the mid-1980s and never exceeded half total Beaujolais production according to current specification history. | Reference/history | supported | high | mid-1980s | same. |
| `cand:nouveau-current-scale` | `place:beaujolais` | Current Inter Beaujolais material describes Nouveau at >20% of production and >160,000 hl annually. | Frontier/reference-context | supported | medium-high | current source, must carry observed_at | official regional Nouveau source. citeturn1search0 |
| `cand:gamay-parentage` | `grape:gamay-noir-a-jus-blanc` | Gamay noir is an offspring of Pinot × Gouais blanc. | Reference/ampelography | supported | high | durable | peer-reviewed genetics. citeturn8search1 |
| `cand:gamay-1395-event` | Gamay + candidate historical event | Philip the Bold’s 1395 ordinance targeted Gamay in ducal territory; it should not be represented as a simple one-step migration to Beaujolais. | Reference/history | supported with interpretive caution | high | 1395 | serious historical scholarship/reporting. citeturn7search3turn7search4 |
| `cand:carbonic-definition` | candidate practice | Carbonic maceration requires intact grapes in CO₂-rich anaerobic conditions and involves intracellular metabolism before conventional fermentation completion. | Reference/practice | supported | high | durable | OIV/AWRI. citeturn11search0turn11search10 |
| `cand:semi-carbonic-distinction` | candidate practice | Semi-carbonic fermentation can generate CO₂ from fermentation of crushed fruit at the vessel bottom, exposing intact berries above to intracellular metabolism. | Reference/practice | supported | high | durable | AWRI. citeturn11search10 |
| `cand:beaujolais-semi-carbonic-tradition-not-rule` | `place:beaujolais` | Current legal explanatory text describes a semi-carbonic-inspired regional tradition, but the specification does not make carbonic fermentation a universal appellation requirement. | Reference/legal interpretation | supported | high | 2026 | current cahier. citeturn18view3 |
| `cand:chauvet-technical-research` | `person:jules-chauvet` | Chauvet participated in published technical research on carbonic maceration/fermentation by the early 1960s. | Reference/history | supported | high | 1963 | scientific publication. citeturn11search4 |
| `cand:grandcour-history` | candidate producer | Domaine de la Grand’Cour was acquired by Jean Dutraive in 1969; Jean-Louis joined 1977 and took over 1989. | Reference/producer | supported | high | dated | first party. citeturn13search0 |
| `cand:grandcour-fruit-sourcing` | candidate producer | After severe 2016-17 hail, the Dutraive family developed wines using purchased grapes selected from outside the estate. | Reference/history/producer | supported | high | 2016 onward scoped | first party. citeturn13search0 |
| `cand:terres-dorees-management-2024` | candidate producer | From harvest 2024, operational management/development of Terres Dorées was entrusted to Domaines Roger Zannier, with Jean-Paul Brun remaining involved in a transition. | Reference/current producer | supported | high | from 2024 | Zannier + Rhône Tourisme. citeturn25search0turn25search3 |
| `cand:terres-dorees-base` | candidate producer | Current public business base is 565 Route d’Alix, Charnay. | Reference/geography | supported | high | observed 2026 | Rhône Tourisme. citeturn25search0 |
| `cand:foillard-start-1981` | candidate producer | Jean Foillard took over/began the estate in 1981 according to a 2025 independent account. | Reference/producer | **provisional** | medium | historical, contested | independent report. citeturn12search3 |
| `cand:foillard-acreage-conflict` | candidate producer | Current public hectare figures for Foillard materially conflict and should not be collapsed into one number. | Open/contradiction | contested | high | observed sources 2025-26 | multiple. citeturn12search3turn12search9 |

**Candidate relationship register**

| From | Predicate | To | Evidence | Status | Time scope | Notes |
|---|---|---|---|---|---|---|
| `place:beaujolais` | `CONTAINS / REGIONAL_CONTEXT_FOR` | ten cru appellations | INAO/Inter Beaujolais | supported | current | Use existing predicate semantics, do not invent legal polygon containment from region anchor. |
| `appellation:beaujolais` | `HAS_MENTION` candidate/current appropriate predicate | `Villages` legal mention | 2026 cahier | supported | current 2026 | Prefer name/legal assertion if ontology has no mention entity. |
| `grape:gamay-noir-a-jus-blanc` | `OFFSPRING_OF` | Pinot | genetics | supported | durable | Relationship form must match current grape ontology. citeturn8search1 |
| Gamay | `OFFSPRING_OF` | Gouais blanc | genetics | supported | durable | Same. |
| candidate 1395 historical event | `CONCERNS` | Gamay | scholarship | supported | 1395 | Do not encode “caused migration to Beaujolais.” |
| candidate 1395 event | `LOCATED_IN / GOVERNED_BY` | ducal Burgundy context | scholarship | supported | 1395 | Historical geography should not be replaced by modern Burgundy polygon. |
| Domaine Marcel Lapierre | `LOCATED_IN` | Villié-Morgon | first party | supported | current | Producer base, not vineyard. |
| Lapierre | `CLASSIFIED_AS` or producer/wine-specific existing predicate | Morgon | first party + INAO | supported | current wine identity | Existing CARTA relationship should be preserved. |
| Marcel Lapierre | `INFLUENCED_BY` / current supported guidance predicate | Jules Chauvet | first party | supported | circa 1981 | Do not upgrade automatically to formal mentorship. |
| Jean Foillard | `INFLUENCED_BY` | Jules Chauvet | Kermit Lynch | supported/provisional | early career | Safer than `MENTORED_BY`. |
| Lapierre / Foillard / Breton / Thévenet | `MEMBER_OF` | Gang-of-Four ecosystem | Kermit Lynch | supported | historical/informal | Existing ecosystem pattern. |
| Château Thivin | `LOCATED_IN` | Odenas | first party | supported | current | Base only. |
| Château Thivin | `ASSOCIATED_WITH_APPELLATION` | Côte de Brouilly | first party/legal | supported | current | Use existing producer/appellation predicate if available. |
| Grand’Cour | `LOCATED_IN` | Fleurie | first party | supported | current | Base only. |
| Grand’Cour | `FARMS / HOLDS_SITE` appropriate predicate | Grand’Cour / Chapelle des Bois / Champagne | first party | supported | source-described current/historical | Do not assert title/ownership unless source does. |
| Grand’Cour family project | `SOURCES_FRUIT_FROM` | outside estate parcels | first party | supported | post-2016 | Keep distinct from holdings. |
| Domaine des Terres Dorées | `LOCATED_IN` | Charnay | public current source | supported | current | Exact base coordinate may derive from address geocoding with disclosed provenance. |
| Domaines Roger Zannier | `OPERATES / MANAGES` | Domaine des Terres Dorées | operator source | supported | from harvest 2024 | Use closest existing predicate. |
| Jean-Paul Brun | `WORKS_WITH / TRANSITION_ROLE_AT` | Terres Dorées | operator source | supported | five-year transition announced 2024 | Do not infer retirement. |
| Yvon Métras | `PARENT_OF` | Jules Métras | widely corroborated | supportable once person identities exist | durable | Family relationship does not merge producers. |
| Jules Métras producer | `SUCCESSOR_OF` | Yvon Métras producer | current merchant claims only | **withhold** | unresolved | Relationship not ready. |

No relationship should be created for Beaujolais ↔ Jura “Same Energy.”

**Identity-resolution register**

| Ambiguity | Resolution |
|---|---|
| **Beaujolais region vs Beaujolais AOC** | Keep `place:beaujolais` semantic regional orientation separate from `appellation:beaujolais` legal identity. No region polygon. |
| **Beaujolais-Villages** | Current 2026 law places `Villages` under Beaujolais as a mention. Reconcile any existing separate CARTA/INAO presentation identity without destroying useful navigation. |
| **85 vs 88 communes** | 85 = dated 2024 “wine-growing communes” regional measure; 88 = current 2026 legal geographical-area commune count. |
| **Gamay noir à jus blanc vs Gamay N** | Same core cultivar in human/regulated naming contexts; `N` is French varietal-color notation, not a different grape. |
| **Gamay de Bouze / Gamay de Chaudenay** | Separate accessory cultivars named in current broad Beaujolais law, not synonyms of Gamay noir à jus blanc. citeturn19view1 |
| **Person vs domaine** | Marcel/Mathieu/Camille Lapierre remain people; Domaine Marcel Lapierre producer. Same principle for Jean-Paul Brun/Terres Dorées and Jean-Louis Dutraive/Grand’Cour. |
| **Parent vs child producer** | Yvon Métras and Jules Métras must remain separate producer/person identities unless evidence demonstrates legal/business merger. Alex Foillard similarly should not be folded into Jean Foillard merely because of parentage. |
| **Terres Dorées ownership/management** | “Entrusted operational management/development” to Zannier is not automatically equivalent to a documented asset sale; model exact source wording. citeturn25search3 |
| **Côte du Py** | Named wine site/slope associated with Py hill; not synonymous with Morgon, Villié-Morgon or the whole hill. |
| **La Madone** | Potentially chapel/landmark, local site vocabulary and cuvée/label usage. Resolve identities independently. |
| **Champagne in Fleurie** | Local site name, not Champagne wine region. UI requires kind/context display. |
| **Producer base vs vineyards** | Every proposed producer point is base/cellar/business location only. Never use it as holding centroid. |
| **Nouveau vs primeur** | Current Beaujolais specification permits the complementary wording `primeur` or `nouveau`; do not treat them as separate appellations. |
| **Nouveau vs all Beaujolais** | Nouveau is one regulated early-release path inside broad Beaujolais/Villages, not a synonym for regional wine. |
| **Gang of Four membership** | Informal ecosystem membership, not employer, association membership or pairwise collaboration. |

**Spatial / GIS acquisition register**

| Status | Dataset / knowledge | Treatment |
|---|---|---|
| **Already present in CARTA** | Current INAO AOC/AOP geography snapshot and external-ID mappings under `data/geography/` | Reuse. Do not redownload merely for this world. Current Atlas already documents that INAO geometry represents regulatory geographical area. fileciteturn6file0L2-L2 |
| **Already present** | Beaujolais regional orientation anchor derived from child appellation geometry | Reuse and derive fit bounds. Never replace with hand-authored regional polygon. fileciteturn8file0L2-L2 |
| **Needs reconciliation** | Beaujolais-Villages mapped identity vs 2026 legal `Villages` mention | Preserve geometry where useful, reconcile legal entity/name semantics and source version. |
| **Needs reconciliation** | Current 2026 Beaujolais legal area vs repository’s Aug 24, 2026 INAO geometry snapshot | Confirm snapshot already incorporates the August 2026 legal update before making current-rule claims from geometry. |
| **Needs acquisition only if existing administrative context is insufficient** | Selected commune/locality point geometry for Villié-Morgon, Fleurie, Odenas, Charnay, Chiroubles, Vauxrenard, Romanèche-Thorins | Use authoritative gazetteer/administrative sources; no need for all Beaujolais commune polygons. |
| **Needs acquisition / license check** | BRGM geological units useful at Beaujolais scale | Adopt only with dataset-specific provenance, licensing, scale and transformation manifest. |
| **Needs license confirmation before reuse** | Inter Beaujolais detailed terroir-map graphics/data | Strong research source; do not assume redistribution rights. |
| **Needs authoring from evidence** | Producer-base points | Use exact public address where available or municipality/approximate point with precision field. |
| **Should remain source-described only** | Côte du Py, Corcelette, Grand’Cour, Chapelle des Bois, Champagne until authoritative wine-site geometry exists | No guessed polygons. |
| **Lead only** | Grille Midi, La Madone geometry from name/cadastre matching | Name matching is insufficient. |
| **Terrain run responsibility** | DEM/hillshade/contours | **No acquisition here.** Consume whatever reusable terrain architecture lands separately. |

**Source ledger**

Access date for this research run: **2026-08-30**, unless an existing CARTA source record already carries 2026-08-29.

| Source | Publisher | Type | URL | Access date | Claims supported | Limitations |
|---|---|---|---|---|---|---|
| CARTA README | CARTA | Repository architecture | `https://github.com/thatssoreg/carta/blob/main/README.md` | 2026-08-30 | One authority, multiple projections, Atlas purpose | Project doctrine, not wine evidence. fileciteturn2file0L2-L2 |
| CARTA Architecture | CARTA | Repository architecture | `https://github.com/thatssoreg/carta/blob/main/docs/architecture.md` | 2026-08-30 | Spatial/temporal/relationship semantics | Internal contract. fileciteturn3file0L2-L2 |
| Human Reference Contract | CARTA | Repository architecture | `https://github.com/thatssoreg/carta/blob/main/docs/atlas-projection.md` | 2026-08-30 | Projection/native subject/lens constraints | Internal contract. fileciteturn4file0L2-L2 |
| Evidence Policy | CARTA | Repository policy | `https://github.com/thatssoreg/carta/blob/main/docs/evidence-policy.md` | 2026-08-30 | Conflict, trade-source and mentorship discipline | Internal policy. fileciteturn5file0L2-L2 |
| CARTA Atlas | CARTA | Product architecture | `https://github.com/thatssoreg/carta/blob/main/docs/carta-atlas.md` | 2026-08-30 | INAO geometry semantics; region anchors | Internal contract. fileciteturn6file0L2-L2 |
| Atlas Editorial Foundation | CARTA | Editorial doctrine | `https://github.com/thatssoreg/carta/blob/main/docs/atlas-editorial-foundation.md` | 2026-08-30 | Questions, lenses, regional thesis | Internal doctrine. fileciteturn7file0L2-L2 |
| Current Beaujolais Human Reference | CARTA | Existing projection | `https://github.com/thatssoreg/carta/blob/main/atlas/countries/france/regions/beaujolais.md` | 2026-08-30 | Baseline audit | Projection, not independent evidence. fileciteturn8file0L2-L2 |
| Current Lapierre profile | CARTA + first-party sources | Reconciled reference | `https://github.com/thatssoreg/carta/blob/main/atlas/producers/domaine-marcel-lapierre.md` | 2026-08-30 | Lapierre chronology, practice, certification, sulfur | Composite projection; source records remain authority. fileciteturn11file0L2-L2 |
| Gang of Four profile | CARTA | Reconciled ecosystem | `https://github.com/thatssoreg/carta/blob/main/atlas/ecosystems/gang-of-four-beaujolais.md` | 2026-08-30 | Nickname/community model | Relies heavily on Kermit Lynch framing. fileciteturn12file0L2-L2 |
| 2024 Beaujolais key figures | Inter Beaujolais | Primary institutional | `https://carnet.beaujolais.com/fr/` | CARTA source 2026-08-29 | 11,771 ha, 12-appellation institutional framing, 85 communes, 96/4 grapes, 94/4/2 colors | Snapshot dated 2024, not current law. fileciteturn19file0L2-L2 |
| 2026 Beaujolais cahier | French Ministry of Agriculture | Primary regulatory | `https://info.agriculture.gouv.fr/boagri/document_administratif-587d5ea5-ef21-44d1-ad87-80a5851ec807` | 2026-08-30 | Current Beaujolais/Villages identity, communes, grapes, colors, Nouveau law/history, physical/geological description | Legal explanatory sections may contain institutional historical interpretation in addition to operative rules. citeturn20search7turn17view0 |
| Homologation order, 5 Aug 2026 | Légifrance | Primary legal | `https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054673145` | 2026-08-30 | Current specification date and replacement of 2022 order | Order points to specification for substantive details. citeturn15view0 |
| Beaujolais terroir overview | Inter Beaujolais | Primary institutional | `https://www.beaujolais.com/2020/09/21/a-la-decouverte-des-terroirs-beaujolais/` | 2026-08-30 | Geological complexity | Detailed map reuse rights not established. citeturn1search3 |
| Terroir / premier-cru research summary | Inter Beaujolais | Primary institutional | Via cited Inter Beaujolais 2024 page | 2026-08-30 | 300+ soils, 15 rock types, ~600 lieux-dits, historical site mapping | Interprofessional perspective; legal classification proposals are not current law. citeturn1search1 |
| Morgon | INAO | Primary regulatory/institutional | `https://www.inao.gouv.fr/produit/morgon-ou-morgon-cru-du-beaujolais-18178` | 2026-08-30 | Villié-Morgon scope, Py hill, current 2024 spec link | Product prose contains sensory language Atlas should not convert into terroir fact. citeturn24view0 |
| Fleurie | INAO | Primary regulatory/institutional | `https://www.inao.gouv.fr/produit/fleurie-ou-fleurie-cru-du-beaujolais-16759` | 2026-08-30 | One-commune scope, slopes, spec date | Same sensory-prose caution. citeturn14search3 |
| Brouilly | INAO | Primary regulatory/institutional | `https://www.inao.gouv.fr/en/node/29117` | 2026-08-30 | Six communes, Mont Brouilly, spec date | Current legal text still required for detailed rules. citeturn14search9 |
| Régnié | INAO | Primary regulatory/institutional | `https://www.inao.gouv.fr/produit/regnie-ou-regnie-cru-du-beaujolais-17297` | 2026-08-30 | Régnié-Durette + Lantignié parcel scope, 1988 recognition | “Some parcels” requires parcel plan for geometry. citeturn14search14 |
| Beaujolais-Villages product page | INAO | Primary institutional presentation | `https://www.inao.gouv.fr/produit/beaujolais-villages-rouge-17214` | 2026-08-30 | Current public presentation of Villages | Public product naming is less legally precise than the current Beaujolais cahier. citeturn20search8 |
| Biology Letters Pinot/Gouais study | Royal Society / peer reviewed | Primary scientific | `https://doi.org/10.1098/rsbl.2009.0810` | 2026-08-30 | Gamay and Chardonnay parentage | Genetics does not imply stylistic similarity. citeturn8search1 |
| OIV carbonic definition | OIV | Primary institutional/scientific | `https://www.oiv.int/` | 2026-08-30 | Carbonic mechanism | Use exact OIV term/version during ingestion. citeturn11search0turn11search1 |
| AWRI carbonic technical material | Australian Wine Research Institute | Primary technical institution | Via cited AWRI page | 2026-08-30 | Carbonic vs semi-carbonic distinction | General winemaking source, not Beaujolais law. citeturn11search10 |
| Grand’Cour producer material | Domaine de la Grand’Cour | Primary producer | Via cited producer page | 2026-08-30 | History, holdings, carbonic practice, hail/purchased fruit | Producer self-report; mutable current details need dates. citeturn13search0turn13search4 |
| Château Thivin producer material | Château Thivin | Primary producer | `https://www.chateau-thivin.com/` | 2026-08-30 | 1877 Geoffray tenure, Mont Brouilly identity | Technical current farming/cellar claims should be fetched from specific first-party pages before ingestion. citeturn13search15 |
| Domaine des Terres Dorées | Rhône Tourisme | Public institutional/local tourism | `https://www.rhonetourisme.com/je-prepare/le-gourmand/nos-adresses-gourmandes/vente-a-la-ferme/139697_domaine-des-terres-dorees/` | 2026-08-30 | Current base, 2024 transition, present vineyard description | Current acreage description contains arithmetic gap: 37 + 18 ≠ 57. citeturn25search0 |
| Zannier transition announcement | Domaines Roger Zannier | Primary operator | `https://www.zannier.com/les-domaines-roger-zannier-investissent-le-beaujolais/` | 2026-08-30 | Operational-management transition and Brun’s continuing role | Corporate announcement, fit for transaction/role wording, not independent evaluation. citeturn25search3 |
| Yvon Métras retailer cluster | Multiple merchants | Trade/lead only | `https://www.petitescaves.com/collections/yvon-metras-beaujolais` | 2026-08-30 | Leads on Vauxrenard, Grille Midi, La Madone, 1988 | **Copy propagation risk.** Colorful identical wording and extreme vine-age claims recur. citeturn25search4 |
| Yvon Métras bottle/base listing | Lobenbergs | Trade | `https://www.gute-weine.de/produkt/yvon-metras-beaujolais-rouge-2023-75859h/` | 2026-08-30 | Bottler/base lead: Bize, Vauxrenard | Not sufficient for vineyard ownership or succession. citeturn25search14 |

**Merchant-copy propagation warning:** the Métras results show especially obvious propagation. Phrases about Yvon being “not much of a talker,” the 1988 start, Chauvet/Lapierre association, laboring soils and 1898 vines recur across merchants in nearly identical sequence. Treat these as one provenance family until an independent underlying source is identified. Foillard acreage and chronology show a different hazard: genuinely conflicting figures that may reflect source age/scope. CARTA’s evidence policy correctly forbids averaging them. fileciteturn5file0L2-L2

**Open questions**

| Question | Classification | Why it matters |
|---|---|---|
| Has the repository’s 2026-08-24 INAO geometry snapshot fully absorbed the 5 Aug 2026 Beaujolais specification and its Villages treatment? | **does not block implementation**, but must be reconciled before claiming geometry is current-law-perfect | Affects identity/version semantics, not regional thesis. |
| What are the exact current 2024 accessory-grape transitional provisions in each of the ten cru cahiers? | **does not block implementation** | Basic cru guides can ship on robust red/Gamay/geography facts; deeper Rules copy should wait. |
| Can Inter Beaujolais’s detailed terroir spatial material be legally redistributed or transformed? | **does not block implementation** | Narrative geology can ship without proprietary geometry. |
| Which BRGM dataset/scale best matches Atlas’s Beaujolais zoom and what are its exact reuse terms? | **does not block implementation** | Geology overlay is enrichment, not prerequisite. |
| What is Jean Foillard’s current operating-area scope, and why do 14/23 ha sources disagree? | **does not block implementation** | Omit acreage rather than block producer profile. |
| Is Foillard certified for any/all estate production, and on what dates? | **does not block implementation** | Current profile can state bounded organic-practice evidence only. |
| What was the exact bilateral nature of Foillard’s relationship with Chauvet? | **does not block implementation** | `INFLUENCED_BY` is already sufficient. |
| What is the current first-party status of Yvon Métras versus Jules Métras vineyards, labels and operational succession? | **does not block implementation** | Reason to exclude them from first producer roster. |
| Are Grille Midi and La Madone official wine-site identities with defensible geometry, and how do they correspond to cadastral names? | **Frontier/future research** | Non-geometric knowledge is sufficient initially. |
| What exact historical role did Georges Duboeuf play in Nouveau’s international commercialization, with archival/independent evidence? | **does not block implementation** | Would improve Nouveau history, but current legal timeline already works. |
| Which 2026 cru Premier Cru proposals, if any, have passed from producer/Inter Beaujolais study into a formal INAO legal stage? | **Frontier/current research** | Must not describe study/proposal as current classification. |
| Is there a robust regional time series for harvest dates, higher-elevation planting or white-Beaujolais growth? | **Frontier/future research** | Needed before publishing climate/altitude trend claims. |
| Is there a robust regional time series for organic certification/farming adoption? | **Frontier/future research** | Avoid anecdote-to-region generalization. |
| Can exact public cellar addresses be primary-sourced for Lapierre, Foillard, Thivin and Grand’Cour? | **does not block implementation** | Municipality-level points satisfy current Atlas contract. |

**No unresolved research question identified here blocks a bounded Beaujolais regional-world implementation.**

## Implementation and terrain handoff

**Implementation blueprint**

This is an expected later change set, not a repository modification.

**Machine authority**

Extend the repository’s current entity, claim, source, relationship and name records using the same conventions already in `data/`. Highest-priority ingest:

* current 2026 Beaujolais legal specification and explicit Villages-mention identity;
* current commune/geographical scope;
* Nouveau timeline and current circulation/release rules;
* Gamay genetics/history;
* carbonic/semi-carbonic practice definitions;
* selected producer claims and succession;
* Mont Brouilly/Py hill/site identity distinctions;
* new contradictions where this handoff found unresolved source conflicts.

Do not overwrite the dated 2024 96/4 and 94/4/2 records. They are valid historical observations.

**Human Reference**

Likely extend the existing Beaujolais region page, Morgon page, Gamay stub and Lapierre/Gang material through the current deterministic Human Reference generator. Promote Gamay to baseline. Create producer profiles only after the necessary machine records exist.

The existing files most clearly implicated are:

`atlas/countries/france/regions/beaujolais.md`  
`atlas/countries/france/appellations/morgon.md`  
`atlas/grapes/gamay-noir-a-jus-blanc.md`  
`atlas/producers/domaine-marcel-lapierre.md`  
`atlas/ecosystems/gang-of-four-beaujolais.md`

New profiles should follow whatever current path convention is present at implementation time rather than this handoff inventing filenames.

**Geography**

Reuse existing INAO geography manifests, mappings and geometry/assertion conventions under `data/geography/`. Reconcile current Beaujolais-Villages identity against the August 2026 specification. Add only wine-meaningful locality/geographic-feature authority.

Do not create a regional Beaujolais polygon.

**Producer bases**

Extend the reusable multi-region producer-point dataset/contract proven by the Béarn run. Exact address may be used for Terres Dorées. Municipality/approximate markers are preferable to fabricated precision for the other first-release producers. fileciteturn13file0L2-L2

**Atlas editorial release**

Follow the existing release inheritance convention in `data/atlas/`, extending the current live editorial release rather than editing a frontend-specific Beaujolais configuration. Expected data includes:

* `regional_world: true` for Beaujolais;
* hero kicker and thesis;
* five pillar copy blocks;
* four or five Questions Worth Following;
* producer roster;
* grape cards;
* Nouveau Then/Now;
* glossary;
* map-click priority;
* context return for Burgundy;
* site/place actions;
* terrain moments only through whatever common terrain contract lands.

The existing Run 06 release proves that map-click priority, glossary, context returns and region-specific pillar copy are already data-authored. fileciteturn14file0L2-L2

**Glossary/lenses**

Minimum:

`carbonic maceration`  
`semi-carbonic maceration`  
`whole cluster`  
`primeur / nouveau`

Cultural lenses:

IYKYK: Gang of Four  
IYKYK: Lapierre `N`  
Then / Now: Nouveau  
Then / Now: Terres Dorées transition

Do not ship a regional tasting Tell merely to satisfy lens symmetry.

**Questions Worth Following**

Bind each question to governed claims and native subjects. The Burgundy/1395 route requires a historical-event or equivalent claim-bearing subject before becoming clickable. No dead CTA.

**Tests**

Extend existing Atlas and navigation tests rather than creating a Beaujolais-only test harness.

At minimum validate:

* every 12-part regional navigation feature resolves, while strict legal identity for Villages remains correct;
* every current mapped AOC feature remains clickable;
* current Beaujolais/Villages/cru click priority is data-authored;
* every editorial sentence has valid claim IDs;
* every producer marker exposes precision/type;
* no marker is described as vineyard geometry;
* all glossary claims resolve to sources;
* all Questions Worth Following land on native subjects;
* context return restores Beaujolais viewport;
* Same Energy never becomes a false graph relationship;
* no unlicensed site/geology geometry enters generated assets;
* no current quantity lacks observation scope;
* current 2026 law does not overwrite 2024 statistical observations.

Existing `scripts/build_atlas.py`, `scripts/validate_atlas.py` and Atlas test suites should remain the generator/validator surfaces unless the repository convention has changed by implementation time. Current architecture expressly requires deterministic projection from machine authority. fileciteturn6file0L2-L2

**Browser acceptance**

Confirm desktop and phone behavior for:

* regional entry;
* Mont Brouilly legal overlap;
* Morgon/Côte du Py distinction;
* Gamay native exploration without changing viewport;
* producer Explore vs Go;
* Nouveau timeline/rule;
* carbonic glossary;
* Burgundy rabbit hole and reversible return;
* evidence drawer showing current 2026 law versus dated 2024 measurements.

**Terrain handoff**

**Beaujolais terrain bounds:** do not author numeric “region bounds” as a new spatial truth. Use the existing regional fit derived from the union of mapped Beaujolais child/legal features, plus the shared terrain system’s normal visual padding. This preserves the settled rule that Beaujolais is a semantic region, not an invented polygon.

**Desired terrain moments**

| Moment | Desired view | What terrain adds | What stays quiet |
|---|---|---|---|
| **Regional arrival** | Entire 55 km wine corridor, Saône east, Monts du Beaujolais west | Explains corridor form and east-west relief relationship | Do not exaggerate vertical relief or shade entire legal area as vineyard. |
| **Mont Brouilly** | Hill with Brouilly and Côte de Brouilly outlines | Best physical-versus-legal demonstration in the region | No “this exposure creates X flavor.” |
| **Morgon / Py** | Villié-Morgon, Py hill, Côte du Py label | Makes named site and hill legible inside one cru | Do not draw Côte du Py vineyard polygon without source. |
| **Fleurie / Chiroubles** | Neighboring slopes and vertical change | Shows why close legal origins can occupy different hill positions | No “higher = fresher.” |
| **Southern Charnay / Pierres Dorées** | Rolling southern terrain, less dramatic than crus | Prevents Atlas from visually equating “important terrain” with steep crus only | Terrain subordinate to geology/Chardonnay story. |
| **Saône context** | Pull east enough to retain plain/river orientation | Places Beaujolais in ordinary French geography | No hydrological causal wine claims without evidence. |

**Features/labels needing terrain context**

Mont Brouilly  
Py hill  
Côte du Py  
Fleurie  
Chiroubles  
Juliénas/Mont de Bessay  
Vauxrenard only if it enters producer/locality authority  
Saône plain  
Monts du Beaujolais

**Zoom behavior**

Region scale: terrain quiet, enough to establish western hills and eastern plain.

Cru scale: hillshade/contours may become more legible at Mont Brouilly, Morgon, Fleurie/Chiroubles.

Site scale: terrain can support named-site orientation, but no automatically inferred vineyard polygons.

Producer selection: terrain should not move merely because a producer is explored. `Explore` keeps context; explicit `Go there` may move to base geography.

**Terrain must never be used to imply:**

* altitude produces freshness;
* aspect dictates ripeness or taste;
* steepness proves quality;
* hill location proves vineyard ownership;
* a producer base marks vineyard land;
* a cru polygon represents planted vineyard;
* geological unit predicts aroma;
* a terrain-derived slope is a named climat;
* a vineyard’s cultural prestige is visible in elevation data.

**Build-readiness verdict**

# READY FOR BEAUJOLAIS IMPLEMENTATION

The minimum bounded implementation scope is:

1. Keep the existing five-pillar regional-world contract and current shared Atlas UI.
2. Replace the baseline Beaujolais editorial framing with the **one grape, many places, moving reputation** thesis.
3. Reconcile the current **August 2026 Beaujolais legal specification**, especially the legal status of `Villages`, against existing machine authority and geography.
4. Preserve 2024 statistics as dated observations: 96% Gamay, 4% Chardonnay; 94% red, 4% white, 2% rosé; 11,771 claimed hectares; 85 wine-growing communes. fileciteturn17file0L2-L2
5. Provide useful click surfaces for Beaujolais, Villages and all ten crus, with deep treatment concentrated on **Morgon, Côte de Brouilly, Fleurie, Beaujolais/Villages**, and enhanced treatment for Brouilly, Chiroubles and Moulin-à-Vent.
6. Promote **Gamay** from navigation stub to native baseline subject.
7. Add **Nouveau / primeur** as a Rules + Culture + Then/Now mechanism, using the 1951, 1985, mid-1980s and current evidence.
8. Add a precise **carbonic / semi-carbonic glossary** and producer contrast.
9. Add five producer anchors: **Lapierre, Foillard, Château Thivin, Grand’Cour/Dutraive, Terres Dorées**.
10. Map producer bases only at defensible precision.
11. Add Mont Brouilly and Py terrain moments through the shared terrain architecture after that run lands.
12. Add the **Gamay → 1395 ordinance → Burgundy** rabbit hole with reversible map context.
13. Leave Métras succession, detailed lieu-dit geometry, Duboeuf’s full historical dossier, region-wide climate trends and Premier Cru proposals as bounded follow-up research rather than blocking release.

No new frontend, region-specific schema or parallel truth store is needed.

**Recommended acceptance tour**

**Minute zero to one: enter the apparent simplicity.**  
The learner enters Beaujolais and sees the hero:

> **One grape · many places · a reputation still moving**

The map fits the wine corridor between the Monts du Beaujolais and Saône. A 2024 fact establishes the provocation: **96% Gamay**. The interface immediately asks: *How can one grape make the map more important, not less?* fileciteturn17file0L2-L2

**Minute one to two: let terrain break the hierarchy open.**  
The learner goes to **Mont Brouilly**. Terrain makes the hill legible. Brouilly and Côte de Brouilly remain simultaneously visible, but Côte de Brouilly wins the more specific click. The guide explains that the hill is a physical feature, the two colored outlines are legal geographical areas, and neither is a vineyard map. citeturn14search9turn2search0

This is the terrain moment and the first legal distinction.

**Minute two to three: move from cru to grape to producer.**  
The learner moves to **Morgon**, sees Villié-Morgon and Py hill, then explores Côte du Py as a named site without a fabricated polygon. They choose **Domaine Marcel Lapierre** while the map stays on Morgon. Lapierre’s story supplies a direct human mechanism: Marcel’s 1981 Chauvet-guided turn, later family succession, semi-carbonic cellar work and the distinction between minimized sulfur and “never uses sulfur.” fileciteturn11file0L2-L2

A glossary tap on **semi-carbonic** explains why whole clusters, carbonic maceration and semi-carbonic maceration are not synonyms.

**Minute three to four: invert the obvious reputation story.**  
The learner follows:

> **How did a wine designed for release within weeks come to shape how the whole region was recognized?**

A compact Then / Now sequence shows 1951 early-release permission, the 1985 third-Thursday convention, roughly 500,000 hl in the mid-1980s, and the current smaller but still substantial Nouveau role. The lesson explicitly states that official history says primeur never exceeded half of total production. citeturn18view2turn1search0

From there, one producer comparison prevents a false conclusion: Grand’Cour can show a CO₂-saturated whole-bunch approach, while Terres Dorées demonstrates that Beaujolais is not legally or culturally trapped inside one cellar protocol. citeturn13search0turn25search13

**Minute four to five: leave the region without losing it.**  
The learner returns to **Gamay** and chooses:

> **What did the 1395 Gamay ordinance actually change, and what did it not?**

Atlas preserves the Beaujolais exploration trail but moves explicitly to **Burgundy**. The historical event corrects the standard banishment myth: Philip the Bold’s ordinance was real, but the later geography of Gamay cannot be reduced to one royal command. citeturn7search3turn7search4turn7search6

A visible context return then offers:

> **Back to Gamay in Beaujolais**

The viewport, active regional subject and exploration trail restore rather than reset.

That five-minute journey demonstrates the finished world’s argument: **Beaujolais becomes more interesting, not less, when Gamay stops being the answer and becomes the thread connecting place, law, cellar, markets, people and time.**