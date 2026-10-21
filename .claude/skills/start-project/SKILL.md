---
name: start-project
description: Moves a generated project from pre-sales to development when the client has signed — syncs the development skills and tools, opens one change per item of the signed release with requirements, scenarios, tasks and the days of estimate.py, checks the days add up, and updates the project's CLAUDE.md. Use it when someone says an offer was accepted, a contract signed, or asks to «start», «kick off development of» a project.
---

# Start the project

The pre-sales documentation becomes the basis for building. Work in the
project folder (the sibling of the generator), with absolute paths. Write in
the project language (`lang` in its `.projectgen.json`).

## 0 · What you need

- **The project**: its folder. If unclear, ask.
- **What was signed**: the whole estimate, the first release only, or a
  different scope (items removed, discounts in days, variations). Always ask:
  the brief's estimate is not the contract. If the user has the offer or the
  contract, read it.
- **The confirmed stack**: usually the brief's, but it may have changed since
  (look for ADRs marked superseded and the newest ones).

## 1 · Sync the tools

```sh
python update_project.py ../<ProjectName>
```

It copies the development skills, `tools/` and the `changes/` and `specs/`
templates from the current generator. It never touches documents, code, specs
or changes.

## 2 · Read

1. `docs/estimate/estimate.py`: items, groups, days per release.
2. `docs/sales/Quote-brief.html`: scope per release, assumptions, exclusions,
   open points.
3. All of `docs/technical/`, ADRs included.
4. `docs/client-sources/` and any detailed specification the client sent after
   the offer.
5. Existing code, if any (a demo, a prototype, the client's base).

## 3 · Specs

`specs/` says what the system does **today**, not what it will do. So:

- **project without code**: `specs/` keeps only its `README.md`. All the
  requirements of the signed scope live in the changes' specs (step 4) and
  reach `specs/` when the changes are archived;
- **project with code**: one file per module in `specs/` (format in
  `specs/README.md`) describing what the code really does, checked by reading
  it. What is missing compared with the signed scope goes into changes.

In both cases:

- requirements and scenarios come from `docs/technical/`, the brief and the
  client's specification; write only the **signed scope**;
- unresolved open points are not requirements: they go in the `proposal.md` of
  the change they affect, under `## To clarify` (`## Da chiarire` in Italian),
  and block only that change.

## 4 · The changes of the first release

For each development item of the signed release, one change
(`python tools/changes.py new <name>`), filled in as `/propose` does:

- **Estimate item** = the exact item name; **Estimated days** = its days in the
  release. Large items (over 10 days) may be split into several changes whose
  days add up to the item.
- Cross-cutting items (project management, testing, training, documentation)
  do **not** become changes: their work is inside the others or tracked
  separately. List them in the summary with their days.
- The change's `specs/` with the module's requirements; `tasks.md` in order;
  `design.md` only where there is a choice to make.
- Dependencies between changes (roles first, then the modules that use them)
  go in `proposal.md` under `## Depends on` (`## Dipende da`).

At the end `python tools/changes.py check` with no problems, and
`python tools/changes.py list`: estimated days of the changes plus those of the
cross-cutting items must match the signed release. If they do not, fix it or
explain why.

## 5 · The project's CLAUDE.md

Update `CLAUDE.md` at the project root:

- **Phase**: «Development of <release>, started on <date>», the signed scope in
  two lines and the deadline if any;
- a **Stack** section with the confirmed technologies and the commands to run,
  test and lint the code (real ones if code exists, otherwise the planned ones
  marked «to confirm at first run»);
- the recommended order of the changes, following dependencies.

The rest of the file stays as it is.

## 6 · Hand-over

Reply with:

- the specs written (modules) and the open changes, with days;
- the check of the days against the signed release;
- the open points still to close with the client, and which changes they block;
- the first change to take: `/apply <name>`, run **with Claude Code opened in
  the project folder**;
- the reminder: commits and pushes are the user's.
