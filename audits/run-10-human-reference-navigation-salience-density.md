# CARTA Run 10 — Human Reference navigation salience and graph-density audit

## 1. Executive finding

**CARTA currently produces good rabbit holes when the governing path is direct, explicitly anchored, geographically directional, or professionally specific. It does not produce consistently good rabbit holes once a broad country, broad grape, or national classification becomes the only two-hop explanation.**

The machine graph remains technically coherent. The reader projection is beginning to overstate weak adjacency.

This is a concentrated but real product problem:

- 160 Human Reference profiles have reader-facing surfaces.
- They produce 1,024 directed candidate-profile pairs and 985 displayed links.
- Mean / median / p95 candidate counts are 6.4 / 5 / 14.
- Five profiles (3.12%) hit and exceed the 16-link cap: France (46 candidates), United States (22), Aurélien & Charlotte Houillon (17), Jura (17), and Spain (17).
- 46.29% of all displayed links have a shortest governed graph distance of two; among displayed graph-reachable links at distance one or two, 62.81% are two-hop.
- In the 28-page, 257-link human review, 103 links were A, six B, 76 C, 28 D, and 44 E. A/B therefore account for 42.41%; D/E account for 28.02%.
- D/E rates differ materially by reader job: grape 6.98%, country 15.79%, producer 36.00%, appellation 38.46%, and region 41.07%.

The central failure modes are inspectable:

1. `region/appellation → France → sibling region/appellation` turns shared country into apparent subject relevance;
2. composite `producer → component wine → broad grape/classification → component wine → producer` collapses to a permitted two-edge profile path and creates unrelated producer adjacency;
3. `country_entity_ids` is unioned with editorial anchors, so every producer's structural country assignment becomes a reciprocal country-page recommendation;
4. alphabetical title is the final decision-maker inside broad semantic buckets;
5. ranking cannot remove noisy candidates from profiles that remain below the cap.

The smallest justified Run 11 change is **an explicit profile-kind-aware two-hop eligibility policy plus separate projection treatment for `country_entity_ids` and `representative_anchor_ids`**. Direct relationships and explicit anchors should remain. Broad hub authority should remain. Numeric predicate weights and global degree penalties should not be the first production change.

Run 10 does not change production navigation or STRATA v0.2.

## Starting state

- Repository: `thatssoreg/carta`
- Canonical branch inspected: `main`
- Starting SHA: `0cd35464018768199cf9fcb2a79ac57a13805ede`
- Commit: `Merge Lampyres Matassa professional bridge`
- Fresh checkout state before the audit branch: clean, `main...origin/main`, with local `HEAD` and `origin/main` at the same SHA
- Audit branch: `run-10-human-reference-navigation-salience-density`

The user-supplied older checkout at `/Users/alionheart/Documents/carta` was not modified: it was stale at `ee49ef64465ce5fe022cf9c6715257dca86e853d` and contained unrelated untracked files. A fresh checkout was used to reconstruct actual GitHub main without disturbing that state.

### Required Lampyres / Matassa gate

The starting condition is satisfied:

- the reconciled `producer:domaine-lampyres`, `person:francois-xavier-daure`, and Harvest Moon world is present;
- `producer:matassa` and `person:tom-lubbe` are present;
- `person:francois-xavier-daure WORKED_FOR producer:matassa` is supported by `rel:daure-worked-for-matassa` for the 2015–2019 vintage span;
- Matassa has an honest `node/stub` profile;
- generated Lampyres navigation links to Matassa without either profile naming the other as a representative anchor.

## 2. Current navigation architecture

Production behavior is established from `scripts/validate_data.py`, not inferred from Markdown output.

### Eligible predicates

Only supported or provisional Reference relationships with one of these predicates enter the navigation graph:

`CLASSIFIED_AS`, `COLLABORATED_WITH`, `FARMED_BY`, `FARMS_IN`, `FARMS_PARCEL`, `FOUNDED`, `LOCATED_IN`, `MADE_BY`, `MADE_FROM`, `MEMBER_OF`, `MENTORED_BY`, `OWNED_BY`, `PLANTED_AT`, `TRAINED_AT`, `USES_PRACTICE`, `WITHIN`, `WITHIN_APPELLATION`, `WORKED_FOR`, and `WORKED_WITH`.

The graph is made undirected for discovery only. This does not create inverse machine authority.

### Distance and candidate generation

- Maximum relationship distance: two.
- A profile starts graph traversal from all `component_entity_ids`.
- `country_entity_ids` and `representative_anchor_ids` are unioned into one navigation-seed set.
- A target surfaced profile becomes eligible when any of these is true:
  1. a current navigation seed is a target component (`curated_outbound`);
  2. a current component is a target navigation seed (`curated_reciprocal`);
  3. a permitted graph path of distance zero, one, or two connects the component sets.
- A profile can therefore be anchor-eligible without any relationship path.
- Composite profiles shorten apparent traversal. If each producer profile includes its wine, `wine A MADE_FROM Syrah` and `wine B MADE_FROM Syrah` is a two-edge profile-to-profile path even though the reader experiences producer-to-producer adjacency.

### Ranking and sorting

The production tuple is:

1. outbound anchor, rank 0;
2. reciprocal anchor, rank 1;
3. otherwise `2 + graph distance` (shared component 2, direct relationship 3, two-hop 4);
4. graph distance, with no graph path sorted as 99;
5. title, case-insensitive alphabetical;
6. profile ID.

