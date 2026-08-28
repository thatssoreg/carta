# CARTA audits

This directory holds the audit material that still participates in current Human Reference quality control.

It is not machine authority. Canonical knowledge lives in [`../data/`](../data/), and projection rules live in [`../docs/atlas-projection.md`](../docs/atlas-projection.md).

## Current navigation-quality baseline

- [`run-10-human-reference-navigation-ratings.json`](run-10-human-reference-navigation-ratings.json) is the fixed A/B/C/D/E ratings fixture used to measure navigation regressions.
- [`run-10-human-reference-navigation-salience-density.md`](run-10-human-reference-navigation-salience-density.md) records the benchmark and salience analysis that established the fixture.
- [`run-11-human-reference-kind-aware-navigation.md`](run-11-human-reference-kind-aware-navigation.md) records the durable reasoning behind the current kind-aware navigation policy.

The production resolver, tests, and validator are authoritative for current behavior. These audits explain why the current regression fixture and navigation semantics exist.

## Historical execution audits

Completed run-by-run reconciliation and maintenance reports were useful while CARTA was under construction, but they no longer belong in the active repository reading path. They remain recoverable through Git history rather than being maintained as a parallel status archive.
