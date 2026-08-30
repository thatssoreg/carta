# CARTA Atlas Editorial Foundation v1.0

Durable editorial doctrine for CARTA Atlas: what Atlas believes, how it sounds,
what it is allowed to assert, and how future regional worlds are built so that
they share a design language without sharing a personality.

This document governs learner-facing Atlas copy. It does not govern machine
authority. [Evidence policy](evidence-policy.md) decides what CARTA knows;
[Human Reference contract](atlas-projection.md) decides how a profile is written;
this file decides what Atlas says, in whose voice, and with what posture toward
what is still unknown.

---

## 1. Editorial thesis

Conventional wine education is organized around what can be memorized and tested:
grape lists, appellation hierarchies, classification tiers, benchmark styles,
legal thresholds, and an accepted idea of what counts as classic. Atlas carries
that knowledge accurately. It is not the interesting endpoint.

The Atlas thesis is that **a wine style is a temporary settlement**, not a fixed
property of a place. Every "classic" is the current result of pressures that were
once in motion and mostly still are: geology and climate, plant material, farming,
cellar technology, war, replanting, chemistry, trade, regulation, succession,
migration, fashion, accident, and refusal. Jurançon's dry category is younger than
its sweet one. Prosecco stopped being the name of a grape in 2009. Gamay covered
most of the Aube in the 1950s. Naturé is a legal synonym for Savagnin, not
evidence of a method. Each is a place where a settled-looking fact turns out to
have a date on it.

The north star, written to be recoverable in one line:

> **How did this place become this wine, and why might it become something
> different next?**

Three commitments follow.

**Rigor before provocation.** A provocation not supported by a governed claim is
not published. The question form is a way into sourced knowledge, never a
substitute for it.

**Uncertainty is content.** Some unknowns are recognized as unknown — the exact
Garay cellar chronology, whether a parcel sits inside or outside the Irouléguy
line. Others have not yet become questions. A reference that speaks only where
it is certain teaches that wine is settled.

**Producers are historical agents**, not illustrative examples attached to
appellations. They are the mechanism by which regions change.

Atlas is interested in natural wine without treating natural wine as
automatically virtuous, and respects the canon without mistaking it for the end
of the story. Contrarianism for its own sake is the failure mode, and it is as
bad as recitation.

---

## 2. Voice

### Traits

- **Curious, not doctrinaire.** Atlas would rather show why an answer is
  contested than assert the tidier version.
- **Concrete.** Name the mechanism: the wind, the topping regime, the sugar
  threshold, the picking pass. Never "unique," "iconic," or "magical."
- **Culturally literate without being clubby.** Insider knowledge gets
  translated, not performed.
- **Comfortable with limits.** "We do not know yet" is a publishable sentence
  when it is specific about what is missing.
- **Conversational, not sloppy.** Short sentences are allowed. Filler is not.
- **Willing to correct.** A misconception is often the most useful thing on a
  page — but Atlas corrects the idea, never the reader.

### Anti-patterns

- Generic AI prose ("rich tapestry," "storied history," "nestled in") and
  marketing register ("iconic," "legendary," "must-try," "hidden gem").
- Adjective stacks standing in for a mechanism.
- Romantic mysticism without substance — *terroir* as a conclusion rather than a
  set of named factors.
- Rote-memorization posture: permitted-variety lists with no reason to care.
- Gatekeeping, including gatekeeping disguised as connoisseurship.
- **Project-aware prose.** Atlas must not explain its own architecture (§3).
- Apologizing for coverage, or narrating the backlog.
- Counting the interface out loud ("three considered next moves").

### Before / after, from current Atlas copy

**Landing paragraph** — `atlas-app/index.html`

> *Before:* "CARTA keeps cities, rivers, borders, and coasts in view while
> sourced wine geography appears at the scale where it becomes useful."

This describes the software's behavior. The learner is told what the system
does, not what they are about to see.

> *After:* "Cities, rivers and coastlines stay where they are. Wine geography
> arrives when you get close enough for it to mean something — and then keeps
> going, past the borders that wine law asks you to treat as fixed."

**Thin-coverage fallback** — `atlas-app/src/main.js`

> *Before:* "The map has reliable official coverage here. A fuller story can grow
> later; for now, use the shape to orient yourself and compare the wine areas
> around it."

Apologetic, and it makes the roadmap the subject.

> *After:* "This outline is the official production area — its legal shape, drawn
> by the rules. What grows inside it, and who farms it, is a separate question.
> Compare it with the areas it touches."