The algorithm is already direct-first **inside the graph-only bucket**. It is not direct-first across anchors: any outbound or reciprocal anchor outranks any direct relationship.

No predicate, path multiplicity, hub degree, confidence distinction between supported/provisional, target kind, source kind, or relationship specificity changes rank.

### Cap, publication, and duplicate behavior

- Maximum displayed related profiles: 16.
- Linkable targets: `published`, `stub`, and `queued` profiles with a path.
- `machine_only` profiles are never link targets, but their component entities may still be graph intermediaries.
- Machine-only editorial anchors are rendered as deferred plain text.
- The target-profile loop yields one candidate record per target profile. Multiple paths do not duplicate the target and do not increase its rank.
- The relationship adjacency graph itself collapses parallel edges to a neighbor set for shortest-distance calculation.
- The audit tool separately enumerates relationship-record paths so path multiplicity and predicate patterns remain measurable.

### Representative anchors

`representative_anchor_ids` is effective editorial projection authority:

- outbound anchors receive the strongest rank;
- the target page discovers the source reciprocally at the second rank;
- no typed relationship is required;
- an anchor can point to a component nested in a composite profile.

The problem is not representative anchors themselves. The problem is that `country_entity_ids`, which is structural placement metadata, receives identical projection semantics. A producer's country assignment thereby acts like an editorial recommendation from the country page.

### Profile-kind semantics

`profile_kind` validates primary-entity compatibility and canonical path placement. It does **not** change navigation eligibility, traversal, ranking, cap allocation, or rendering. Countries, grapes, producers, regions, appellations, classifications, and ecosystems all run through the same candidate and sort function.

## 3. Graph-density metrics

Normal authority counts at the starting SHA are:

`entities=505, relationships=524, claims=396, sources=292, names=33, spatial=34, profiles=183`

Of 183 governed profiles, 160 are surfaced and 23 are non-linkable dispositions. Of 524 relationships, 486 are eligible navigation records.

### Overall reader-candidate graph

| Metric | Result |
|---|---:|
| Surfaced profiles | 160 |
| Directed candidate-profile pairs after profile deduplication | 1,024 |
| Displayed links | 985 |
| Mean / median / p95 candidates | 6.4 / 5 / 14 |
| Maximum candidates | 46 (France) |
| Profiles at the cap | 5 (3.12%) |
| Profiles with actual displacement (`candidates > 16`) | 5 (3.12%) |
| Displayed shortest distance 0 | 8 (0.81%) |
| Displayed shortest distance 1 | 270 (27.41%) |
| Displayed shortest distance 2 | 456 (46.29%) |
| Displayed anchor-only / no graph path | 251 (25.48%) |

Production's winning-route classification differs because anchors override graph distance:

| Winning production route | Links | Percent |
|---|---:|---:|
| Outbound anchor | 377 | 38.27% |
| Reciprocal anchor | 211 | 21.42% |
| Shared component | 6 | 0.61% |
| Direct relationship | 34 | 3.45% |
| Two-hop relationship | 357 | 36.24% |

Among graph-only winners, 91.30% are two-hop rather than direct (357 versus 34). Across every displayed link that has a shortest relationship distance of one or two, 62.81% are two-hop (456 of 726).

### Candidate growth by profile kind

| Kind | Profiles | Mean candidates | Median | p95 | Max | Mean direct | Mean two-hop | Saturated / displaced |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Appellation | 28 | 6.25 | 5 | 13 | 14 | 1.39 | 3.25 | 0 / 0 |
| Classification | 2 | 9.00 | 9 | 13 | 13 | 4.00 | 3.00 | 0 / 0 |
| Country | 9 | 13.56 | 10 | 46 | 46 | 2.33 | 3.00 | 3 / 3 |
| Ecosystem | 2 | 6.00 | 6 | 7 | 7 | 0 | 0 | 0 / 0 |
| Grape | 36 | 4.22 | 3 | 12 | 12 | 1.67 | 1.25 | 0 / 0 |
| Landscape | 1 | 2.00 | 2 | 2 | 2 | 0 | 0 | 0 / 0 |
| Producer | 58 | 6.64 | 7 | 12 | 17 | 1.76 | 3.52 | 1 / 1 |
| Region | 24 | 6.58 | 5 | 14 | 17 | 1.67 | 3.79 | 1 / 1 |

Country candidate growth is the clearest cap problem. Region and producer sets are smaller, but human review shows that salience can fail well before the cap.

### Saturated profiles

| Profile | Kind | Candidates | Displayed | Displaced |
|---|---|---:|---:|---:|
| France | Country | 46 | 16 | 30 |
| United States | Country | 22 | 16 | 6 |
| Aurélien & Charlotte Houillon | Producer | 17 | 16 | 1 |
| Jura | Region | 17 | 16 | 1 |
| Spain | Country | 17 | 16 | 1 |

## 4. Hub analysis

### Highest-degree eligible entities

| Entity | Type | Eligible degree |
|---|---|---:|
| France | Place | 13 |
| California | Place | 10 |
| Chardonnay | Grape | 7 |
| Riesling | Grape | 7 |
| Clos Apalta Domaine | Project | 7 |
| Bassi Vineyard | Vineyard | 7 |
| Vin de France | Classification | 6 |
| Cabernet Sauvignon | Grape | 6 |
| Palomino Fino | Grape | 6 |
| Syrah | Grape | 6 |

