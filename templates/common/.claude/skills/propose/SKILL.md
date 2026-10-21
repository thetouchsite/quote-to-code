---
name: propose
description: Opens a new change in changes/<name>/ — proposal, added or modified requirements with scenarios, design, checklist of tasks — tied to the estimate item and its days. Use it before building anything that changes the system's behaviour, when someone asks to «add», «change», «start working on» a feature or module.
---

# Propose

Before writing code, write down what changes. A change is a folder in
`changes/<name>/`; create it with the script, then fill it in.

Write in the project language (`lang` in `.projectgen.json`). The keywords
follow it, and `tools/changes.py check` enforces them:

| | English project | Italian project |
| --- | --- | --- |
| Requirement heading | `### Requirement: …` | `### Requisito: …` |
| Obligation | SHALL / MUST | DEVE / NON DEVE |
| Scenario | `#### Scenario: …` with **WHEN** / **THEN** / **AND** | `#### Scenario: …` with **QUANDO** / **ALLORA** / **E** |
| Delta sections | `## Added / Modified / Removed requirements` | `## Requisiti aggiunti / modificati / rimossi` |
| Proposal fields | Status, Estimate item, Estimated days, Actual days | Stato, Voce di stima, Giornate stimate, Giornate reali |
| Fill-in marker | TO-WRITE | DA-SCRIVERE |

## 1 · Name and folder

- A short name, lowercase with dashes, naming the capability:
  `class-booking`, `two-level-commissions`, `fix-reminders`.
- Check it does not exist: `python tools/changes.py list`.
- Create it: `python tools/changes.py new <name>`.

## 2 · Read before writing

- `specs/` of the modules touched: what the system does today.
- `docs/technical/` and `docs/technical/adr/`: how it is built, what was decided.
- `docs/estimate/estimate.py`: the item that covers this work and its days.
- The code that will be touched, enough not to propose the impossible.

If something unclear would change the work substantially, ask the user before
writing. Otherwise pick the most reasonable reading and write it in the
proposal.

## 3 · `proposal.md`

- **Estimate item**: the exact item name in `estimate.py`. If no item covers
  the work, write «out of estimate» («fuori stima») and tell the user: it is a
  change request, and sales decides.
- **Estimated days**: the item's days (or the share of it, if an item is split
  into several changes; the shares never exceed the item). For work out of
  estimate, your estimate, using the reference days in the generator's
  `pricing.md` if available.
- **Status**: `open` (`aperta`).
- Why, what changes, specs touched, what stays out: short sentences.

## 4 · The change's specs

For each module touched, `changes/<name>/specs/<module>.md` with only the
differences, under the added / modified / removed sections (format in
`changes/README.md`).

- A requirement states an obligation and is verifiable.
- Every requirement has at least one scenario; edge cases that matter
  (permissions, missing data, errors) are scenarios of their own.
- A **modified** requirement repeats the exact title used in `specs/` and the
  full new text, not just the changed part.
- If the module has no file in `specs/` yet, everything goes under «added».

## 5 · `design.md`

Only when there is a choice to make or data to change. Contestable choices
become an ADR in `docs/technical/adr/` (Status, Context, Decision,
Consequences). Otherwise delete the file.

## 6 · `tasks.md`

- Small tasks (half a day at most), in order of execution, grouped by area.
- The last section is always verification: a test for every scenario, plus
  `python tools/changes.py check <name>`.

## 7 · Check and hand-over

```sh
python tools/changes.py check <name>
```

Fix until it reports no problems. Then reply with: the folder, the estimate
item and days, each new or changed requirement in one line, the assumptions
made, and the next step: `/apply <name>`.

No commits: the user does them.