**Inspector heading** — `atlas-app/src/main.js`

> *Before:* "Why this is interesting"

Asserting interest is the weakest possible way to create it.

> *After:* "What this point is arguing about" — or, better, the world's own
> question (§5) when one applies to the clicked feature.

---

## 3. About Atlas

**CARTA should be almost invisible inside Atlas.** A learner never needs
governance, machine authority, profile maturity, projections, Human Reference or
STRATA, and those words should not appear in learner-facing copy at all.

One place is legitimate, and it should be small, optional and reachable rather
than imposed: an **About Atlas** panel sharing the overlay furniture already built
for **Sources & map meaning**. The Sources dialog carries the honest half of the
story ("The street map, official wine-area shapes, and CARTA's wine stories have
different jobs"); About Atlas carries the worldview half.

The acronym may be expanded exactly once, and only in terms of why the dimensions
matter to understanding wine:

> **CARTA** — Cartography, Ampelography, Relationships, Time, Access.
> Where a wine comes from. What the plant actually is. Who is connected to whom,
> and how. When each of those things changed. And whether you can get near the
> bottle.

### Candidate About Atlas copy

> **A geographic way into wine.**
>
> Most wine education starts with a list to memorize: regions, grapes,
> classifications, the styles that count as classic. Atlas starts with the ground
> instead, and treats the list as the result of something.
>
> Because it usually is. A style that looks permanent normally has a date on it —
> a law written in 1975, a vineyard replanted after a war, a wind that used to
> arrive later in the year, a grower who ignored the accepted answer and turned
> out to be right. Grapes move. People cross borders that wine law treats as
> settled. Climates change while the labels stay the same.
>
> So Atlas begins with the world, then follows the relationships outward: from a
> place to its grapes, from a grape to its relatives, from a producer to the
> people who taught them, and from any of those to somewhere you did not expect
> to end up.
>
> Everything stated as fact here comes from a source you can inspect. Where the
> record is thin or contested, Atlas says so rather than smoothing it over. The
> open questions are part of the subject.

### Landing-page assessment

`A geographic way into wine` and `Start with the world. Then follow the wine.`
are both **strong and should be retained**. They are plain, they promise a method
rather than a mood, and the second names the two halves of the product. The only
weakness is that "follow the wine" is softer than what Atlas does — it follows
relationships, several of which are not wine. A permitted variant if a sharper
line is ever wanted: *Start with the world. Then follow what connects.* The
supporting paragraph beneath the headline is where the real work is needed (§2).

---

## 4. Knowledge versus perspective

The single most important structural rule: **a reader must always be able to
tell what kind of statement they are reading**, without being taught a schema to
do it.

Atlas keeps five registers apart. They already exist in the system; this names
them for editorial use.

| Register | What it is | How it must read | Evidence standard |
|---|---|---|---|
| **Record** | A sourced fact about the world | Stated plainly, attributable on inspection | A governed claim with source IDs |
| **Rule** | What a legal name actually requires | Framed as a specification, dated, never as quality | Current appellation text or equivalent authority |
| **Reading** | Atlas's own interpretation or framing | Visibly Atlas's argument — "the useful way to read this is…" | Must rest on named Records; may not introduce new facts |
| **Culture** | Insider context, transmission, access, vernacular | Bounded, translated, never presented as a legal tier or a ranking | Sourced observation; dated where it can change |
| **Open** | Contested, unresolved, or not yet known | Specific about what is missing and why it matters | A recorded contradiction, a low/unknown confidence, or a named gap |

Practical consequences:

- **A Reading may not manufacture a Record.** An affinity written as Same Energy
  is never written back as a relationship in machine authority.
- **Rules never rank.** *Vendanges tardives* is a narrower legal path with a later
  date and a higher sugar floor, not a higher tier of quality, and copy must not
  let the two ideas touch.
- **Culture never borrows the authority of Rule.** Scarcity, allocation,
  mentorship and house codes are context. The Jura line — *"Scarcity is context,
  not a ranking"* — is the model.
- **Open is published, not hidden.** A visible unresolved question beats a
  smoothed paragraph; the ecosystem *watching* list is the existing pattern.
- **Register words stay out of the interface.** The reader sees the difference
  through placement, framing and inspectable sources, not through category labels.

---

## 5. Questions, provocations and prompts

### The primitive

Recommended name: **Questions Worth Following.**

"Questions & Provocations" over-promises provocation and invites contrarianism.
"Good places to begin" — the current panel label — undersells what these are:
not starting points, but unresolved tensions a learner can actually chase through
the map. *Worth following* carries both the promise and the obligation: if it
cannot be followed, it does not ship.

The data object stays `entry_points`; the learner-facing collection label becomes
Questions Worth Following, with "Pick up the thread" retained as the invitation.
A question may be a question, a flat provocation, a comparison, or an instruction
to notice something. The shape is free; the rules are not.

### Rules

1. **It must be answerable by moving through Atlas** — not by a paragraph, not by
   an external article. If following it changes nothing the learner can see or
   compare, it is decoration.
2. **It must route to a subject that has claims.** Every question carries claim
   IDs and lands on a real subject route.
3. **It must be genuinely open or genuinely counter-intuitive.** "What grapes are
   grown in Jurançon?" is a lookup. "How can ripeness and freshness rise
   together?" is a tension the evidence resolves.
4. **The payoff must exist and must be honest.** If it needs research CARTA does
   not have, it goes to §11, not to the panel.
5. **No rhetorical or marketing questions.** "Ready to discover the magic of the
   Jura?" is not in this family.
6. **Three to five per world**, or the panel becomes a quiz.
7. **At least one should leave the region.** The strongest Atlas move ends
   somewhere the learner did not expect.
8. **Kickers do work**, stating the terms of the tension in a few words so the
   question is not floating.

### Examples

Drawn from subjects already in CARTA or Natural Wine 2.5. Each still requires
claim binding before publication.

1. **Béarn / Jurançon** — *How can ripeness and freshness rise together?*
   *Atlantic rain · mountain wind · patient fruit.* A physical paradox resolved by
   foehn, slope, thick skins and late harvest, with the legal categories as payoff
   rather than premise. **Live; keep as the reference case.**

2. **Jura** — *Why does "oxidative Jura" explain less than people think?*
   *One grape · several cellar decisions.* Two traditions co-exist rather than one
   succeeding the other.

3. **Burgundy ↔ Jura** — *Why does Chardonnay sound like a place in Burgundy and
   a decision in Jura?* *Same grape · two regional scripts.* Existing claim
   support, against the idea that a grape has one identity.

4. **Beaujolais** — *How did the year's cheapest novelty become the reference
   point for modern natural wine?* *Nouveau · a reputation inverted.* "Classic"
   and "cheap" are assignments, and they can swap inside one generation.

5. **Pyrenean Atlantic** — *When does the same grape stop being the same grape?*
   *One plant · two jurisdictions · two legal names.* Petit Courbu is named
   Hondarrabi Zuri Zerratia under Bizkaiko rules, and a 2025 amendment moved its
   status; naming is jurisdictional and time-bound.

6. **Savagnin ↔ Palomino Fino** — *What do Jura and Jerez share that a flavour
   comparison would miss?* *Same Energy · film yeast, different worlds.* The
   mechanism travels; the structure, law and geography do not.

7. **Loire ↔ western Pyrenees** — *What is a Loire grower doing in this story?*
   *The border is a working network.* Garay worked with Leroy; Egia was mentored
   by Garay; the tempting shortcut from Egia to Leroy is explicitly rejected.

---

## 6. Cultural lenses

The existing list has grown faster than its evidence standards: several entries
overlap, several are formats rather than lenses, and one or two are gimmicks
waiting to happen. Keep **four** named lenses in the durable vocabulary, demote
three to structural mechanisms that live elsewhere, retire the rest.

### Keep — the four lenses

**The Tell** — a recognition clue, plus why it works *and* where it misleads.
*For:* turning a label word, a synonym, a bottle shape or a house code into
usable literacy. *Not for:* tasting-note stereotypes or "if it tastes X it must
be Y." *Evidence:* a claim supporting the cue and a stated boundary condition. A
Tell without its failure mode is a myth. The Savagnin *Naturé* note is the model.

**IYKYK** — insider context translated without gatekeeping.
*For:* transmission, house codes, allocation pressure, hospitality practice,
trade vernacular. *Not for:* flattering the reader or signalling that Atlas is on
the inside. *Evidence:* sourced observation, dated where it can change.
**Scarcity/access and food/hospitality fold in here** as instances rather than
surviving as separate lenses — with the standing guardrail that scarcity is
context, never a quality score.

**Same Energy** — a bounded affinity between two things that are not the same.
*For:* mechanism-level resemblance across regions, laws or grape families — the
move that gets a learner out of a region without losing the thread. *Not for:*
vibes, importer-portfolio adjacency, "if you like X try Y." *Evidence:* an
explicit comparison claim plus a stated difference; never written back as a
stylistic-neighbour relationship. **People Also Like retires into this lens** —
same idea, weaker evidence bar, recommendation-engine tone.

**Then / Now** — a dated pair showing a settled-looking thing in an earlier
state. *For:* the core thesis — grape mixes, legal categories, farming norms,
cellar defaults, ripening dates, reputations. *Not for:* decline narratives,
nostalgia, or anything with only one dated end. *Evidence:* **two dated claims,
one per state**, plus an explicit statement of what changed. This is the newest
lens and the one that most directly carries §1; introduce it in one world first.
**Bottle(s) That Changed Things folds in here**, as a Then/Now whose hinge is a
specific wine, with the evidence policy's high-risk language rules applying in
full to any "changed things" assertion.

### Demote — structural, not lenses

**Lineage / producer networks** — too important to be a card. This is §7, and
eventually a network view. As a lens it shrinks into a flourish.

**Helpful Vernacular** — already implemented correctly as the inline glossary and
the practice/word subject grammar (§10). A terminology system, not a lens;
duplicating it as a card gives one word two definitions.

**Culture carriers** — a category label with no evidence standard attached.
Whatever is worth saying under it is IYKYK, Lineage or Then/Now.

### Retire

**A Weird Connection** — Same Energy or a Rabbit Hole, wearing a tone. Naming
weirdness as a category invites reaching for it. Retire the label, keep the
instinct.

**Something to Remember** — a summary device that rewards memorization, which is
the posture Atlas is defined against.

### Not a lens at all

**Rabbit Hole** is navigation, not interpretation: an unexpected supported
connection worth following. It stays a signal on routes and in the trail panel,
and is not presented alongside the four lenses as if it were commentary.

### Standing rules

- **The toolkit is not a checklist.** Two well-earned lenses beat six filled in.
- **Two per subject view is the ceiling**, and a subject may have none.
- **A lens must name a specific thing.** "This region has a rich culture" is the
  absence of a lens, not a lens.
- **A lens never carries the load of a Record.** If the important thing is a
  fact, publish the fact.

---

## 7. Producers animate the world

> Producers are not examples attached to appellations. They are how a region
> changes, and how it is connected to other regions.

An appellation explains what is permitted. A producer explains what was actually
done, by whom, learned from whom, in which decade, with what consequences. Every
mechanism Atlas cares about — farming, technology, style, succession, market
access, the arrival and disappearance of a category — passes through people.

### Editorial treatment

- **Lead with what the producer makes legible**, not with prestige. The existing
  cards already do this: Tournelle makes one cellar decision visible; Labet turns
  parcels into a comparison; Cauhapé puts dry and sweet under one roof. Keep the
  reason line mandatory.
- **A producer set is not a ranking**, said once per world rather than implied by
  ordering. The Béarn line — "These producers are not a ranking" — is the model.
- **Scale, tenure and sourcing are facts, not modesty.** 9.5 hectares, four of
  them terraced, purchased fruit identified separately, beats any adjective.
- **Transmission over trophy.** Read the apprenticeship before the allocated
  bottle.
- **Distinguish person from producer.** Pierre Overnoy and Maison Pierre Overnoy
  are different subjects, and the handoff to Emmanuel Houillon is the interesting
  part.

### Relational storytelling — the Pyrenean Atlantic case

CARTA's Pyrenean Atlantic ecosystem is the best existing demonstration of what
Atlas should eventually feel like, because its boundary is generated by
explanatory relationships rather than drawn in advance on a political map. The
governed network, exactly as CARTA holds it:

- Alfredo Egia `MENTORED_BY` Imanol Garay
- Imanol Garay `WORKED_WITH` Richard Leroy
- Egia, Garay and Gile Iturriondobeitia collaborated in **Hegan Egin**

And, as importantly, what CARTA refuses: Egia `MENTORED_BY` Leroy, Egia
`WORKED_WITH` Leroy and Garay `MENTORED_BY` Leroy are all explicitly rejected
edges, as are Petit Manseng `PARENT_OF` Gros Manseng and Courbu `MUTATION_OF`
Courbu noir.

This is the shape of the eventual experience. As more regions come alive, a
learner in Jurançon should see that the French–Basque edge is a working network —
mentorship, a shared project, fruit and technique crossing a border wine law
treats as absolute — and be able to follow it to the Loire without Atlas ever
collapsing three typed edges into one flattering lineage story. The distance
between "Egia and Leroy are two steps apart in a documented chain" and "Leroy
mentored Egia" is exactly the distance between this product and wine folklore.

Editorial requirements for network storytelling:

1. **Show the type, not just the link.** Mentorship, worked with, collaborated on
   a named project and family succession are four different things, and the
   difference is usually the lesson.
2. **Two-step chains are shown as two steps**, never as one relationship.
3. **Cultural relevance is not spatial relocation.** Garay and Egia illuminate
   Jurançon's world; their vineyards do not move into it, and the copy says so —
   as the current Béarn lens already does.
4. **Rejected edges are teachable.** Name the tempting edge, then why it is
   blocked; Natural Wine 2.5's `STOP` register shows the form.
5. **The first network map is relational, not geometric.** Useful spatial
   knowledge exists before polygons do.

### Cellar research as an entry point

Some of CARTA's deepest material originated with specific bottles. The durable
principle:

> **A bottle is an entry point, not a category.** The personal origin of a
> research dossier is not product context, and Atlas never contains a cellar.

A wine subject opens outward — wine → producer → grape → place → people → lineage
→ another region — using the same subject grammar as everything else; the existing
"Read the bottle outward" framing is already correct. Nothing in Atlas should
indicate that one wine entered CARTA because someone owned it and another did
not. Provenance of *research attention* is not provenance of *knowledge*, and only
the second projects.

---

## 8. Natural Wine 2.5 → CARTA → Atlas

Three projects, three jobs.

| | Holds | Produces for the next stage |
|---|---|---|
| **Natural Wine 2.5** | Teaching intelligence, cultural framing, misconception discipline, historical arcs, producer canon and countercanon | Research questions, framings, distinctions that matter, coverage signals, contradictions |
| **CARTA** | Reconciled reusable knowledge: entities, claims, sources, relationships, geography, time | Governed claims and typed relationships |
| **Atlas** | The interactive spatial and editorial experience | A learner who can follow a relationship and knows what kind of statement they just read |

### What should flow from NW2.5 into Atlas

- **Misconception discipline** — the highest-value import. The glossary
  register's inclusion test (a term earns a place only if the trade contradicts
  its technical meaning, it names two things that must be kept apart, it is a
  conclusion disguised as a description, a category word mistaken for a
  certification word, or it carries a moral charge the evidence does not support)
  is *exactly* the standard for The Tell.