### Most frequent two-hop intermediaries

| Intermediary | Directed profile pairs | Relationship-record path instances | Dominant source → target kind |
|---|---:|---:|---|
| France | 72 | 72 | region/appellation ↔ region/appellation |
| California | 30 | 40 | region/appellation/country geography pairs |
| Vin de France | 30 | 30 | producer → producer |
| Syrah | 30 | 30 | producer → producer |
| Chardonnay | 20 | 50 | producer → producer |
| Riesling | 12 | 34 | producer → producer |
| Garnacha Tinta | 12 | 26 | producer → producer |
| Cabernet Sauvignon | 12 | 24 | producer → producer |
| Pinot Noir | 12 | 18 | producer → producer |
| Napa Valley AVA | 12 | 12 | producer/geography pairs |

The superhubs are not interchangeable:

- France creates exactly 72 directed peer-geography pairs: 12 region→region, 20 region→appellation, 20 appellation→region, and 20 appellation→appellation.
- Vin de France and the listed broad grapes create producer→producer pairs.
- California creates both valid descendant navigation and invalid up-then-down sibling navigation, so degree alone cannot decide what to suppress.
- Pinot Noir is `machine_only`, but its entity remains an eligible intermediary and creates 12 directed producer pairs. Machine-only target suppression does not prevent graph influence.

These are superhubs by projection effect. Their authority is not wrong and should not be deleted.

### Highest-degree surfaced profiles and most frequent recommendations

Because the candidate relation is nearly reciprocal and most pages remain below cap, surfaced candidate degree and recommendation frequency are similar. The cap creates the small differences.

| Profile | Candidate profiles | Times displayed as a recommendation |
|---|---:|---:|
| France | 46 | 46 |
| United States | 22 | 22 |
| Spain | 17 | 17 |
| Jura | 17 | 17 |
| Aurélien & Charlotte Houillon | 17 | 17 |
| JONATA | 15 | 15 |
| Portugal | 14 | 14 |
| California | 14 | 14 |
| Jurançon | 14 | 14 |
| Loire Valley | 14 | 14 |
| Côtes du Rhône | 13 | 13 |
| Vin de France | 13 | 12 |

## 5. Human salience sample

The sample contains 28 surfaced pages and every one of their 257 displayed links. It covers five countries, seven region/appellation surfaces, six surfaced grapes, and ten producers. Pinot Noir was explicitly checked but cannot be sampled as a page because `profile:pinot-noir-disposition` is `machine_only`; its intermediary effect is audited separately. CARTA currently has zero surfaced standalone `wine` profiles, so wine-page semantics cannot be empirically scored in this run.

### Rating distribution

| Rating | Links | Percent |
|---|---:|---:|
| A — essential orientation | 103 | 40.08% |
| B — strong explanatory connection | 6 | 2.33% |
| C — useful expansion | 76 | 29.57% |
| D — technically connected, low-salience | 28 | 10.89% |
| E — distracting / misleading | 44 | 17.12% |

### Every displayed neighbor classified

