# Run 07 · Editorial foundation, first application

**Release:** `atlas-run-07-editorial-foundation`
**Governed by:** [`docs/atlas-editorial-foundation.md`](../docs/atlas-editorial-foundation.md)
**Scope:** landing, About, voice, copy system. No terrain, no new world, no new
subjects, no Natural Wine 2.5 ingestion.

Run 07 changes what Atlas says. It changes no geometry, no claim, no relationship
and no subject: `scripts/project_editorial.py` refuses to write if the subject
projection moves, and it did not — all 53 native subjects reproduced byte-identically
from the committed inputs.

## What was wrong

The foundation named one structural failure and a set of copy failures.

The structural one: **Jura's prose was the application's default.** `atlas-app/src/main.js`
held Jura's five pillar ledes, Jura's Place story, Jura's rule intro and a hard-coded
list of Jura appellation IDs, each used whenever a world lacked its own. Béarn masked
this because Béarn authors its own copy. Any third world would have opened speaking as
Jura — and the rule-group fallback would have rendered Arbois and Château-Chalon
buttons inside it, or thrown on a subject lookup. This is the §12 failure mode
verbatim: one voice for every place.

The copy failures were the four in §2 and the backlog: a landing paragraph that
described the software's behavior, a coverage fallback that apologized and narrated the
roadmap, an inspector heading that asserted interest instead of creating it, and headings
that counted the interface out loud.

## What changed

**Structural.** Jura's copy moved into Jura's own release data
(`data/atlas/run-07-editorial-foundation.json`). The application now holds no regional
prose at all: a pillar with no authored lede renders thin rather than padded (§12.2),
and a world with no rule groups renders none. Pillar intros fall back only to neutral
structural labels that name a pillar's job rather than any region's argument.

Enforcement, so this cannot regress by omission: `build_atlas.py` and `validate_atlas.py`
both refuse a regional world that does not author its own pillar copy, Place story and
rule grammar, and reject a rule group pointing at a non-native area. Two tests cover the
same ground from the artifact side, including an assertion that no sentence of one
world's copy appears in another world's, or in the application.

`load_experience_config` now resolves the whole `extends` chain rather than one level.
It previously merged only the newest overlay onto its immediate parent, which meant a
third release would have silently dropped Run 05. Run 07 is the first release where that
mattered.

**Copy.** Landing paragraph and meta description rewritten to the §2 replacement; both
landing lines kept, as §3 requires. Coverage fallback, inspector heading, "Keep wandering"
kicker and trail-panel line replaced. The discovery collection is now **Questions Worth
Following**, with "Pick up the thread" retained as the invitation and the header
affordance relabelled from "Start here", which undersold the panel in the same way the
retired label did. The inspector renders the world thesis through the inline-term
pipeline instead of stripping the markup with a regex, so `foehn` is glossed on that
surface too — the §10 requirement and backlog item 9.

**About Atlas** ships as an overlay sharing the Sources dialog's furniture, reachable
from inside the Sources dialog and not from the header, carrying the §3 copy and
expanding the acronym exactly once. The two dialogs cross-link.

## Checklist (§13) against the changed surfaces

| # | Item | Result |
|---|---|---|
| 1 | One-sentence argument no other world could use | Both worlds; enforced |
| 4 | Record / Rule / Reading / Culture / Open distinguishable | Coverage fallback now separates the legal shape from what grows in it |
| 5 | Legal category implying quality | None introduced |
| 8 | Specialized term glossed at first use, `foehn` included | Now true on the inspector surface |
| 12 | Copy explaining CARTA, the roadmap or the interface | Removed from landing, coverage, inspector and headings |
| 13 | Coverage limits stated plainly, not apologized for | Rewritten |
| 14 | Read aloud: marketing or generic AI prose | None found; sweep clean |

Items 2, 3, 6, 7, 9, 10, 11 concern world content rather than this run's surfaces and
were not re-litigated.

## Verification

- `scripts/validate_atlas.py` — PASS (53 native subjects, 22 editorial subjects, 4 entry points)
- `tests/test_atlas.py` + `tests/test_navigation.py` — 33 tests, all passing
- `npm run build` — clean
- All 39 `document.querySelector` targets in `main.js` resolve against `index.html`
- Pillar rendering exercised directly for Jura, Béarn and a world with no authored copy:
  the bare world renders five pillars, borrows no sentence from either world, and emits
  no empty lede paragraph

## Deliberately not done

- **P3 (items 10–14)** — lens vocabulary reduction, the Jura scarcity reclassification,
  the first Then/Now, the extra Jura question and the learner-facing open-questions
  treatment. These change editorial vocabulary and world content, not the copy system,
  and belong to their own run.
- **`regionalAreaScaleMarkup`** still carries a hard-coded Jura appellation allow-list.
  It is gated to `place:jura` and cannot leak into another world, but the list is world
  data and should move before a third world ships.
- **Terrain, new worlds, content enrichment** — explicitly out of scope.