- **Register separation.** The history spine keeps evidence, interpretation,
  contested material and movement mythology visibly apart. That is §4, arrived at
  independently.
- **Historical change.** The seven arcs, and the nine parallel histories that must
  not collapse into one origin story, are raw material for Then/Now.
- **Relationship discipline.** The influence network's edge types and its rule
  that shared taste, importer portfolio, proximity or fandom cannot support a
  lineage edge is the posture CARTA encodes as typed and rejected edges.
- **Regional framing and failure modes** — the landscape briefs already name what
  goes wrong: "treating 'Jura' as one landscape — Arbois, Pupillin and the
  Sud-Revermont are different maps sharing a page."
- **Vocabulary that carries a verdict.** Clean, funky, authentic, minimal
  intervention, terroir: banned as conclusions there, and for the same reason
  here.
- **Producer significance, stylistic distinctions, comparisons, canon and
  countercanon** — as candidate subjects and framings for future worlds.

### Boundaries

- **NW2.5 is not a runtime source.** Atlas reads CARTA. Nothing in the curriculum
  repository is loaded by the application, ever.
- **NW2.5 is not automatic factual authority.** A curriculum statement becomes an
  Atlas statement only after entering CARTA as a claim with its own sources and
  confidence; curriculum register marks do not transfer as claim status.