| Page | A | B | C | D | E |
|---|---|---|---|---|---|
| France | Jurançon; Béarn; Irouléguy; Pacherenc du Vic-Bilh; Beaujolais; Cornas; Côte-Rôtie; Côtes du Rhône; Jura; Loire Valley; Palette; Savoie; Arbois | — | Richard Leroy | Aurélien & Charlotte Houillon; Château Simone | — |
| United States | California; Napa Valley; Columbia Gorge; Contra Costa County; Santa Barbara County; Santa Ynez Valley; St. Helena; Ballard Canyon; Petaluma Gap | — | — | Arnot-Roberts; Ashes & Diamonds; Burgess; Corison; Hiyu; JONATA; Pax | — |
| Germany | Mosel; Rheinhessen; Saar; Kabinett; Riesling | — | Keller; Falkenstein; Wasenhaus; A.J. Adam; Günther Steinmetz | — | — |
| Switzerland | — | — | Château d'Auvernier | — | — |
| Portugal | Azores; Lima Valley; Porto Santo; Madeira; Pico DOP; Madeirense DOP | — | Arinto dos Açores; Loureiro; Aphros; Maçanita; Profetas e Villões; Eruptio; Natus Vini; Trincadeira | — | — |
| Loire Valley | France; Menu Pineau | — | Clos du Tue-Boeuf; Vin de France; Bergerie; Le Grand Cléré | — | Beaujolais; Cornas; Côte-Rôtie; Côtes du Rhône; Jura; Jurançon; Palette; Savoie |
| Jura | Arbois; France; Chardonnay; Savagnin | — | Labet; Tournelle; Overnoy; Bruyère-Houillon; Saint Pierre | — | Beaujolais; Cornas; Côte-Rôtie; Côtes du Rhône; Jurançon; Loire; Palette |
| Savoie | France; Combe de Savoie | — | Carrel & Senger; Chevillard | — | Beaujolais; Cornas; Côte-Rôtie; Côtes du Rhône; Jura; Jurançon; Loire; Palette |
| Côtes du Rhône | France; Houillon; Guillaume Gilles; Syrah | — | Cornas; Côte-Rôtie | Vin de France | Beaujolais; Jura; Jurançon; Loire; Palette; Savoie |
| California | United States; Contra Costa; Napa; Santa Barbara; Santa Ynez; St. Helena; Ballard Canyon | — | Burgess; Pax; Ashes & Diamonds; Corison; Phelan; Sandhi; Soleras del Pacífico | — | — |
| Napa Valley | Corison; Cabernet Sauvignon; Burgess; California; St. Helena | — | United States; Ashes & Diamonds; Cabernet Franc | — | Contra Costa; Santa Barbara; Santa Ynez |
| Vin de Savoie Apremont | France | — | Chevillard | — | — |
| Syrah | — | — | Arnot-Roberts; Houillon; Chambeyron-Manin; Gilles; JONATA; Pax; Dureza; Vindiou; Côtes du Rhône; Petaluma Gap | Cabernet Sauvignon; Vin de France | — |
| Riesling | Rheinhessen; Saar; Wachau; Kabinett; Germany | — | Falkenstein; Keller; Rudi Pichler; A.J. Adam | — | — |
| Mourvèdre | — | — | Lampyres; Bébian; Sandhi | Vin de France | — |
| Savagnin | Jura; Arbois | — | Tournelle; Labet; Saint Pierre; Chardonnay | — | — |
| Chardonnay | Jura; Arbois; Chablis Grand Cru | — | Saint Pierre; Labet; Louis Michel; Scar of the Sea; Hiyu; Columbia Gorge; SLO Coast; Savagnin | — | — |
| Aligoté | — | — | Numa Cornut | — | — |
| Domaine Lampyres | Mourvèdre; Vin de France; France | Matassa | — | Houillon; Bébian; Sandhi | Bodegas Muga; Clos du Tue-Boeuf; Le Grand Cléré; Vindiou |
| Matassa | France | Lampyres | — | — | — |
| Domaine Labet | Chardonnay; Savagnin; France; Jura | — | Tournelle; Saint Pierre; Hiyu | Louis Michel; Scar of the Sea | — |
| Aurélien & Charlotte Houillon | Côtes du Rhône; Syrah; Vin de France; France | Overnoy; Bruyère-Houillon | Chambeyron-Manin; Gilles | Arnot-Roberts; JONATA; Pax; Lampyres; Bébian | Muga; Clos du Tue-Boeuf; Le Grand Cléré |
| Günther Steinmetz | Mosel; Germany | — | — | Château d'Auvernier; Hiyu; Wasenhaus | — |
| Burgess | Cabernet Sauvignon; Napa; California; United States | — | Ashes & Diamonds; Corison | Clos Apalta; JONATA | — |
| COS | Italy | — | — | — | — |
| Casa Coste Piane | Glera; Italy | — | — | — | — |
| Imanol Garay | France; Spain; Petit Courbu; Petit Manseng; Raffiat; Bizkaia; Bizkaiko Txakolina; Gros Manseng; Irouléguy; Pyrenean Atlantic | Alfredo Egia; Richard Leroy | — | — | — |
| Clos du Tue-Boeuf | Menu Pineau; Vin de France; Loire; France | — | — | — | Houillon; Lampyres; Le Grand Cléré; Bébian; Vindiou |

### Why every D/E link appeared

| Page | Rating | Links | Exact projection cause |
|---|---|---|---|
| France | D | Houillon; Château Simone | Reciprocal country anchors; no country-page rule explains why they should outrank 30 displaced French surfaces. |
| United States | D | Arnot-Roberts; Ashes & Diamonds; Burgess; Corison; Hiyu; JONATA; Pax | Identical reciprocal `country_entity_ids`; alphabetical title selects producers over internal geography. |
| Loire | E | Beaujolais; Cornas; Côte-Rôtie; Côtes du Rhône; Jura; Jurançon; Palette; Savoie | `Loire WITHIN France` followed by target `WITHIN/LOCATED_IN France`. |
| Jura | E | Beaujolais; Cornas; Côte-Rôtie; Côtes du Rhône; Jurançon; Loire; Palette | Shared France intermediary; alphabetical peers display while Savoie is displaced. |
| Savoie | E | Beaujolais; Cornas; Côte-Rôtie; Côtes du Rhône; Jura; Jurançon; Loire; Palette | Shared France intermediary with no more specific connection. |
| Côtes du Rhône | D | Vin de France | One wine carries both classifications across time; the generator exposes no context. |
| Côtes du Rhône | E | Beaujolais; Jura; Jurançon; Loire; Palette; Savoie | Shared France intermediary only. |
| Napa | E | Contra Costa; Santa Barbara; Santa Ynez | Napa→California→sibling place/appellation; alphabetization outranks St. Helena. |
| Syrah | D | Cabernet Sauvignon | A represented blend contains both grapes; one co-occurring wine becomes a general grape adjacency. |
| Syrah | D | Vin de France | One Syrah wine is classified under the national class. |
| Mourvèdre | D | Vin de France | One or more Mourvèdre wines use the broad national class. |
| Lampyres | D | Houillon; Bébian; Sandhi | Shared grape and/or Vin de France wine, with no producer relationship. |
| Lampyres | E | Muga; Clos du Tue-Boeuf; Le Grand Cléré; Vindiou | Broad shared grape or Vin de France; the unlabelled producer adjacency implies more than authority says. |
| Labet | D | Louis Michel; Scar of the Sea | Unrelated producers connected through Chardonnay-bearing component wines. |
| Houillon | D | Arnot-Roberts; JONATA; Pax; Lampyres; Bébian | Shared broad grape/classification only. |
| Houillon | E | Muga; Clos du Tue-Boeuf; Le Grand Cléré | Shared Garnacha/Vin de France produces conspicuous cross-region producer adjacency. |
| Steinmetz | D | Château d'Auvernier; Hiyu; Wasenhaus | Shared Pinot Noir/Chardonnay component paths; the central Riesling context is not surfaced. |
| Burgess | D | Clos Apalta; JONATA | Cabernet Sauvignon-bearing wines in different regions. |
| Clos du Tue-Boeuf | E | Houillon; Lampyres; Le Grand Cléré; Bébian; Vindiou | Every adjacency is producer→wine→Vin de France→wine→producer in the composite projection. |

