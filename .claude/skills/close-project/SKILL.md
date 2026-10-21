---
name: close-project
description: At the end of a project or a release compares estimated and actual days item by item, writes the actuals report in the project, and updates the «Reference days» table and orders of magnitude in pricing.md, so the next estimates start from real numbers. Use it when someone says a project or release is finished, delivered, closed, or asks for actuals.
---

# Close the project

Estimates only get better if every closed project feeds its real numbers back
into `pricing.md`. This skill does it. Write the project report in the project
language; edit `pricing.md` in its own language.

## 1 · Collect the numbers

In the project folder:

```sh
python tools/changes.py actuals
python tools/changes.py actuals --csv
python docs/estimate/estimate.py --csv
```

- Changes still open are closed (`/archive`) or declared out of the actuals:
  ask the user.
- Cross-cutting items (management, testing, training, documentation) have no
  changes: ask the user for the real days, or an honest estimate. Never invent.
- Read the `## Actuals` sections of archived proposals: they explain the gaps.

## 2 · The project report

Write `docs/actuals.md` in the project:

- table item · estimated · actual · gap, grouped as in `estimate.py`;
- totals per release and overall;
- the main causes of the gaps, in short sentences (scope changed, integration
  harder than expected, client's expectations…);
- work outside the estimate («out of estimate» changes), separately;
- what we would estimate differently next time.

It is an internal document: it does not go to the client.

## 3 · Pricing

In the generator's `pricing.md`:

- in **Reference days**, add or update the rows of this project's components
  with the **actual** days and the project name in the «From» column. If a
  component already exists, write a range covering the real cases (e.g. 8–14 →
  8–16), not an invented average;
- in **Orders of magnitude**, add a line with the scope and real total;
- update «Last updated» at the top.

Rates are not touched: whoever owns pricing decides them.

`pricing.md` is internal: the project name in «From» is fine, nothing else
about the client.

## 4 · Hand-over

Reply with: estimated and actual totals with the gap, the three items with the
largest gap and why, the lines changed in `pricing.md`, and the reminder:
commits and pushes are the user's, in the project and in the generator.