- **No prose is copied wholesale.** Framings and distinctions travel; sentences do
  not.
- **Curriculum-internal identifiers never appear in Atlas** — producer codes,
  session numbers, ring assignments, matrix references.
- **Rings, tiers and canon membership are not Atlas categories.** They are course
  structure, and importing them would smuggle in a ranking Atlas does not make.
- **Corrections travel upstream, not sideways.** An error found in Atlas is fixed
  in CARTA's governed records first, then re-projected.

---

## 9. Environmental legibility

Atlas should eventually carry two layers of environmental context, and they do
different jobs.

**Layer one — wine-professional shorthand.** Compact labels of the "cool
continental / moderate maritime / warm Mediterranean" family. Their value is
translation: they let someone carry Atlas knowledge into vocabulary they already
use and compare a new region against known ones. Short, visually secondary,
always attached to a subject.

**Layer two — the actual drivers.** Rainfall, elevation, slope, aspect, wind,
maritime influence, continentality, diurnal range, frost, rivers, mountains,
geology, soils. These explain the wine, and they are what make a region
individual — which shorthand by definition cannot.

### How they coexist

1. **Shorthand never appears alone.** A label with no drivers behind it is a
   memorization prompt — the posture §1 rejects.
2. **Drivers never require the shorthand.** Jurançon's lesson is Atlantic rain, a
   drying autumn foehn, steep terraced slopes and late thick-skinned grapes. No
   three-word climate label improves that sentence.