The machine-readable fixture `audits/run-10-human-reference-navigation-ratings.json` contains the complete candidate IDs and full explanations, and the audit tool refuses to evaluate it unless every current displayed link on every sampled page is rated exactly once.

## 6. Lampyres → Matassa test

Current Lampyres display order is:

1. Mourvèdre — outbound representative anchor, direct `MADE_FROM` path;
2. Vin de France — outbound representative anchor, direct `CLASSIFIED_AS` path;
3. France — outbound structural country anchor, no eligible graph path;
4. Matassa — direct graph distance 1, `person:francois-xavier-daure WORKED_FOR producer:matassa`;
5–11. seven broad-grape/classification two-hop producer candidates.

Result:

- Matassa surfaces from Lampyres: **yes**.
- Distance: **1**.
- Predicate: **`WORKED_FOR`**.
- Current rank: **4 of 11**.
- Matassa surfaces Lampyres reciprocally from the Matassa page: **yes, rank 2 of 2**, after France.
- Broad two-hop producer paths do not outrank Matassa because direct graph paths rank before two-hop graph paths.
- Core editorial/structural anchors do outrank Matassa because all anchors outrank all graph paths.
- Matassa is not in immediate cap danger. It would be displaced only after at least 16 outbound/reciprocal anchors plus alphabetically earlier direct graph candidates accumulated. That is possible under growth but materially safer than a two-hop candidate.

The current generator therefore passes the existence and survival portion of this canonical test. It does **not** understand that `WORKED_FOR` is more explanatory than shared grape/classification paths; distance happens to protect the result.

Model B moves Matassa to rank 1 without changing the displayed set. Model E also moves it to rank 1 and removes all seven broad two-hop producer candidates, leaving Matassa, Mourvèdre, Vin de France, and France.

## 7. Broad-grape test

The pressure is real and is caused by composite profile semantics:

`producer profile component wine → MADE_FROM → grape ← MADE_FROM ← target component wine → target producer profile`

The profile-to-profile resolver starts from both wines, so the operative relationship distance is two.

Measured two-hop producer-pair effects:

- Syrah: 30 directed producer pairs / 30 path instances;
- Chardonnay: 20 pairs / 50 path instances;
- Riesling: 12 pairs / 34 path instances;
- Garnacha Tinta: 12 pairs / 26 path instances;
- Cabernet Sauvignon: 12 pairs / 24 path instances;
- Pinot Noir: 12 pairs / 18 path instances, despite Pinot Noir having no reader-facing page.

This is structurally valid: the represented wines really use the grape. It is not reliably editorially useful on producer pages. Labet→Tournelle via Chardonnay plus a shared `USES_PRACTICE` path can be a defensible C; Labet→Louis Michel via Chardonnay alone is D. Burgess→Corison within Napa is C; Burgess→Clos Apalta via Cabernet Sauvignon alone is D. A grape node's degree does not carry the missing context.

For grape pages themselves, direct `MADE_FROM` paths are mostly healthy. The sample grape D/E rate is only 6.98%. The failures are secondary co-occurrence/classification paths such as Syrah→Cabernet Sauvignon through one blend and Mourvèdre→Vin de France through one wine.

## 8. Broad-geography test

Two mechanisms must be distinguished.

### Relationship traversal

France mediates 72 directed peer-geography pairs. Loire→France→Jura is a permitted two-hop path, but “both are in France” does not make Jura a useful next click from Loire. California similarly mixes valid descendant traversal with sibling-state traversal: California→Santa Ynez→Ballard Canyon is useful, while Napa→California→Santa Ynez is not Napa orientation.

Direction matters. A blanket geography-hub penalty would suppress both good and bad cases.

### Structural country anchors

Country pages do not need a relationship path to accumulate producers. Every producer with `country_entity_ids: [place:united-states]` is reciprocally eligible from the United States page. This turns structural placement into an editorial list. At the cap, title alphabetization chooses among producers and internal geography.

This is not an ontology failure and not bad authority. It is incorrect projection semantics for the country reader job.

### Specific site, appellation, practice, and professional paths

Specificity survives today only when it is also encoded as an anchor or a shorter path:

- Lampyres→Matassa (`WORKED_FOR`) is direct and beats every broad two-hop producer path, but three anchors still precede it.
- Houillon→Overnoy (`MENTORED_BY`) is both direct and explicitly anchored, so it ranks second.
- Burgess→Napa (`CLASSIFIED_AS`) and Côtes du Rhône→Houillon/Gilles (`CLASSIFIED_AS` in reverse discovery) are direct and salient.
- California→Santa Ynez→Ballard Canyon is a two-hop descendant relationship and useful; the same predicate family in Napa→California→Santa Ynez is a low-salience sibling path. Direction, not predicate name alone, distinguishes them.
- Labet→Hiyu has both broad Chardonnay paths and a more specific shared `USES_PRACTICE` path. Current ranking ignores the extra specificity and treats it like any other two-hop producer.