3. **Shorthand is a derived, sourced, dated value — not a vibe.** A category
   assigned decades ago may already be wrong, and Atlas of all products should
   not present a stale classification as a permanent property.
4. **Do not ingest broad WSET-style climate categories without reconciliation.**
   Adopting a category system wholesale imports an authority CARTA has not
   examined and labels places on the basis of nothing.
5. **The driver set is per-region, not a template.** Jura needs escarpment, marl
   banding and altitude; Béarn needs Atlantic rainfall, foehn and slope. A
   universal driver form produces universal copy.
6. **Environmental context must answer a question the world is already asking**,
   not fill a panel.

### Principle for future terrain work

Terrain is not designed in this run. The posture is:

> **Terrain must answer a question already asked in the copy.** Relief, slope and
> aspect earn their place when they explain something the learner has a reason to
> care about — why ripening survives an Atlantic autumn, why an escarpment
> produces banded marl, why one side of a valley behaves differently. Terrain
> rendered for atmosphere is expensive decoration, and it makes every region look
> like every other region.

The usual provenance rules apply: no geometry without provenance, and no geometry
inference merely for visual completeness.

---

## 10. Terminology

Specialized vocabulary is not the enemy; undefined specialized vocabulary is.
Atlas already has the right mechanism — inline glossed terms carrying a
definition, a "why it matters" line and claim IDs. The standard below protects it
from becoming clutter.

**Standard:**

1. **Define at first learner-facing use, within the subject view** — not in a
   separate glossary the reader must go find.
2. **Two parts, always: what it means, and why it matters here.** The second part
   is what separates Atlas from a dictionary. *Ouillé* means topped up; it matters
   because it is the most useful word for dismantling the idea that every Jura
   white is oxidative.
3. **Two sentences maximum per part.** A definition needing a paragraph is a
   subject, not a term.
4. **Subtle but visible.** The term stays readable in the sentence; the definition
   arrives without navigating away and without a modal.
5. **Every glossed term carries claim support** and links onward when a real
   subject exists — `voile` to the practice, `passerillage` to the appellation
   that regulates it.
6. **Six glossed terms per subject view is the ceiling**, and gloss only the word
   the copy actually needs.
7. **Do not gloss a conclusion.** *Terroir*, *natural*, *clean*, *funky*,
   *authentic*, *minimal intervention* are contested frames, not glossable terms.
   If they appear, they appear as the subject of a Tell.

**`foehn` is explicitly flagged.** It must receive inline explanation on every
learner-facing surface where Béarn or Jurançon copy uses it, including the world
thesis, where it currently appears. It is the load-bearing term in that world's
central question, unfamiliar to most English-language readers, and doing causal
work in the sentence. The existing definition is right in shape: a warm, dry
downslope wind which in Jurançon can interrupt the wet Atlantic pattern during the
long autumn — and which matters because it explains concentration without
pretending the foothills are arid.

Terms already carrying this treatment, and which should stay: *voile*, *sous
voile*, *ouillé*, *élevage*, *flor*, *marl*, *mistelle*, *passerillage*, *sec*,
*tries successives*, *vendanges tardives*. Terms to add as their worlds arrive:
*climat*, *lieu-dit*, *schist*, *carbonic maceration*, *ancestral method*.

---

## 11. Research gaps

> **Interesting rabbit holes should not hit a wall and die.**

When Atlas finds a promising connection CARTA cannot yet support, there are
three legitimate outcomes and one forbidden one. The forbidden one is filling
the space with generic prose. Fabrication is not on the list at all.

**Close it now** — small enough to resolve inside the current world build. One
specific fact is missing, a known authority states it, verification takes minutes
rather than a session, and nothing else depends on the answer. *Example: the
commune count for an appellation's production area.*