The current algorithm therefore does not naturally rank specificity. It benefits incidentally from anchor priority and path length. Predicate-only weighting cannot solve the directional geography case, and degree-only penalties cannot solve the Labet/Hiyu case.

## 9. Displacement forensics

Git snapshots were reconstructed directly from repository history:

- Run 07 main: `ee49ef64465ce5fe022cf9c6715257dca86e853d`;
- Run 08 main: `27f3ab7`;
- Run 09 main: `f74088f`;
- Lampyres/Matassa patch: `0cd3546`.

### Growth stability

| Transition | Common profiles | Current profiles changed | Current prior-link retention | Model E profiles changed | Model E prior-link retention |
|---|---:|---:|---:|---:|---:|
| Run 07 → Run 08 | 130 | 36 (27.69%) | 99.87% (1 removal) | 19 (14.62%) | 100% |
| Run 08 → Run 09 | 146 | 29 (19.86%) | 99.65% (3 removals) | 13 (8.90%) | 100% |
| Run 09 → bridge patch | 159 | 1 (0.63%) | 100% | 1 (0.63%) | 100% |

Added links without removals are expected graph growth. The cases below are actual cap displacement: an old candidate remained eligible but stopped displaying.

### Case 1 — Run 08, United States

- **Before:** San Luis Obispo Coast AVA displayed at slot 15; Pax Wines did not exist as a surfaced candidate.
- **After:** Pax Wines displayed at slot 14; San Luis Obispo Coast AVA remained eligible but fell below the cap.
- **New route:** Pax's new profile carried `country_entity_ids: [place:united-states]`, producing a reciprocal anchor with no relationship path.
- **Why current logic chose it:** reciprocal anchor rank 1 beats the SLO Coast graph/anchor bucket; title ordering resolves remaining peers.
- **Human preference:** the internal AVA. A country page should preserve internal geography before an automatically reciprocal producer.

### Case 2 — Run 09, France

- **Before:** Combe de Savoie displayed at slot 16.
- **After:** newly activated Aurélien & Charlotte Houillon displayed at slot 15; Combe de Savoie remained one of 45 eligible candidates but was displaced.
- **New route:** Houillon's structural `country_entity_ids: [place:france]` created a reciprocal anchor.
- **Why current logic chose it:** every reciprocal country anchor ranks before graph-only geography.
- **Human preference:** Combe de Savoie for country orientation. Houillon may be useful elsewhere, but the present rule has not earned its priority over internal geography.

### Case 3 — Run 09, Jura

- **Before:** Savoie displayed at slot 15.
- **After:** Maison Pierre Overnoy and Renaud Bruyère & Adeline Houillon entered at slots 7 and 8; Savoie remained eligible but was displaced.
- **New routes:** both new producer profiles explicitly anchor `place:jura`, producing reciprocal anchors; no relationship path is required.
- **Why current logic chose them:** reciprocal anchors outrank Savoie's France-mediated two-hop path.
- **Human preference:** the new Jura-specific producers. This is a beneficial displacement and demonstrates that instability is not itself evidence of failure.

### Case 4 — Run 09, United States

- **Before:** Phelan Farm displayed at slot 16.
- **After:** newly activated Burgess Cellars entered at slot 11; Phelan remained eligible but fell below the cap.
- **New route:** Burgess's `country_entity_ids` created another reciprocal country anchor.
- **Why current logic chose it:** both are structural reciprocal country candidates; alphabetical title makes Burgess win.
- **Human preference:** the current model supplies no governed basis to choose Burgess or Phelan. A human country editor would probably choose an undisplayed internal geographic/legal surface before either. This is precisely why country pages need a different projection job.

## 10. Alternative-model comparison

The prototypes do not write Atlas pages. All use the same governed authority and deterministic inputs.

### Model definitions

- **A — Current:** exact production algorithm.
- **B — Direct-first:** direct graph connections before anchors and two-hop candidates; otherwise deterministic. This tests stronger direct-first behavior. Production is already direct-first only within graph candidates.
- **C — Predicate/specificity weighted:** explicit costs favor professional, production, site, grape, and classification predicates over broad `LOCATED_IN`/`WITHIN` paths, with small anchor bonuses.
- **D — Hub-penalized:** direct paths before two-hop paths, then a deterministic penalty based on intermediary degree.
- **E — Profile-kind-aware:** explicit source-kind eligibility gates and target-kind preferences. Country pages prefer structural surfaces and do not accept reciprocal producers unless the country explicitly anchors them; producer pages reject producer→producer two-hop paths that have only broad grape/classification/geography semantics; region/appellation pages reject up-then-down peer geography; grape pages reject unanchored grape/classification co-occurrence at distance two.

### Human-rated performance

| Model | A/B retained | C retained | D/E removed | Sample current links removed | Displayed links overall | Professional paths displayed | Isolated profiles left empty |
|---|---:|---:|---:|---:|---:|---:|---:|
| A current | 100% (109/109) | 100% (76/76) | 0% (0/72) | 0 | 985 | 16/16 | 0 |
| B direct-first | 100% | 100% | 0% | 0 | 985 | 16/16 | 0 |
| C predicate weighted | 95.41% | 98.68% | 0% | 6 | 985 | 16/16 | 0 |
| D hub penalized | 94.50% | 100% | 2.78% | 8 | 985 | 16/16 | 0 |
| E profile-kind-aware | 99.08% (108/109) | 73.68% (56/76) | 97.22% (70/72) | 91 | 697 | 16/16 | 0 |

### Interpretation

**Model B** changes order on 52 of 160 profiles and moves Matassa from Lampyres rank 4 to rank 1, but changes no displayed set. It cannot solve D/E links on profiles below the cap.

**Model C** adds numeric policy but removes no D/E sample links. It loses five A/B links at saturated pages because weighting only chooses different cap winners. It is more complex without solving eligibility.

**Model D** also acts only at ranking time. It removes two D/E links but loses six A/B links. Global degree cannot distinguish California descendant navigation from California sibling traversal. Hub penalties are not justified as the primary fix.

**Model E** is the only prototype that addresses the under-cap problem. It retains all six professional B links, all 16 professional-path candidate pairs overall, 102 of 103 A links, and every isolated page keeps at least one link. It removes all 44 E links and 26 of 28 D links. It retains 56 of 76 C rabbit holes, so it is intentionally conservative and would need acceptance fixtures to protect useful expansions. Its single A loss is St. Helena from Napa: current authority has St. Helena `LOCATED_IN California` but no St. Helena→Napa containment edge. The prototype correctly cannot reconstruct that unstated relationship; the review exposes a targeted authority-completeness gap, not a need to weaken the kind gate.

Model E reduces displayed links by 29.24% while preserving breadth: it still surfaces eight target kinds and 45 source-kind→target-kind combinations, compared with seven target kinds and 44 combinations under current output. It is also more stable in the Run 07→08 and Run 08→09 reconstructions: no prior common-profile link was displaced.

The simple result is that **eligibility semantics matter more than numeric ranking**. Once a candidate is admitted on a page with fewer than 16 candidates, no ranker can remove it.

## 11. Profile-kind analysis

One universal Human Reference resolver is no longer sufficient, although one shared deterministic engine should remain.

### Producer

The reader job is empirically distinct. Direct professional relationships, producer/wine identity, core grapes, appellations, sites, and explicit practices work. Producer adjacency through only a broad grape or national classification does not. Producer sample D/E is 36.00%.

### Grape

Grape pages are the healthiest tested kind. Direct producers and explicit regions/appellations mostly work; D/E is 6.98%. The failure is narrower: grape-to-grape co-occurrence through one blend and broad classification through one wine. A grape rule should prefer where the grape matters and which represented producers/wines illuminate it, not every graph-nearest profile.

Pinot Noir cannot be evaluated as a page because it remains machine-only, although it already acts as a producer-pair intermediary. This is a projection-governance pressure point, not permission for a broad Pinot enrichment run here.

### Region and appellation

These kinds fail most often: 41.07% and 38.46% D/E. The generator needs containment direction and specific represented producers/grapes, not peer surfaces reached by climbing to France or California and descending elsewhere.

### Country

Country pages are conceptually different. Their job is structured orientation, not nearest-profile traversal. Internal regions, appellations, landscapes, legal/classification systems, and represented grapes should receive deterministic families/sections. Producers should appear only through explicit representative selection or a separately governed rule, not because every producer records its country.

### Wine

The proposed wine job is plausible—producer, grapes, sites, practices, and legal identity—but it is not yet earned by this repository sample because there are no surfaced standalone wine profiles. Run 11 should not enable a wine-specific production policy without fixtures.

### Conclusion

Profile-kind semantics are earned for producer, grape, country, region, and appellation. They should be implemented as small inspectable policy tables/gates inside the existing resolver, not as separate hand-maintained graphs or page-specific lists.

## 12. Architecture disposition

The systemic problem belongs to:

- **B. Human Reference projection — primary.** Structural country placement and editorial anchors are conflated; composite profile traversal admits broad adjacency.
- **D. Ranking algorithm — secondary.** Alphabetical order decides within semantic buckets, but ranking alone cannot remove under-cap noise.
- **E. Profile-kind-specific rendering/selection — primary.** Country and geographic pages have different reader jobs from producer and grape pages.

It does **not** belong to STRATA ontology. The existing predicates represent the accepted facts correctly. No relationship should be deleted or weakened because it creates projection noise.

`representative_anchor_ids` does not need a schema change. Its projection semantics remain useful. `country_entity_ids` needs different resolver treatment, not different data.

One targeted authority-completeness issue was exposed: St. Helena AVA is not currently asserted within Napa Valley AVA. That omission can be repaired from fit authority in a focused future pass, but it does not explain the systemic density problem and does not warrant STRATA v0.3.

**STRATA v0.2 remains unchanged.**

## 13. Recommended smallest change

Run 11 should implement a restrained Model E, not the prototype's numeric scoring details:

1. Keep one shared deterministic resolver, the current 16-link cap, canonical profiles, and graph authority.
2. Split projection roles:
   - `representative_anchor_ids` remain strong outbound and reciprocal editorial signals;
   - `country_entity_ids` remains a strong outbound “containing country” link from a subject page;
   - `country_entity_ids` no longer makes every subject a reciprocal country-page recommendation.
3. Add inspectable two-hop eligibility gates by source kind:
   - producer→producer: reject candidates when every path is only shared `MADE_FROM`, `CLASSIFIED_AS`, `LOCATED_IN`, or `WITHIN` through a broad grape/classification/geography; preserve direct, explicit anchors, professional paths, specific site/parcel paths, and explicit shared-practice paths;
   - region/appellation→peer geography: reject up-then-down broad-container paths; preserve direct containment, descendant traversal, and explicit anchors;
   - grape→grape/classification: reject unanchored two-hop co-occurrence through one wine; preserve direct producers and explicit place/appellation anchors;
   - country: order structural internal/reference families first and admit producers only through explicit country-page representative anchors or another separately governed deterministic rule.