**Open a dossier** — deserving its own focused research run. It would unlock a
genuinely new relationship or an entire subject; it recurs across more than one
world; it touches a high-risk claim category (parentage, succession, mentorship,
legal status, boundaries, causal claims about style); the evidence likely exists
but needs real source work; and the payoff is a question a learner would follow.
*Examples already on the watching list: the Garay cellar chronology, the Garay
parcel relative to the Irouléguy boundary, the Gile / Guillermo Iturriondobeitia
identity crosswalk.* Record the gap where the subject lives, name what is missing
and what it would unlock, and leave it visible.

**Let it go** — a low-value tangent. Interesting only to the editor; the payoff is
one fact with nothing attached; the sources would be promotional or circular; or
the answer would change nothing a learner can see or compare. Say nothing rather
than gesturing at it.

Two supporting rules:

- **A named open question is publishable content.** The ecosystem *watching* list
  is the existing pattern and a learner-facing form of it belongs in Atlas. "We do
  not yet know whether this parcel falls inside the Irouléguy boundary" is more
  interesting than most settled facts.
- **A gap is never filled with a Reading.** A paragraph of framing where a fact
  should be is the most damaging thing Atlas can publish.

---

## 12. Regional individuality

Future worlds share a **design language**. They must not share a **personality**.

**Shared — the grammar.** The pillar structure (Place, Grapes & Wines, People,
Culture, Rules), the four lenses, Questions Worth Following, inline terminology,
map reactions, the trail, the register discipline of §4, and the honesty rules
about geometry and coverage. A learner who has used one world should never have
to relearn how Atlas works.

**Not shared — the argument.** Each world has one central tension that decides
what leads, what gets space, and which lenses earn a place:

- **Jura** — the cellar decision. A grape name settles almost nothing, and two
  traditions co-exist rather than one succeeding the other. *Grapes & Wines and
  the practice vocabulary lead.*
- **Béarn / Jurançon** — a climate paradox with a legal resolution. *The Place
  leads; the Rules land the payoff.*
- **Beaujolais** — reputation and market: one grape and one region occupying
  opposite positions within a generation. *The People and a Then/Now lead.*
- **Burgundy** — boundary and hierarchy: one patch of ground belonging to several
  wine geographies at once. *The Rules and the map lead.*
- **Loire** — breadth, and the limits of a single name. *The Place and the network
  lead.*

Three consequences:

1. **Every world states its own thesis in one sentence**, and that sentence is the
   world. No world ships with a generic thesis.
2. **Pillar emphasis is per-world.** A pillar with nothing specific to say should
   be thin rather than padded.
3. **No world's copy may serve as another world's default.** This is currently
   violated — Jura-specific fallback prose sits in the application as the default
   for any world without its own pillar copy. That is how a product acquires one
   voice for every place.

---

## 13. Editorial checklist

Run before a regional world ships.

1. Can the world's argument be stated in **one sentence no other world could use**?
2. Is there at least one **Question Worth Following that leaves the region** — and
   does following it arrive somewhere?
3. Does every question, lens and featured connection **resolve to a subject with
   claims**, with no dead ends?
4. Could a reader tell **Record from Rule from Reading from Culture from Open**
   without being taught the difference?
5. Does any **legal category** anywhere imply quality or hierarchy?
6. Does every **producer card** say what that producer makes legible rather than
   why they are admired, with the "not a ranking" framing present?
7. Are **relationships shown with their type**, and two-step chains shown as two
   steps?
8. Is every **specialized term glossed at first use** with a "why it matters" line
   — `foehn` included wherever Béarn or Jurançon copy uses it?
9. Are there **more than two lenses on any subject view**, or any lens filling a
   slot rather than naming something specific?
10. Does any **climate shorthand appear without its drivers**, or any driver set
    that is a template rather than this region's actual problem?
11. Is there **at least one dated fact showing this world was once different** —
    and is any "classic" presented as timeless?
12. Does any copy **explain CARTA, the roadmap, or the interface** to the reader?
13. Are **coverage limits stated plainly** rather than apologized for, and is every
    known gap closed, dossiered, or deliberately dropped?
14. Read aloud: does any sentence sound like **marketing, a tasting-note
    stereotype, or generic AI prose**?

---

## Immediate Editorial Application Backlog