4. Within the surviving semantic band, keep deterministic distance and alphabetical/ID tie-breaks. Do not add degree-derived or prestige-like scores.
5. Emit or expose the winning route/predicate family in tests and analysis so future audits can explain every displayed link.

This is more change than “direct-first,” but less complexity than predicate scoring plus hub penalties. The evidence shows direct-first alone is insufficient.

## 14. Explicit non-recommendations

- Do not change STRATA v0.2.
- Do not delete, weaken, or hide correct machine relationships.
- Do not create a hand-maintained Markdown neighbor graph.
- Do not reduce the global cap as a noise fix; 72 D/E sample links appear on under-cap pages.
- Do not eliminate all two-hop traversal; useful producer/practice, place/descendant, and grape/context rabbit holes use it.
- Do not make global hub degree the main ranking signal; degree changes as authority grows and cannot distinguish direction or reader job.
- Do not adopt the prototype's numeric predicate costs as production configuration.
- Do not edit representative anchors page by page to chase generated churn.
- Do not use prestige, fame, price, critic scores, or personal taste.
- Do not activate wine-kind semantics before CARTA has surfaced wine fixtures.
- Do not perform a broad producer, grape, region, country, or appellation research run to solve projection behavior.
- Do not change production ranking in Run 10.

## 15. Proposed Run 11 implementation acceptance criteria

### Architecture and determinism

1. STRATA v0.2, relationship authority, schemas, and evidence policy remain unchanged unless a separately documented representation failure is proven.
2. The implementation is a deterministic, inspectable policy inside the existing generator; no second graph or page-specific neighbor lists.
3. `--write-human-reference` followed by validation is idempotent and leaves no diff.
4. The normal `Validate CARTA` action passes.

### Canonical cases

5. Lampyres surfaces Matassa through direct `WORKED_FOR`; Matassa is never removed by broad grape, country, or Vin de France growth.
6. Houillon retains Overnoy and Bruyère-Houillon; broad Syrah/Garnacha/Vin de France-only producer candidates do not display.
7. Imanol Garay retains Alfredo Egia and Richard Leroy.
8. Clos du Tue-Boeuf does not recommend producers whose only connection is Vin de France.
9. Labet retains Tournelle and Saint Pierre; Louis Michel and Scar of the Sea do not display through Chardonnay alone; a consciously accepted Hiyu practice-specific path is protected by a fixture.
10. Loire, Jura, Savoie, and Côtes du Rhône do not display peer French surfaces solely through France.
11. California retains valid descendant paths such as Ballard Canyon; Napa does not display California siblings solely through California.
12. The United States page preserves internal regions/AVAs before any producer set; adding a producer country assignment cannot displace an internal geographic/legal surface.
13. Riesling's current good producer/region/classification set remains intact.
14. Syrah→Cabernet Sauvignon and Mourvèdre/Syrah→Vin de France do not display without an explicit anchor or more specific governed relationship.
15. No isolated sampled profile becomes empty.

### Quantitative gates

16. On the committed 28-page rating fixture: retain at least 99% of A/B links, remove at least 90% of D/E links, retain at least 70% of C links, and retain 100% of professional B links.
17. Preserve all 16 currently surfaced professional-path candidate pairs.
18. Historical replay across Run 07→08 and Run 08→09 produces no displacement of a previously displayed common-profile link under the new model unless a fixture explicitly accepts the displacement.
19. Add at least one standalone wine-profile fixture before enabling any wine-specific rule.
20. Add a targeted authority test for St. Helena/Napa only after fit authority supplies the missing containment assertion; do not encode that fact in projection code.

## Reproducing the metrics

The audit tool reads only governed JSONL records and imports the production eligibility constants and shortest-path function from `scripts/validate_data.py`.

```text
.venv/bin/python scripts/audit_navigation.py --format markdown
.venv/bin/python scripts/audit_navigation.py \
  --ratings audits/run-10-human-reference-navigation-ratings.json \
  --format markdown
.venv/bin/python scripts/audit_navigation.py \
  --git-ref 27f3ab7 --compare-ref ee49ef6 --format json
.venv/bin/python scripts/audit_navigation.py \
  --git-ref f74088f --compare-ref 27f3ab7 --format json
```

JSON output contains, for every surfaced profile:

- direct and shortest-two-hop candidate counts;
- anchor-only counts;
- raw anchor/path instances;
- unique/deduplicated candidates;
- displayed and displaced counts;
- every eligible relationship-record path, predicate pattern, direction, and intermediary;
- path multiplicity;
- exact displayed lists for Models A–E.

The tool does not write authority or Atlas output.

## Validation

Executed on the audit branch after adding only audit/tooling artifacts:

```text
.venv/bin/python -m py_compile scripts/audit_navigation.py
.venv/bin/python scripts/audit_navigation.py \
  --ratings audits/run-10-human-reference-navigation-ratings.json \
  --format markdown
.venv/bin/python scripts/validate_data.py
```

Result:

```text
PASS entities=505, relationships=524, claims=396, sources=292, names=33, spatial=34, profiles=183
```