Concrete changes implied by this foundation. **P1 and P2 were applied in Run 07
(`atlas-run-07-editorial-foundation`)**; P3 remains open. Ordered by value.

**P1 — structural · applied in Run 07**

1. **Remove Jura-specific fallback copy from the application.**
   `atlas-app/src/main.js` uses Jura pillar prose ("Five principal grapes share a
   compact region…", "Jura's cultural pull is easiest to understand through
   transmission and access…") as the default for any world lacking `pillar_copy`.
   Replace with neutral structural defaults, or require `pillar_copy` per world
   and fail validation without it. The single biggest threat to §12.

2. **Rewrite the landing supporting paragraph.** Keep both existing lines; replace
   the CARTA-behavior sentence beneath them (§2). Update the meta description at
   the same time.

3. **Add an About Atlas panel**, reusing the Sources dialog furniture, with the §3
   copy. Expand the acronym once. Link it from the Sources dialog, not the
   primary navigation.

4. **Rename the discovery collection to Questions Worth Following**, keeping "Pick
   up the thread" as the invitation. Retire "Good places to begin."

**P2 — copy corrections · applied in Run 07**

5. **Replace the thin-coverage fallback string** ("A fuller story can grow
   later…") with the non-apologetic version in §2. It currently appears on every
   mapped feature without a world.

6. **Replace "Why this is interesting"** in the inspector with a heading that
   shows rather than asserts — ideally the active world's question when one
   applies to the clicked feature.

7. **Replace "Three considered next moves"** with "Where this goes next," and
   remove interface counting from headings generally.

8. **Tighten the trail-panel copy** ("A little trail of what caught your
   attention" → "What caught your attention, in order").

9. **Gloss `foehn` in the Béarn world thesis.** It is defined in the glossary but
   appears in `place:bearn`'s thesis; confirm the inline term markup fires there
   and on every surface using the word.

**P3 — editorial vocabulary · open**

10. **Reduce the lens vocabulary to four** (The Tell, IYKYK, Same Energy,
    Then/Now). The published legend registers only IYKYK and Same Energy while The
    Tell is used as a signal — reconcile legend, signals and this document so one
    vocabulary is in force.

11. **Reclassify the Jura scarcity lens as an IYKYK instance**, keeping its text
    intact. Same for future access and hospitality material.

12. **Pilot one Then/Now in a single world.** Jurançon's 1936 sweet recognition
    against the 1975 dry recognition is the cleanest available pair, already dated
    in the ecosystem timeline, and it demonstrates directly that a "classic" style
    has a date on it.

13. **Add the Jura question** *Why does "oxidative Jura" explain less than people
    think?* to the Jura entry points. The current set is strong but leads with
    size rather than with the region's actual tension.

14. **Surface a short learner-facing open-questions treatment** on one subject,
    modelled on the ecosystem watching list — starting with the Petit Manseng /
    Savagnin relationship, already bounded short of parentage and a better
    teaching moment as an open question than as a footnote.

---

### What Run 07 changed

1. Jura's pillar copy, Place story and rule grammar moved out of `atlas-app/src/main.js`
   and into Jura's own release data. The application now carries no regional prose:
   a pillar with no authored lede renders thin, and a world with no rule groups
   renders none. `scripts/build_atlas.py` and `scripts/validate_atlas.py` both refuse
   a regional world that does not author its own pillar copy, Place story and rule
   grammar, so §12 is enforced rather than merely stated.
2. The landing paragraph and meta description no longer describe the software's
   behavior. **About Atlas** ships as an overlay sharing the Sources furniture,
   reachable from the Sources dialog rather than the header, expanding the acronym
   once. The discovery collection is **Questions Worth Following**.
3. The thin-coverage fallback, the inspector heading, the "Keep wandering" kicker
   and the trail-panel line were replaced per §2. The inspector now renders the
   world thesis through the inline-term pipeline instead of stripping its markup,
   so `foehn` is glossed on that surface too (§10).

**Known, deliberately deferred:** `regionalAreaScaleMarkup` in the application still
carries a hard-coded Jura appellation allow-list. It is gated to `place:jura` and so
cannot leak into another world, but the list belongs in world data before a third
world ships.

---

**Governs:** learner-facing CARTA Atlas copy and future regional world builds.
**Does not govern:** machine authority, claim status, or Human Reference profile
structure.
**Companions:** [CARTA Atlas](carta-atlas.md) · [Human Reference contract](atlas-projection.md) · [Evidence policy](evidence-policy.md) · [Architecture](architecture.md)
